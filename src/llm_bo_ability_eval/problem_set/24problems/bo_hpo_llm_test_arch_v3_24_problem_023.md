## Q23. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet101, RMSprop, fedadam, lr=0.082056, batch=64, epochs=40) → 1.4190
- (GPT-like, SGD, fedavg, lr=0.000312, batch=16, epochs=7) → 0.5781
- (ResNet18, Adam, fedadam, lr=0.169218, batch=128, epochs=30) → 0.5685
- (BERT-base, SGD, fedadam, lr=0.000044, batch=32, epochs=1) → 0.5384
- (LeNet5, RMSprop, fedadam, lr=0.005311, batch=64, epochs=24) → 1.3919
- (LSTM-2, SGD, fedadam, lr=0.001644, batch=64, epochs=22) → 0.6077
- (ResNet50, RMSprop, fedprox, lr=0.044721, batch=64, epochs=30, mu=0.2) → 1.4493
- (GPT-like, AdamW, fedavg, lr=0.000252, batch=16, epochs=7) → 0.5496
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)