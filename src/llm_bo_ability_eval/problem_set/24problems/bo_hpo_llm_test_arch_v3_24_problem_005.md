## Q5. GP (continuous) — Architecture=LSTM-2, Optimizer=Adam
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.001000, wd=0.00000, drop=0.20 → y=0.5446
- lr=0.002000, wd=0.00000, drop=0.30 → y=0.4988
- lr=0.004000, wd=0.00500, drop=0.40 → y=0.5462
**Candidates** (evaluate EI):
- lr=0.001600, wd=0.00000, drop=0.25
- lr=0.002400, wd=0.00200, drop=0.35
- lr=0.003200, wd=0.00600, drop=0.45