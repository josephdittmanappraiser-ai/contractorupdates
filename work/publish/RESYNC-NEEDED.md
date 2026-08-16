# Eight pages that may have been overwritten with stale content

The batch-1 agent from the earlier 78-page run was still working when the full
103-page republish started. It finished afterwards, publishing the pre-orange build
of these eight pages. If a final-run agent had already published the current build
for one of them, that page is now a version behind.

Re-publish these from disk after the final run completes, then delete this file.

97LkciO7  UsCWiuFS  NsLO2nOG  CdSdKzBe  DlIKTBQI  wDPxEfiY  JkmOSCGO  J2niBBpI

The batch-2 agent from that run finished later still, with the same problem. Its eight:

XRbBTenE  EnZXkDw7  6om1Ew5L  VTYG7Q8l  ANQ8zEnL  aDBxl6nR  CpQZ9LtX  VaWXHk0M

All sixteen are listed in work/publish/batches/resync.tsv.

Lesson for the runbook: never start a publish run while an earlier one is still in
flight. A stale writer that finishes late silently reverts a page, and nothing in the
tooling notices -- both agents report success, because both did exactly what they were
told with the bytes they had.
