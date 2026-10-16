# Verification status

| Item | Status | Evidence |
|---|---|---|
| Repository, scripts, searches and runbook | Prepared | Versioned source |
| Local script guardrails and static config checks | Passed: 8 tests on 2026-10-16 | Python unittest; not VM results |
| Isolated Kali and Ubuntu network | Pending | No verified lab topology |
| Baseline SSH simulation | Pending | No genuine run captured |
| Splunk ingestion and SPL execution | Pending | No Splunk instance tested |
| Fail2ban source-IP blocking | Pending | No live ban verified |
| End-to-end lab completion | Pending | Requires all runtime evidence |

Never replace Pending with Verified based on generated example logs, source code, or a screenshot of a configured but untested tool. Raw logs, screenshots, and client-run manifests are ignored by Git until reviewed and sanitized.
