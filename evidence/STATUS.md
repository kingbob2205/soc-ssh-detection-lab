# Verification status

| Item | Status | Evidence |
|---|---|---|
| Repository, scripts, searches and runbook | Prepared | Versioned source |
| Local script guardrails and static config checks | Passed: 8 tests on 2026-10-16 | Python unittest; not VM results |
| Isolated Kali and Ubuntu network | Verified during setup; private IPs rechecked 2026-10-17 | UTM Host Only; Kali 10.77.0.10, Ubuntu 10.77.0.20; no default route verified during setup |
| Baseline SSH simulation | Pending | No genuine run captured |
| Splunk ingestion and SPL execution | Verified for ingestion and failure aggregation on 2026-10-17 | Splunk Enterprise 10.6.1.1 macOS ARM64; 16 ingested events, 3 Failed password events from 10.77.0.10; screenshots 07–08. Threshold alert and dashboard remain untested |
| Protected SSH simulation | Executed 2026-10-17 | Kali run directory runs/20261017T155542.363870Z-protected; completion screenshot; raw client manifest remains in Kali |
| Fail2ban source-IP blocking | Verified 2026-10-17 | 2026-10-17/01–06 screenshots: ban list, nftables rule, SSH events, Fail2ban log and refused client connection |
| End-to-end lab completion | Pending | Requires all runtime evidence |

Never replace Pending with Verified based on generated example logs, source code, or a screenshot of a configured but untested tool. Raw logs, screenshots, and client-run manifests are ignored by Git until reviewed and sanitized.
