# Setup and execution

## 1. Create the lab

Use dedicated Kali and Ubuntu VMs. Retain existing personal VMs unchanged. Choose a host-only network that allows the two guests to communicate; configure a private `10.77.0.0/24` segment, for example Kali `10.77.0.10` and Ubuntu `10.77.0.20`. Do not use a bridged office/home LAN for this exercise. Verify the actual UTM network settings and both guest routes. Install packages using temporary NAT connectivity before the exercise, then disconnect that adapter. Guest package downloads require Internet access; the simulation does not.

Create a snapshot before the exercise and retain UTM console access. Record OS versions, CPU architecture, VM topology, IPs, and UTC time in the incident report. Ensure clocks are synchronized before disconnecting Internet access. Do not assume UTM defaults use this subnet or permit VM-to-VM communication.

Ubuntu preparation (inside the dedicated target VM):

```bash
sudo apt-get update
sudo apt-get install openssh-server fail2ban nftables
sudo systemctl enable --now ssh
sudo /usr/sbin/sshd -t
sudo /usr/sbin/sshd -T | grep -E 'passwordauthentication|kbdinteractiveauthentication|loglevel'
sudo journalctl -u ssh.service -n 20 --no-pager
```

The simulation needs password authentication available on the **dedicated isolated guest** to produce `Failed password` events. If it is disabled, do not weaken an existing or production host; configure a disposable lab VM appropriately first. No root password or real account credentials are used. Check that `soclab_nonexistent` does not exist with `getent passwd soclab_nonexistent` (expected: no entry). Do not create that user.

On a newly prepared lab VM only, keep the response jail inactive for the baseline run. If Fail2ban is already protecting another purpose, use a fresh VM instead of stopping existing protection.

Kali preparation:

```bash
sudo apt-get update
sudo apt-get install python3 openssh-client sshpass
```

## 2. Baseline simulation (before enabling the response jail)

On Ubuntu record a UTC start timestamp:

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
```

From Kali, in this repository:

```bash
python3 scripts/simulate_ssh.py --target 10.77.0.20 --phase baseline --isolated-lab-confirmed
```

This is a small password-guessing simulation against an invalid username, not a successful compromise. Client `permission_denied` results are not server-log or SIEM evidence.

On Ubuntu export the event window, replacing the example timestamp with the recorded start time:

```bash
sudo journalctl -u ssh.service --since '2026-10-16 10:00:00 UTC' -o short-iso --no-pager > ubuntu-ssh.log
```

Import this real file into Splunk Web using Add Data -> Upload. Create/select index `soc_lab`, set sourcetype `soclab:sshd`, and host `ubuntu-lab`. Review timestamp extraction in the preview before submitting. Use All time for first investigation, then narrow to the experiment window. Run `splunk/searches/01_failures.spl` and `02_threshold.spl`. Save search results and screenshots locally. See the Splunk README for offline versus scheduled searches.

## 3. Enable host response

Copy `config/sshd-soclab.local` to Ubuntu:

```bash
sudo install -m 0644 config/sshd-soclab.local /etc/fail2ban/jail.d/sshd-soclab.local
sudo fail2ban-client -t
sudo systemctl enable --now fail2ban
sudo fail2ban-client reload
sudo fail2ban-client status sshd
```

The jail uses the systemd backend and nftables. Confirm that packages and permissions support the action; a running service alone does not prove a working ban.

## 4. Repeat and verify

From Kali:

```bash
python3 scripts/simulate_ssh.py --target 10.77.0.20 --phase protected --isolated-lab-confirmed
```

From the Ubuntu console:

```bash
sudo fail2ban-client status sshd
sudo journalctl -u fail2ban --since '10 minutes ago' --no-pager
sudo nft list ruleset
```

A Fail2ban installation may log to `/var/log/fail2ban.log` instead of the journal. Inspect the active logging configuration and capture the relevant ban entry.

Record the source IP in the banned list, the corresponding nftables rule, and a connection test from Kali while the ban is active:

```bash
ssh -o ConnectTimeout=3 -o ConnectionAttempts=1 soclab_nonexistent@10.77.0.20
```

Timeout/refusal alone is inconclusive: rule evidence and the source-IP ban must agree. After the ten-minute ban expires (or the controlled unban below), verify that the same source can again reach the SSH authentication prompt. Never infer blocking simply from a falling count in Splunk.

Export the protected SSH window separately and import it once; avoid reimporting the baseline data. Use `03_auth_timeline.spl` to investigate successful and failed logins. Fewer logged failures after blocking do not by themselves prove there was no compromise.

## 5. Cleanup

From Ubuntu console, to unban the lab source early:

```bash
sudo fail2ban-client set sshd unbanip 10.77.0.10
```

Restore the lab snapshot or remove only this project's jail file and reload Fail2ban after reviewing other jails. Keep the lab isolated. Restore guest network adapters only after the simulation has stopped. Do not publish raw personal logs or credentials.

## Completion gate

The project is complete only when real evidence proves: baseline authentication failures, Splunk ingestion and query results, the protected run, a matching Fail2ban ban/firewall rule, and the before/during/after connection behavior. Complete the incident report and update status with the actual date. A rendered dashboard without data does not satisfy this gate.
