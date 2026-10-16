import argparse
import importlib.util
from pathlib import Path
import configparser
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("simulation", ROOT / "scripts/simulate_ssh.py")
simulation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(simulation)

class LabChecks(unittest.TestCase):
    def test_no_public_loopback_lan_or_hostname_targets(self):
        for value in ["8.8.8.8", "127.0.0.1", "192.168.1.1", "example.com", "::1", "10.77.0.0", "10.77.0.255"]:
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                simulation.target_ip(value)

    def test_exact_lab_target(self):
        self.assertEqual(simulation.target_ip("10.77.0.20"), "10.77.0.20")

    def test_dry_run_never_connects(self):
        with patch.object(simulation.subprocess, "run", side_effect=AssertionError("network forbidden")):
            self.assertEqual(simulation.main(["--target", "10.77.0.20", "--phase", "baseline", "--isolated-lab-confirmed", "--dry-run"]), 0)

    def test_attempt_limit(self):
        with self.assertRaises(SystemExit):
            simulation.main(["--target", "10.77.0.20", "--phase", "baseline", "--isolated-lab-confirmed", "--attempts", "100"])

    def test_explicit_isolation_ack_required(self):
        with self.assertRaises(SystemExit):
            simulation.main(["--target", "10.77.0.20", "--phase", "baseline", "--dry-run"])

    def test_dashboard_well_formed(self):
        tree = ET.parse(ROOT / "splunk/app/default/data/ui/views/ssh_lab.xml")
        self.assertEqual(len(tree.findall(".//query")), 3)

    def test_alert_not_enabled_by_install(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read(ROOT / "splunk/app/default/savedsearches.conf")
        self.assertEqual(config["SOC Lab - Repeated SSH failures"]["disabled"], "1")

    def test_jail_uses_journal_and_finite_ban(self):
        config = configparser.ConfigParser()
        config.read(ROOT / "config/sshd-soclab.local")
        self.assertEqual(config["sshd"]["backend"], "systemd")
        self.assertEqual(config["sshd"]["bantime"], "600")

if __name__ == "__main__":
    unittest.main()
