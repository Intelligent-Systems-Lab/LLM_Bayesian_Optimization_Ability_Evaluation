# 24 Architecture-Aware BO/HPO Questions (with Step-by-Step Answers) — v3
This pack adds **neural architecture** (e.g., LeNet5, ResNet*, LSTM, BERT, GPT-like) as a categorical variable and ties it to
typical optimizer/regularization preferences.

- **Q1–Q12 (GP)**: Architecture and optimizer are **fixed** per item, search space has only **continuous** dims: lr (log-real), weight_decay, dropout.

- **Q13–Q24 (TPE)**: Architecture, optimizer, and FL aggregator are **categorical**; continuous dims include lr, batch, epochs (and mu if fedprox).

Objective: **minimize** validation loss.

---
## Q1. GP (continuous) — Architecture=LeNet5, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.002500, wd=0.00000, drop=0.10 → y=0.5438
- lr=0.005000, wd=0.00010, drop=0.20 → y=0.4980
- lr=0.010000, wd=0.00510, drop=0.30 → y=0.5454
**Candidates** (evaluate EI):
- lr=0.004000, wd=0.00000, drop=0.15
- lr=0.006000, wd=0.00210, drop=0.25
- lr=0.008000, wd=0.00610, drop=0.35
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8806, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.0122, -1.0825, 1.0146]; f*=0.4980
3) EI on candidates:
   - lr=0.004000, wd=0.00000, drop=0.15: μ=0.5056, σ=0.0622, z=-0.123, EI=0.02118
   - lr=0.006000, wd=0.00210, drop=0.25: μ=0.5038, σ=0.0677, z=-0.085, EI=0.02422
   - lr=0.008000, wd=0.00610, drop=0.35: μ=0.5234, σ=0.1787, z=-0.142, EI=0.05930
4) **Recommend** the argmax-EI candidate.
---
## Q2. GP (continuous) — Architecture=ResNet18, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.050000, wd=0.00000, drop=0.10 → y=0.5478
- lr=0.100000, wd=0.00010, drop=0.20 → y=0.5020
- lr=0.200000, wd=0.00510, drop=0.30 → y=0.5494
**Candidates** (evaluate EI):
- lr=0.080000, wd=0.00000, drop=0.15
- lr=0.120000, wd=0.00210, drop=0.25
- lr=0.160000, wd=0.00610, drop=0.35
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8806, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.018, -1.0874, 1.0203]; f*=0.5020
3) EI on candidates:
   - lr=0.080000, wd=0.00000, drop=0.15: μ=0.5096, σ=0.0622, z=-0.123, EI=0.02117
   - lr=0.120000, wd=0.00210, drop=0.25: μ=0.5078, σ=0.0677, z=-0.085, EI=0.02422
   - lr=0.160000, wd=0.00610, drop=0.35: μ=0.5274, σ=0.1787, z=-0.142, EI=0.05932
4) **Recommend** the argmax-EI candidate.
---
## Q3. GP (continuous) — Architecture=ResNet50, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.050000, wd=0.00000, drop=0.10 → y=0.5442
- lr=0.100000, wd=0.00010, drop=0.20 → y=0.4984
- lr=0.200000, wd=0.00510, drop=0.30 → y=0.5458
**Candidates** (evaluate EI):
- lr=0.080000, wd=0.00000, drop=0.15
- lr=0.120000, wd=0.00210, drop=0.25
- lr=0.160000, wd=0.00610, drop=0.35
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8806, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.0128, -1.083, 1.0152]; f*=0.4984
3) EI on candidates:
   - lr=0.080000, wd=0.00000, drop=0.15: μ=0.5060, σ=0.0622, z=-0.123, EI=0.02118
   - lr=0.120000, wd=0.00210, drop=0.25: μ=0.5042, σ=0.0677, z=-0.085, EI=0.02422
   - lr=0.160000, wd=0.00610, drop=0.35: μ=0.5238, σ=0.1787, z=-0.142, EI=0.05930
