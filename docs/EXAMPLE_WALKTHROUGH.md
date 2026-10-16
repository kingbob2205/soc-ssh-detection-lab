# Worked example — illustrative, not an executed incident

This page explains what a completed run would look like. The IP addresses, log lines, and counts below are examples written for teaching. They are **not collected evidence**, must not be imported as proof of completion, and do not establish that Splunk or Fail2ban was tested.

## Scenario

A Kali VM (`10.77.0.10`) sends a bounded set of incorrect SSH password attempts to a dedicated Ubuntu VM (`10.77.0.20`). The fixed username does not exist. The objective is to detect the behavior, identify its source, and validate a temporary host-level block.

## Planned sequence

1. Prepare the isolated VMs and check time synchronization, SSH configuration and journal availability.
2. Record the baseline start time and run the simulation on Kali.
3. Export the Ubuntu SSH journal for that window.
4. Upload the real export to `soc_lab` in Splunk with sourcetype `soclab:sshd`.
5. Extract source IP and username, count failures, and inspect successful authentication events.
6. Enable the provided Fail2ban jail and repeat the same bounded simulation.
7. Verify the source IP appears in the jail ban list and corresponding nftables rule.
8. Compare connectivity before the ban, during it, and after expiration/unban.
9. Complete the actual incident report with original evidence.

## Illustrative authentication event

```text
2026-10-16T10:00:01+00:00 ubuntu-lab sshd[1234]: Failed password for invalid user soclab_nonexistent from 10.77.0.10 port 51000 ssh2
```

Interpretation:
- The authentication failed; this line does not show a successful compromise.
- The attempted username was invalid.
- The source was `10.77.0.10`; the remote source port was `51000`.
- The timestamp places the attempt within the investigation window.
- Additional context comes from other events and the VM/network inventory.

## How the detection works

`01_failures.spl` groups failed password events by source and host. `02_threshold.spl` identifies sources with at least five failures inside a fixed one-minute time bucket. `03_auth_timeline.spl` includes accepted password/public-key events so the analyst does not assume that failures imply the absence of successful access.

If 12 matching events from the same source occur in one bucket, an illustrative threshold result would show `failures=12`. A real run may produce another count or split events across buckets; report actual observations rather than forcing this number.

## Response rationale

Fail2ban independently watches the SSH journal. Five matching failures within 60 seconds should trigger a temporary 600-second source-IP ban. This is a lab threshold, not a universal production recommendation. The Splunk query does not initiate the block.

## Evidence needed before claiming success

- Real UTC timestamps and exported SSH events.
- Splunk data preview, query and actual result rows.
- Fail2ban status showing the expected source IP.
- The matching firewall rule and an independent client connectivity test.
- Recovery after the ban expires or is removed.

A connection timeout by itself could also mean a disconnected VM, a routing problem or a stopped SSH server. It must be correlated with the host response evidence.

## What to explain in an interview

Why SSH generates these events; how field extraction and thresholds work; why one invalid-password attempt is different from repeated guessing; the false-positive risks; why Fail2ban and Splunk play different roles; and how you would verify recovery. Present this as a designed lab until you have personally executed it.
