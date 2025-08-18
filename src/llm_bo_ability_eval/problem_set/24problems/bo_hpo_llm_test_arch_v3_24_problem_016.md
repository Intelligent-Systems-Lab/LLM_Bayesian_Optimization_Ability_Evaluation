## Q16. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (GPT-like, Adam, fedadam, lr=0.000099, batch=16, epochs=3) → 0.5673
- (LSTM-2, Adam, fedprox, lr=0.002845, batch=64, epochs=18, mu=0.0) → 0.6238
- (ResNet101, RMSprop, fedavg, lr=0.137087, batch=64, epochs=42) → 1.4415
- (ResNet18, SGD, fedavg, lr=0.246967, batch=128, epochs=30) → 0.6009
- (BERT-base, RMSprop, fedprox, lr=0.000049, batch=64, epochs=3, mu=0.0) → 0.7753
- (LeNet5, SGD, fedprox, lr=0.007054, batch=128, epochs=22, mu=0.1) → 0.5754
- (ResNet50, RMSprop, fedavg, lr=0.203583, batch=256, epochs=34) → 3.8993
- (LSTM-2, AdamW, fedprox, lr=0.000994, batch=64, epochs=18, mu=0.1) → 0.6742
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)