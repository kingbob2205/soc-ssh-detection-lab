#!/usr/bin/env python3
"""Bounded SSH lab simulation; client observations are not server/SIEM evidence."""
import argparse
import datetime as dt
import ipaddress
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

LAB = ipaddress.ip_network("10.77.0.0/24")
USER = "soclab_nonexistent"

def target_ip(value):
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Supply a single lab IPv4 address") from exc
    if address.version != 4 or address not in LAB or address in (LAB.network_address, LAB.broadcast_address):
        raise argparse.ArgumentTypeError("Target must be a host on the isolated 10.77.0.0/24 lab segment")
    return str(address)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=target_ip)
    parser.add_argument("--phase", required=True, choices=["baseline", "protected"])
    parser.add_argument("--isolated-lab-confirmed", action="store_true", required=True,
                        help="Confirm this is your dedicated, isolated VM lab")
    parser.add_argument("--attempts", type=int, choices=range(1, 13), default=12)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.dry_run:
        print(json.dumps({"target": args.target, "phase": args.phase, "attempts": args.attempts,
                          "username": USER, "network_connections": 0}))
        return 0
    for binary in ("ssh", "sshpass"):
        if not shutil.which(binary):
            parser.error(f"Missing {binary}; install dependencies inside the Kali lab VM")
    run = Path("runs") / (dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + "-" + args.phase)
    run.mkdir(parents=True, exist_ok=False)
    events = []
    for number in range(1, args.attempts + 1):
        env = dict(os.environ, SSHPASS=f"IntentionallyWrong-LabOnly-{number:02d}")
        command = ["sshpass", "-e", "ssh", "-F", "/dev/null", "-p", "22",
                   "-o", "ConnectTimeout=3", "-o", "ConnectionAttempts=1",
                   "-o", "PreferredAuthentications=password", "-o", "PubkeyAuthentication=no",
                   "-o", "NumberOfPasswordPrompts=1", "-o", "StrictHostKeyChecking=accept-new",
                   "-o", f"UserKnownHostsFile={run / 'known_hosts'}",
                   f"{USER}@{args.target}", "true"]
        try:
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=8)
            error = result.stderr.lower()
            outcome = "permission_denied" if "permission denied" in error else "connection_error"
            if result.returncode == 0:
                outcome = "unexpected_success_STOP"
            events.append({"utc": dt.datetime.now(dt.timezone.utc).isoformat(), "attempt": number,
                           "returncode": result.returncode, "outcome": outcome})
            if result.returncode == 0:
                break
        except subprocess.TimeoutExpired:
            events.append({"utc": dt.datetime.now(dt.timezone.utc).isoformat(), "attempt": number,
                           "outcome": "timeout"})
        time.sleep(1)
    (run / "client-results.json").write_text(json.dumps({"target": args.target, "phase": args.phase,
        "username": USER, "client_observations_only": True, "events": events}, indent=2) + "\n")
    print(f"Client observations saved in {run}. Verify real Ubuntu logs and ban evidence separately.")
    return 1 if any(e["outcome"] == "unexpected_success_STOP" for e in events) else 0

if __name__ == "__main__":
    raise SystemExit(main())
