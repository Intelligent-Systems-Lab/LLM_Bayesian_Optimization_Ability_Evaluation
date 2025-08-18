## Q20. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (LSTM-2, SGD, fedavg, lr=0.004389, batch=32, epochs=22) → 0.8658
- (ResNet18, SGD, fedavg, lr=0.080172, batch=64, epochs=34) → 1.3857
- (BERT-base, Adam, fedprox, lr=0.000031, batch=64, epochs=1, mu=0.2) → 0.7651
- (ResNet50, Adam, fedavg, lr=0.138020, batch=64, epochs=34) → 1.4106
- (ResNet101, RMSprop, fedavg, lr=0.082516, batch=128, epochs=42) → 0.6188
- (LeNet5, SGD, fedadam, lr=0.006774, batch=64, epochs=20) → 1.3566
- (GPT-like, Adam, fedprox, lr=0.000128, batch=32, epochs=3, mu=0.2) → 0.6312
- (LSTM-2, SGD, fedadam, lr=0.001435, batch=64, epochs=24) → 0.6335
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)