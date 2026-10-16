# Splunk investigation content

Splunk Enterprise is the SIEM/search platform for this lab. Enterprise Security is not required. Obtain a valid installation/license through Splunk and verify architecture compatibility. No license or account is supplied here.

## Simple workflow

Create index `soc_lab` through Splunk Web. Upload the genuine Ubuntu journal export, assign sourcetype `soclab:sshd` and host `ubuntu-lab`, and verify the timestamps in preview. Paste searches from `searches/` into Search. If using the XML dashboard, create a Classic dashboard and paste `app/default/data/ui/views/ssh_lab.xml` into Source.

## Optional app installation (self-managed Splunk Enterprise)

Copy `app/` as `$SPLUNK_HOME/etc/apps/soc_ssh_lab/` using the Splunk service owner's permissions. Restart Splunk in accordance with your local lab setup. This app does not create an index or configure data inputs; do those explicitly first. It contains no credentials, external connections, email actions, or active automatic blocking.

The included saved search is **disabled by default**. After validating real data, enable/schedule it through Splunk Web if your license permits alerts. It uses a one-minute rolling search and five failures per source/host. Historical uploads require the standalone SPL with an appropriate time range; an enabled real-time schedule will not detect old imported timestamps. Inspect results for duplicate ingestion and extraction failures. Confirm an actual triggered alert separately from a successful ad hoc search.

All SPL, dashboard behavior and alert scheduling remain unverified until run on a real Splunk instance. Static checks only confirm that files parse and expected sections exist.
