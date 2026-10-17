# Splunk investigation content

Splunk Enterprise is the SIEM/search platform for this lab. Enterprise Security is not required. Obtain a valid installation/license through Splunk and verify architecture compatibility. No license or account is supplied here.

## Simple workflow

Verified on Splunk Enterprise 10.6.1.1 running on the Apple Silicon macOS host. For this test, Splunk monitored a local copy of the Ubuntu SSH journal export, assigning index `soc_lab`, sourcetype `soclab:sshd`, and host `ubunto-lab` (the guest's actual hostname spelling). A basic count returned 16 events. An ad hoc search for `Failed password`, with `rex` extraction and `stats` aggregation, returned three failures from Kali at `10.77.0.10` for `soclab_nonexistent`. See the dated screenshots and observations in `../evidence/2026-10-17/`.

To reproduce with a new authorized lab export, create index `soc_lab`, add a monitor input for the local export file, and set its sourcetype to `soclab:sshd` and its host to match the source system. Check event timestamps, then paste the searches from `searches/` into Search. The tested export was local to the Mac; continuous forwarding from Ubuntu has not been configured.

## Optional app installation (self-managed Splunk Enterprise)

Copy `app/` as `$SPLUNK_HOME/etc/apps/soc_ssh_lab/` using the Splunk service owner's permissions. Restart Splunk in accordance with your local lab setup. This app does not create an index or configure data inputs; do those explicitly first. It contains no credentials, external connections, email actions, or active automatic blocking.

The included saved search is **disabled by default**. After validating real data, enable/schedule it through Splunk Web if your license permits alerts. It uses a one-minute rolling search and five failures per source/host. Historical uploads require the standalone SPL with an appropriate time range; an enabled real-time schedule will not detect old imported timestamps. Inspect results for duplicate ingestion and extraction failures. Confirm an actual triggered alert separately from a successful ad hoc search.

The ad hoc search has been verified on a live local Splunk instance. The packaged dashboard, scheduled alert, and expiry retest remain unverified. Static checks only confirm that files parse and expected sections exist.
