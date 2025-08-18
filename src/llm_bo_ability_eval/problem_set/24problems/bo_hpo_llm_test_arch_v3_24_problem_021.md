## Q21. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet50, Adam, fedprox, lr=0.126951, batch=128, epochs=28, mu=0.05) → 0.5908
- (ResNet101, SGD, fedprox, lr=0.076832, batch=64, epochs=42, mu=0.2) → 1.4432
- (LeNet5, SGD, fedprox, lr=0.002867, batch=64, epochs=24, mu=0.1) → 1.4282
- (BERT-base, Adam, fedavg, lr=0.000018, batch=32, epochs=1) → 0.5614
- (ResNet18, AdamW, fedadam, lr=0.122719, batch=256, epochs=32) → 3.8380
- (GPT-like, RMSprop, fedavg, lr=0.000150, batch=16, epochs=1) → 0.5567
- (LSTM-2, AdamW, fedavg, lr=0.001756, batch=32, epochs=18) → 0.8249
- (ResNet18, AdamW, fedadam, lr=0.198230, batch=128, epochs=28) → 0.5945
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)