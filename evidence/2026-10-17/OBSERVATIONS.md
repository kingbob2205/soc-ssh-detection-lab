# Protected SSH simulation: observed results

Actual VM execution on 2026-10-17. These notes transcribe visible console observations; they are not raw log exports. JPGs are original screenshots, without editing.

- Kali source: `10.77.0.10`, Ubuntu target: `10.77.0.20`, SSH TCP/22.
- Executed the repository simulator with `--phase protected --isolated-lab-confirmed` and the default bound of 12 attempts. No Hydra was used.
- Kali reported run output saved under `runs/20261017T155542.363870Z-protected`. The raw client manifest remains on Kali and has not yet been inspected or exported.
- Ubuntu journal shows invalid-user and failed-password events for `soclab_nonexistent` from Kali. Three failed-password records are visible at 15:55:44, 15:55:49 and 15:55:52 UTC. These are authentication failures, not successful logins.
- Fail2ban's log records five matched events before a ban at **15:55:51.232**, followed by one more match. Its status shows total failed 6, total banned 1 and banned IP `10.77.0.10`. A matched-event counter must not be described as six distinct password attempts: multiple log records can correspond to one connection.
- The `nftables` set contains `10.77.0.10`; the chain rejects TCP/22 traffic from addresses in that set.
- A subsequent Kali `nc -vz -w 3 10.77.0.20 22` returned `Connection refused`, consistent with the matching reject rule.
- Configured jail parameters visible in the log: maxRetry 5, findtime 60 seconds, bantime 600 seconds.

## Evidence

1. `01-fail2ban-ban.jpg`: before/after jail counters and ban list.
2. `02-nftables-rule.jpg`: source IP set and SSH reject rule.
3. `03-fail2ban-log.jpg`: event matches, threshold parameters and ban timestamp.
4. `04-sshd-events.jpg`: genuine journal authentication records.
5. `05-simulation-completed.jpg`: client command and completion location.
6. `06-ssh-blocked.jpg`: refused SSH port connection from Kali.

## Still pending

Post-expiry recovery verification, baseline phase, scheduled threshold alert and dashboard. Fail2ban blocked independently; Splunk's subsequent investigation did not initiate blocking. No successful credential compromise is claimed. The screenshots in this directory are the reviewed evidence selected for publication.

## Splunk investigation verified later the same day

- Installed official Splunk Enterprise 10.6.1.1 macOS ARM64 archive; SHA-512 matched the official download digest. Runtime is outside the repository. Web and management services configured for loopback access.
- Exported genuine SSH journal records over SSH from Ubuntu for 2026-10-17 15:55:35–15:56:10 UTC. A local raw export (not included in this repository) contains 16 lines; SHA-256 `201aede0d9d801382da183c283d37104fa76ff17f681fe7706da1d1fc5b09fb4`.
- Monitor input indexed these as `index=soc_lab`, `sourcetype=soclab:sshd`, `host=ubunto-lab` (actual guest hostname spelling).
- Splunk UI query `index=soc_lab sourcetype="soclab:sshd" earliest=0 | stats count by host sourcetype` returned 16 events. Evidence: `07-splunk-ingestion.jpg`.
- Ran an SPL search filtering `"Failed password"`, extracting user/source IP/source port with `rex`, then aggregating `stats count as failures values(user) as users by host src_ip`. Result: host `ubunto-lab`, source `10.77.0.10`, failures **3**, user `soclab_nonexistent`. Evidence: `08-splunk-failed-passwords.jpg`.
- The prepared threshold of five Failed password records would not trigger on this protected run's three password failures. Fail2ban counted multiple matching messages per connection. Do not equate its six matches with six password failures or claim the threshold alert fired.
