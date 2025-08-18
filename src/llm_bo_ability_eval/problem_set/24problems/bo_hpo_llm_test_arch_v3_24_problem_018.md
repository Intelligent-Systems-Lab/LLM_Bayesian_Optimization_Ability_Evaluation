## Q18. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet18, Adam, fedavg, lr=0.167415, batch=64, epochs=30) → 1.4012
- (BERT-base, RMSprop, fedprox, lr=0.000038, batch=64, epochs=7, mu=0.2) → 0.7907
- (ResNet101, SGD, fedadam, lr=0.075913, batch=256, epochs=40) → 3.8653
- (ResNet50, AdamW, fedprox, lr=0.128726, batch=256, epochs=28, mu=0.0) → 3.8708
- (LSTM-2, Adam, fedadam, lr=0.001293, batch=64, epochs=22) → 0.6040
- (GPT-like, RMSprop, fedprox, lr=0.000130, batch=32, epochs=7, mu=0.0) → 0.6474
- (LeNet5, AdamW, fedavg, lr=0.006962, batch=256, epochs=20) → 3.8419
- (ResNet50, AdamW, fedprox, lr=0.195794, batch=64, epochs=34, mu=0.2) → 1.4565
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)