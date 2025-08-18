## Q1. GP (continuous) — Architecture=LeNet5, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.002500, wd=0.00000, drop=0.10 → y=0.5438
- lr=0.005000, wd=0.00010, drop=0.20 → y=0.4980
- lr=0.010000, wd=0.00510, drop=0.30 → y=0.5454
**Candidates** (evaluate EI):
- lr=0.004000, wd=0.00000, drop=0.15
- lr=0.006000, wd=0.00210, drop=0.25
- lr=0.008000, wd=0.00610, drop=0.35