4) **Recommend** the argmax-EI candidate.
---
## Q4. GP (continuous) — Architecture=ResNet101, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.050000, wd=0.00000, drop=0.20 → y=0.5482
- lr=0.100000, wd=0.00010, drop=0.30 → y=0.5024
- lr=0.200000, wd=0.00510, drop=0.40 → y=0.5498
**Candidates** (evaluate EI):
- lr=0.080000, wd=0.00000, drop=0.25
- lr=0.120000, wd=0.00210, drop=0.35
- lr=0.160000, wd=0.00610, drop=0.45
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8806, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.0185, -1.0879, 1.0209]; f*=0.5024
3) EI on candidates:
   - lr=0.080000, wd=0.00000, drop=0.25: μ=0.5100, σ=0.0622, z=-0.123, EI=0.02117
   - lr=0.120000, wd=0.00210, drop=0.35: μ=0.5082, σ=0.0677, z=-0.085, EI=0.02422
   - lr=0.160000, wd=0.00610, drop=0.45: μ=0.5278, σ=0.1787, z=-0.142, EI=0.05932
4) **Recommend** the argmax-EI candidate.
---
## Q5. GP (continuous) — Architecture=LSTM-2, Optimizer=Adam
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.001000, wd=0.00000, drop=0.20 → y=0.5446
- lr=0.002000, wd=0.00000, drop=0.30 → y=0.4988
- lr=0.004000, wd=0.00500, drop=0.40 → y=0.5462
**Candidates** (evaluate EI):
- lr=0.001600, wd=0.00000, drop=0.25
- lr=0.002400, wd=0.00200, drop=0.35
- lr=0.003200, wd=0.00600, drop=0.45
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8805, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.0134, -1.0835, 1.0158]; f*=0.4988
3) EI on candidates:
   - lr=0.001600, wd=0.00000, drop=0.25: μ=0.5064, σ=0.0622, z=-0.123, EI=0.02118
   - lr=0.002400, wd=0.00200, drop=0.35: μ=0.5046, σ=0.0677, z=-0.085, EI=0.02422
   - lr=0.003200, wd=0.00600, drop=0.45: μ=0.5242, σ=0.1787, z=-0.142, EI=0.05931
4) **Recommend** the argmax-EI candidate.
---
## Q6. GP (continuous) — Architecture=BERT-base, Optimizer=AdamW
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.000015, wd=0.00500, drop=0.00 → y=0.5494
- lr=0.000030, wd=0.01000, drop=0.10 → y=0.5028
- lr=0.000060, wd=0.01500, drop=0.20 → y=0.5502
**Candidates** (evaluate EI):
- lr=0.000024, wd=0.00700, drop=0.05
- lr=0.000036, wd=0.01200, drop=0.15
- lr=0.000048, wd=0.01600, drop=0.25
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3701], [0.78, 1.0004, 0.78], [0.3701, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0342, -5.0536, 2.4477], [-5.0536, 8.8797, -5.0536], [2.4477, -5.0536, 4.0342]]
   - α = K⁻¹y: [1.0221, -1.0922, 1.0234]; f*=0.5028
3) EI on candidates:
   - lr=0.000024, wd=0.00700, drop=0.05: μ=0.5106, σ=0.0622, z=-0.126, EI=0.02111
   - lr=0.000036, wd=0.01200, drop=0.15: μ=0.5085, σ=0.0677, z=-0.084, EI=0.02426
   - lr=0.000048, wd=0.01600, drop=0.25: μ=0.5280, σ=0.1787, z=-0.141, EI=0.05936
4) **Recommend** the argmax-EI candidate.
---
## Q7. GP (continuous) — Architecture=GPT-like, Optimizer=AdamW
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.000100, wd=0.01500, drop=0.00 → y=0.5458
- lr=0.000200, wd=0.02000, drop=0.10 → y=0.4992
- lr=0.000400, wd=0.02500, drop=0.20 → y=0.5466
**Candidates** (evaluate EI):
- lr=0.000160, wd=0.01700, drop=0.05
- lr=0.000240, wd=0.02200, drop=0.15
- lr=0.000320, wd=0.02600, drop=0.25
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3701], [0.78, 1.0004, 0.78], [0.3701, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0342, -5.0536, 2.4477], [-5.0536, 8.8797, -5.0536], [2.4477, -5.0536, 4.0342]]
   - α = K⁻¹y: [1.017, -1.0878, 1.0182]; f*=0.4992
3) EI on candidates:
   - lr=0.000160, wd=0.01700, drop=0.05: μ=0.5070, σ=0.0622, z=-0.126, EI=0.02111
   - lr=0.000240, wd=0.02200, drop=0.15: μ=0.5049, σ=0.0677, z=-0.084, EI=0.02426
   - lr=0.000320, wd=0.02600, drop=0.25: μ=0.5245, σ=0.1787, z=-0.141, EI=0.05935
