## Q9. GP (continuous) — Architecture=ResNet50, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.050000, wd=0.00000, drop=0.10 → y=0.5454
- lr=0.100000, wd=0.00010, drop=0.20 → y=0.4996
- lr=0.200000, wd=0.00510, drop=0.30 → y=0.5470
**Candidates** (evaluate EI):
- lr=0.080000, wd=0.00000, drop=0.15
- lr=0.120000, wd=0.00210, drop=0.25
- lr=0.160000, wd=0.00610, drop=0.35