## Q24. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet50, SGD, fedadam, lr=0.074337, batch=64, epochs=28) → 1.3606
- (LeNet5, AdamW, fedadam, lr=0.005792, batch=64, epochs=18) → 1.3760
- (ResNet18, Adam, fedadam, lr=0.242697, batch=64, epochs=30) → 1.4281
- (ResNet101, AdamW, fedadam, lr=0.119079, batch=64, epochs=44) → 1.4455
- (GPT-like, RMSprop, fedprox, lr=0.000301, batch=32, epochs=1, mu=0.05) → 0.6322
- (BERT-base, SGD, fedavg, lr=0.000047, batch=32, epochs=3) → 0.5486
- (LSTM-2, RMSprop, fedavg, lr=0.004522, batch=128, epochs=22) → 1.4866
- (GPT-like, AdamW, fedadam, lr=0.000188, batch=16, epochs=3) → 0.5139
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)