4) **Recommend** the argmax-EI candidate.
---
## Q8. GP (continuous) — Architecture=ResNet18, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.050000, wd=0.00000, drop=0.10 → y=0.5490
- lr=0.100000, wd=0.00010, drop=0.20 → y=0.5032
- lr=0.200000, wd=0.00510, drop=0.30 → y=0.5506
**Candidates** (evaluate EI):
- lr=0.080000, wd=0.00000, drop=0.15
- lr=0.120000, wd=0.00210, drop=0.25
- lr=0.160000, wd=0.00610, drop=0.35
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8806, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.0197, -1.0889, 1.022]; f*=0.5032
3) EI on candidates:
   - lr=0.080000, wd=0.00000, drop=0.15: μ=0.5108, σ=0.0622, z=-0.123, EI=0.02117
   - lr=0.120000, wd=0.00210, drop=0.25: μ=0.5090, σ=0.0677, z=-0.085, EI=0.02422
   - lr=0.160000, wd=0.00610, drop=0.35: μ=0.5285, σ=0.1787, z=-0.142, EI=0.05932
4) **Recommend** the argmax-EI candidate.
---
## Q9. GP (continuous) — Architecture=ResNet50, Optimizer=SGD
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.050000, wd=0.00000, drop=0.10 → y=0.5454
- lr=0.100000, wd=0.00010, drop=0.20 → y=0.4996
- lr=0.200000, wd=0.00510, drop=0.30 → y=0.5470
**Candidates** (evaluate EI):
- lr=0.080000, wd=0.00000, drop=0.15
- lr=0.120000, wd=0.00210, drop=0.25
- lr=0.160000, wd=0.00610, drop=0.35
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8806, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.0145, -1.0845, 1.0169]; f*=0.4996
3) EI on candidates:
   - lr=0.080000, wd=0.00000, drop=0.15: μ=0.5072, σ=0.0622, z=-0.123, EI=0.02118
   - lr=0.120000, wd=0.00210, drop=0.25: μ=0.5054, σ=0.0677, z=-0.085, EI=0.02422
   - lr=0.160000, wd=0.00610, drop=0.35: μ=0.5250, σ=0.1787, z=-0.142, EI=0.05931
4) **Recommend** the argmax-EI candidate.
---
## Q10. GP (continuous) — Architecture=LSTM-2, Optimizer=Adam
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.001000, wd=0.00000, drop=0.20 → y=0.5494
- lr=0.002000, wd=0.00000, drop=0.30 → y=0.5036
- lr=0.004000, wd=0.00500, drop=0.40 → y=0.5434
**Candidates** (evaluate EI):
- lr=0.001600, wd=0.00000, drop=0.25
- lr=0.002400, wd=0.00200, drop=0.35
- lr=0.003200, wd=0.00600, drop=0.45
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3702], [0.78, 1.0004, 0.78], [0.3702, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0348, -5.0543, 2.4477], [-5.0543, 8.8805, -5.0536], [2.4477, -5.0536, 4.034]]
   - α = K⁻¹y: [1.0016, -1.051, 0.992]; f*=0.5036
3) EI on candidates:
   - lr=0.001600, wd=0.00000, drop=0.25: μ=0.5122, σ=0.0622, z=-0.139, EI=0.02072
   - lr=0.002400, wd=0.00200, drop=0.35: μ=0.5077, σ=0.0677, z=-0.060, EI=0.02503
   - lr=0.003200, wd=0.00600, drop=0.45: μ=0.5235, σ=0.1787, z=-0.111, EI=0.06179
4) **Recommend** the argmax-EI candidate.
---
## Q11. GP (continuous) — Architecture=BERT-base, Optimizer=AdamW
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.000015, wd=0.00500, drop=0.00 → y=0.5466
- lr=0.000030, wd=0.01000, drop=0.10 → y=0.5000
- lr=0.000060, wd=0.01500, drop=0.20 → y=0.5474
**Candidates** (evaluate EI):
- lr=0.000024, wd=0.00700, drop=0.05
- lr=0.000036, wd=0.01200, drop=0.15
- lr=0.000048, wd=0.01600, drop=0.25
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3701], [0.78, 1.0004, 0.78], [0.3701, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0342, -5.0536, 2.4477], [-5.0536, 8.8797, -5.0536], [2.4477, -5.0536, 4.0342]]
   - α = K⁻¹y: [1.0181, -1.0887, 1.0194]; f*=0.5000
