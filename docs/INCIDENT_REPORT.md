# Incident report — protected SSH simulation

## Scope and environment

- Execution date: 2026-10-17 (UTC)
- Kali: Kali 2026.1 ARM64, lab IP `10.77.0.10`
- Target: Ubuntu Server 24.04.3 ARM64, hostname `ubunto-lab`, lab IP `10.77.0.20`
- Network: UTM Host Only; the two guests had no default route when isolation was verified
- SIEM: Splunk Enterprise 10.6.1.1 on Apple Silicon macOS; UI and management interfaces bound to loopback
- Response: Fail2ban SSH jail, `maxretry=5`, `findtime=60s`, `bantime=600s`, nftables action
- Evidence: eight genuine, unedited JPG screenshots in `evidence/2026-10-17/`; observations and limitations are in `evidence/2026-10-17/OBSERVATIONS.md`

## Hypothesis

Repeated failed SSH password attempts from one source should produce authentication events. Splunk should support investigation of those events. Fail2ban should temporarily block the source after the configured retry threshold.

## Timeline (UTC)

| Time | Action / observation | Evidence |
|---|---|---|
| 15:55:42–15:55:52 | Protected, bounded simulator ran from Kali using a nonexistent username and deliberately wrong passwords | `05-simulation-completed.jpg`, `04-sshd-events.jpg` |
| 15:55:44, 15:55:49, 15:55:52 | Ubuntu recorded three `Failed password` messages from `10.77.0.10` | `04-sshd-events.jpg` |
| 15:55:51.232 | Fail2ban logged `Ban 10.77.0.10`; its counter showed six matching journal events, not six distinct password attempts | `01-fail2ban-ban.jpg`, `03-fail2ban-log.jpg` |
| After ban | nftables contained `10.77.0.10` in its SSH ban set and rejected its TCP/22 traffic; Kali's next connection returned `Connection refused` | `02-nftables-rule.jpg`, `06-ssh-blocked.jpg` |
| Later | Splunk indexed 16 exported journal events; SPL aggregation found three failed-password records from Kali for `soclab_nonexistent` | `07-splunk-ingestion.jpg`, `08-splunk-failed-passwords.jpg` |

## Investigation

- Splunk index/source: `soc_lab`, `soclab:sshd`, host `ubunto-lab`.
- Export window: 2026-10-17 15:55:35–15:56:10 UTC (35 seconds); 16 journal lines were ingested.
- Failed-password result: 3 records, source `10.77.0.10`, user `soclab_nonexistent`.
- No accepted authentication was observed in the exported window. This is limited to the exported events.
- Fail2ban's six matches include different SSH/PAM journal messages from connections; the count is not a count of distinct password attempts.
- Splunk's prepared threshold of five failed-password records was **not** triggered by this run. Splunk did not initiate the block.

## Response and validation

Fail2ban independently applied a temporary source-IP block. The jail status, Fail2ban log, nftables set/rule and refused follow-up SSH connection were all observed. Ban expiry and restored connectivity have not been verified yet.

## Limitations and remaining work

This is a bounded simulation against owned, isolated lab VMs. It does not demonstrate credential recovery, detection of every brute-force technique, production readiness, or SCC integration. A baseline run, Splunk scheduled alert, packaged dashboard validation, ban-expiry recovery test, and continuous log forwarding remain pending. Fixed time windows can split events; legitimate user errors can create false positives. Investigate context before production response.

## Interview explanation

Describe only personally executed steps. Explain the journal evidence and SPL extraction, state that Fail2ban performed the block independently, and distinguish the verified ad hoc search from the untriggered scheduled alert.
