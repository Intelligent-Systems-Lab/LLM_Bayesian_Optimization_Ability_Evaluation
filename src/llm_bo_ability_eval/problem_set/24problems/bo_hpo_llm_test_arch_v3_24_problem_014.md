## Q14. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet101, RMSprop, fedavg, lr=0.211479, batch=256, epochs=40) → 3.9307
- (ResNet50, RMSprop, fedprox, lr=0.066977, batch=64, epochs=30, mu=0.1) → 1.4138
- (LeNet5, SGD, fedavg, lr=0.004214, batch=128, epochs=22) → 0.5506
- (BERT-base, SGD, fedadam, lr=0.000045, batch=32, epochs=3) → 0.5385
- (LSTM-2, SGD, fedavg, lr=0.001170, batch=64, epochs=22) → 0.6409
- (ResNet18, Adam, fedprox, lr=0.045422, batch=64, epochs=28, mu=0.05) → 1.4559
- (GPT-like, AdamW, fedprox, lr=0.000198, batch=32, epochs=1, mu=0.0) → 0.5956
- (GPT-like, SGD, fedadam, lr=0.000167, batch=16, epochs=5) → 0.5373
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)