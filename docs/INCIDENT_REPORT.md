# Incident report — pending execution

## Scope and environment
- Actual execution date (UTC): pending
- Kali version / architecture / IP: pending
- Ubuntu version / architecture / IP: pending
- UTM network isolation verified: pending
- Splunk version / architecture / license type: pending
- Evidence files and SHA-256 hashes: pending

## Hypothesis
Repeated failed SSH password attempts from one source should produce authentication events. Splunk should identify the concentration of failures. An enabled Fail2ban jail should temporarily block that source after the configured retry threshold.

## Timeline
| UTC time | Action / observation | Evidence |
|---|---|---|
| Pending | Baseline, detection, response, and retest | Pending |

## Investigation
- Failure count, time window, source IP, and username: pending
- Successful authentication events in the same window: pending
- SPL query and result export: pending
- Alternative explanations and false-positive risks: pending

## Response and validation
- Why this action was selected: pending
- Ban list and matching firewall rule: pending
- Before/during/after connectivity results: pending
- Who/what initiated the block: Fail2ban independently; not Splunk
- Cleanup and recovery: pending

## Limitations
This is a bounded simulation using invalid credentials on owned lab VMs. It does not demonstrate credential recovery, detection of every brute-force technique, production readiness, or SCC integration. Threshold detection may miss distributed/slow attempts; fixed time buckets split events near bucket boundaries. Legitimate user errors can cause false positives. Investigate context before taking production action.

## Interview explanation
Describe only personally executed steps, explain the underlying log evidence, and distinguish a prepared detection from one actually tested in Splunk.
