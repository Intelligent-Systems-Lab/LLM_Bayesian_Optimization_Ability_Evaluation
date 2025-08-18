## Q12. GP (continuous) — Architecture=GPT-like, Optimizer=AdamW
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.000100, wd=0.01500, drop=0.00 → y=0.5506
- lr=0.000200, wd=0.02000, drop=0.10 → y=0.4964
- lr=0.000400, wd=0.02500, drop=0.20 → y=0.5438
**Candidates** (evaluate EI):
- lr=0.000160, wd=0.01700, drop=0.05
- lr=0.000240, wd=0.02200, drop=0.15
- lr=0.000320, wd=0.02600, drop=0.25