3) EI on candidates:
   - lr=0.000024, wd=0.00700, drop=0.05: μ=0.5078, σ=0.0622, z=-0.126, EI=0.02111
   - lr=0.000036, wd=0.01200, drop=0.15: μ=0.5057, σ=0.0677, z=-0.084, EI=0.02426
   - lr=0.000048, wd=0.01600, drop=0.25: μ=0.5253, σ=0.1787, z=-0.141, EI=0.05935
4) **Recommend** the argmax-EI candidate.
---
## Q12. GP (continuous) — Architecture=GPT-like, Optimizer=AdamW
**Search space**: lr (log-real), weight_decay, dropout. Architecture & optimizer fixed.
**Observed trials** (loss):
- lr=0.000100, wd=0.01500, drop=0.00 → y=0.5506
- lr=0.000200, wd=0.02000, drop=0.10 → y=0.4964
- lr=0.000400, wd=0.02500, drop=0.20 → y=0.5438
**Candidates** (evaluate EI):
- lr=0.000160, wd=0.01700, drop=0.05
- lr=0.000240, wd=0.02200, drop=0.15
- lr=0.000320, wd=0.02600, drop=0.25
**Answer (steps):**
1) All dims are continuous ⇒ **GP**.
2) Fit GP on inputs `[log10(lr), wd, dropout]` with RBF kernel (ℓ=0.45, σ_f²=1, σ_n²=0.02).
   - K (rounded): [[1.0004, 0.78, 0.3701], [0.78, 1.0004, 0.78], [0.3701, 0.78, 1.0004]]
   - K⁻¹ (rounded): [[4.0342, -5.0536, 2.4477], [-5.0536, 8.8797, -5.0536], [2.4477, -5.0536, 4.0342]]
   - α = K⁻¹y: [1.0436, -1.1227, 1.0328]; f*=0.4964
3) EI on candidates:
   - lr=0.000160, wd=0.01700, drop=0.05: μ=0.5063, σ=0.0622, z=-0.159, EI=0.02019
   - lr=0.000240, wd=0.02200, drop=0.15: μ=0.5011, σ=0.0677, z=-0.070, EI=0.02470
   - lr=0.000320, wd=0.02600, drop=0.25: μ=0.5210, σ=0.1787, z=-0.138, EI=0.05966
