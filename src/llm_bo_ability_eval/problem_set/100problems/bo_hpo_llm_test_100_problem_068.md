## Q68. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.42) → loss=0.604
- (SGD, lr=0.50) → loss=0.811
- (SGD, lr=0.30) → loss=0.813
- (Adam, lr=0.24) → loss=0.596
- (Adam, lr=0.36) → loss=0.611
- (SGD, lr=0.18) → loss=0.802
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?