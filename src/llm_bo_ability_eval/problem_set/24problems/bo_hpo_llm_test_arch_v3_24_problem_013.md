## Q13. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (LSTM-2, SGD, fedavg, lr=0.002426, batch=128, epochs=18) → 1.4376
- (GPT-like, RMSprop, fedadam, lr=0.000406, batch=16, epochs=3) → 0.5698
- (ResNet18, RMSprop, fedavg, lr=0.045699, batch=256, epochs=34) → 3.9075
- (ResNet101, AdamW, fedavg, lr=0.114719, batch=128, epochs=38) → 0.6182
- (BERT-base, Adam, fedadam, lr=0.000069, batch=64, epochs=1) → 0.7872
- (ResNet50, Adam, fedavg, lr=0.061145, batch=128, epochs=34) → 0.6039
- (LeNet5, Adam, fedadam, lr=0.010010, batch=64, epochs=20) → 1.4075
- (ResNet101, RMSprop, fedadam, lr=0.219924, batch=256, epochs=42) → 3.9321
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)