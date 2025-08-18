## Q22. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet50, Adam, fedavg, lr=0.069735, batch=256, epochs=30) → 3.8490
- (BERT-base, Adam, fedprox, lr=0.000063, batch=64, epochs=1, mu=0.1) → 0.8085
- (GPT-like, RMSprop, fedavg, lr=0.000306, batch=8, epochs=1) → 0.5776
- (LSTM-2, Adam, fedavg, lr=0.003450, batch=32, epochs=20) → 0.8208
- (ResNet101, Adam, fedprox, lr=0.098091, batch=128, epochs=38, mu=0.1) → 0.6329
- (ResNet18, AdamW, fedadam, lr=0.060351, batch=256, epochs=30) → 3.8428
- (LeNet5, SGD, fedavg, lr=0.002331, batch=64, epochs=22) → 1.4063
- (ResNet18, SGD, fedavg, lr=0.075323, batch=64, epochs=32) → 1.3689
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)