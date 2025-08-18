## Q19. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (LeNet5, Adam, fedavg, lr=0.005684, batch=256, epochs=20) → 3.8344
- (ResNet101, SGD, fedavg, lr=0.049579, batch=64, epochs=44) → 1.4671
- (GPT-like, AdamW, fedadam, lr=0.000148, batch=16, epochs=1) → 0.5222
- (LSTM-2, AdamW, fedprox, lr=0.001415, batch=128, epochs=24, mu=0.1) → 1.4803
- (ResNet18, SGD, fedavg, lr=0.118841, batch=64, epochs=30) → 1.3594
- (ResNet50, Adam, fedavg, lr=0.077019, batch=64, epochs=34) → 1.4067
- (BERT-base, RMSprop, fedadam, lr=0.000040, batch=16, epochs=5) → 0.5853
- (LSTM-2, Adam, fedadam, lr=0.000954, batch=32, epochs=18) → 0.8314
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)