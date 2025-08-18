## Q28. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.435  
- x₂=0.50 → y₂=0.790  
- x₃=0.90 → y₃=0.614  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?