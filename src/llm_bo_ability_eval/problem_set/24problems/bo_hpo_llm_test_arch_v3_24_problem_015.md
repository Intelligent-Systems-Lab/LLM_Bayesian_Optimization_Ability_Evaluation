## Q15. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet50, RMSprop, fedprox, lr=0.043371, batch=256, epochs=34, mu=0.05) → 3.9372
- (GPT-like, Adam, fedavg, lr=0.000440, batch=8, epochs=5) → 0.6042
- (ResNet101, RMSprop, fedprox, lr=0.040219, batch=64, epochs=38, mu=0.2) → 1.5166
- (LSTM-2, RMSprop, fedavg, lr=0.001282, batch=32, epochs=24) → 0.8509
- (ResNet18, SGD, fedadam, lr=0.075565, batch=64, epochs=32) → 1.3587
- (BERT-base, RMSprop, fedadam, lr=0.000052, batch=32, epochs=5) → 0.5502
- (LeNet5, RMSprop, fedprox, lr=0.005270, batch=128, epochs=24, mu=0.05) → 0.6027
- (ResNet50, RMSprop, fedavg, lr=0.211698, batch=128, epochs=32) → 0.6072
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)