4) **Recommend** the argmax-EI candidate.
---
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
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
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
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
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
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
## Q16. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (GPT-like, Adam, fedadam, lr=0.000099, batch=16, epochs=3) → 0.5673
- (LSTM-2, Adam, fedprox, lr=0.002845, batch=64, epochs=18, mu=0.0) → 0.6238
- (ResNet101, RMSprop, fedavg, lr=0.137087, batch=64, epochs=42) → 1.4415
- (ResNet18, SGD, fedavg, lr=0.246967, batch=128, epochs=30) → 0.6009
- (BERT-base, RMSprop, fedprox, lr=0.000049, batch=64, epochs=3, mu=0.0) → 0.7753
- (LeNet5, SGD, fedprox, lr=0.007054, batch=128, epochs=22, mu=0.1) → 0.5754
- (ResNet50, RMSprop, fedavg, lr=0.203583, batch=256, epochs=34) → 3.8993
- (LSTM-2, AdamW, fedprox, lr=0.000994, batch=64, epochs=18, mu=0.1) → 0.6742
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
## Q17. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (LSTM-2, SGD, fedadam, lr=0.001961, batch=64, epochs=20) → 0.6000
- (GPT-like, RMSprop, fedadam, lr=0.000142, batch=8, epochs=7) → 0.5780
- (BERT-base, SGD, fedprox, lr=0.000028, batch=64, epochs=7, mu=0.2) → 0.7849
- (LeNet5, AdamW, fedprox, lr=0.008077, batch=64, epochs=18, mu=0.2) → 1.4258
- (ResNet18, AdamW, fedprox, lr=0.063303, batch=128, epochs=34, mu=0.0) → 0.6214
- (ResNet101, RMSprop, fedadam, lr=0.219661, batch=64, epochs=40) → 1.4679
- (ResNet50, SGD, fedavg, lr=0.073407, batch=64, epochs=30) → 1.3688
- (LeNet5, Adam, fedprox, lr=0.004635, batch=256, epochs=22, mu=0.0) → 3.8660
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
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
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
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
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
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
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
## Q21. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet50, Adam, fedprox, lr=0.126951, batch=128, epochs=28, mu=0.05) → 0.5908
- (ResNet101, SGD, fedprox, lr=0.076832, batch=64, epochs=42, mu=0.2) → 1.4432
- (LeNet5, SGD, fedprox, lr=0.002867, batch=64, epochs=24, mu=0.1) → 1.4282
- (BERT-base, Adam, fedavg, lr=0.000018, batch=32, epochs=1) → 0.5614
- (ResNet18, AdamW, fedadam, lr=0.122719, batch=256, epochs=32) → 3.8380
- (GPT-like, RMSprop, fedavg, lr=0.000150, batch=16, epochs=1) → 0.5567
- (LSTM-2, AdamW, fedavg, lr=0.001756, batch=32, epochs=18) → 0.8249
- (ResNet18, AdamW, fedadam, lr=0.198230, batch=128, epochs=28) → 0.5945
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
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
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
## Q23. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet101, RMSprop, fedadam, lr=0.082056, batch=64, epochs=40) → 1.4190
- (GPT-like, SGD, fedavg, lr=0.000312, batch=16, epochs=7) → 0.5781
- (ResNet18, Adam, fedadam, lr=0.169218, batch=128, epochs=30) → 0.5685
- (BERT-base, SGD, fedadam, lr=0.000044, batch=32, epochs=1) → 0.5384
- (LeNet5, RMSprop, fedadam, lr=0.005311, batch=64, epochs=24) → 1.3919
- (LSTM-2, SGD, fedadam, lr=0.001644, batch=64, epochs=22) → 0.6077
- (ResNet50, RMSprop, fedprox, lr=0.044721, batch=64, epochs=30, mu=0.2) → 1.4493
- (GPT-like, AdamW, fedavg, lr=0.000252, batch=16, epochs=7) → 0.5496
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
## Q24. TPE (categorical+continuous) — Architecture-aware
**Search space**: architecture ∈ {LeNet5, ResNet18, ResNet50, ResNet101, LSTM-2, BERT-base, GPT-like}, optimizer ∈ {SGD, Adam, AdamW, RMSprop}, fed_agg ∈ {fedavg, fedadam, fedprox}, and continuous {lr, batch, epochs} (+ mu if fedprox).
**Observed trials** (loss):
- (ResNet50, SGD, fedadam, lr=0.074337, batch=64, epochs=28) → 1.3606
- (LeNet5, AdamW, fedadam, lr=0.005792, batch=64, epochs=18) → 1.3760
- (ResNet18, Adam, fedadam, lr=0.242697, batch=64, epochs=30) → 1.4281
- (ResNet101, AdamW, fedadam, lr=0.119079, batch=64, epochs=44) → 1.4455
- (GPT-like, RMSprop, fedprox, lr=0.000301, batch=32, epochs=1, mu=0.05) → 0.6322
- (BERT-base, SGD, fedavg, lr=0.000047, batch=32, epochs=3) → 0.5486
- (LSTM-2, RMSprop, fedavg, lr=0.004522, batch=128, epochs=22) → 1.4866
- (GPT-like, AdamW, fedadam, lr=0.000188, batch=16, epochs=3) → 0.5139
**Candidates**:
- (ResNet18, SGD, fedavg, lr=0.100000, batch=128, epochs=30)
- (ResNet50, SGD, fedadam, lr=0.080000, batch=128, epochs=30)
- (LSTM-2, Adam, fedavg, lr=0.002000, batch=64, epochs=20)
- (BERT-base, AdamW, fedadam, lr=0.000030, batch=32, epochs=3)
- (GPT-like, AdamW, fedprox, lr=0.000200, batch=16, epochs=3, mu=0.05)
- (LeNet5, SGD, fedavg, lr=0.005000, batch=128, epochs=20)
**Answer (steps):**
1) Categorical variables present ⇒ **TPE**.
2) Split by γ=0.33 into **good**/**bad** sets (lower loss is better).
3) Build l(x) from **good** and g(x) from **bad** using: Laplace-smoothed masses for {architecture, optimizer, fed_agg}, and KDEs for {lr, batch, epochs} (+ mu for fedprox).
4) Compute l/g per candidate and pick **argmax**.
---
