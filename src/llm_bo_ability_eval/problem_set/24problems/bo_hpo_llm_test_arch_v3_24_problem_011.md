## Q11. GP (continuous) — Architecture=BERT-base, Optimizer=AdamW
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.000015, wd=0.00500, drop=0.00 → y=0.5466
- lr=0.000030, wd=0.01000, drop=0.10 → y=0.5000
- lr=0.000060, wd=0.01500, drop=0.20 → y=0.5474
**Candidates** (evaluate EI):
- lr=0.000024, wd=0.00700, drop=0.05
- lr=0.000036, wd=0.01200, drop=0.15
- lr=0.000048, wd=0.01600, drop=0.25