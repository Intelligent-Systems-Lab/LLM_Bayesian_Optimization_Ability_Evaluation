## Q17. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (LSTM-2, SGD, fedadam, lr=0.001961, batch=64, epochs=20) → 0.6000
- (GPT-like, RMSprop, fedadam, lr=0.000142, batch=8, epochs=7) → 0.5780
- (BERT-base, SGD, fedprox, lr=0.000028, batch=64, epochs=7, mu=0.2) → 0.7849
- (LeNet5, AdamW, fedprox, lr=0.008077, batch=64, epochs=18, mu=0.2) → 1.4258
- (ResNet18, AdamW, fedprox, lr=0.063303, batch=128, epochs=34, mu=0.0) → 0.6214
- (ResNet101, RMSprop, fedadam, lr=0.219661, batch=64, epochs=40) → 1.4679
- (ResNet50, SGD, fedavg, lr=0.073407, batch=64, epochs=30) → 1.3688
- (LeNet5, Adam, fedprox, lr=0.004635, batch=256, epochs=22, mu=0.0) → 3.8660
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)