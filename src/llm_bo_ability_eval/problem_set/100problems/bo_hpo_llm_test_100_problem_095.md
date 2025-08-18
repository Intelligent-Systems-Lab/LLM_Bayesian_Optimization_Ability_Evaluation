## Q95. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.36) → loss=0.607
- (RMSprop, lr=0.50) → loss=0.663
- (SGD, lr=0.42) → loss=0.798
- (RMSprop, lr=0.18) → loss=0.685
- (Adam, lr=0.30) → loss=0.591
- (Adam, lr=0.24) → loss=0.600
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?