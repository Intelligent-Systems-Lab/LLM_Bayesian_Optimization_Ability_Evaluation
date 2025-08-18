# 100 BO/HPO Process Understanding Questions (with Step-by-Step Answers): Part 2/13 - Problems 9 to 16
These questions are designed to probe whether a pre-trained LLM truly understands how a *real* Bayesian Optimization (BO) HPO engine works (both GP-based and TPE-based).
Each item is a miniature, fully worked example requiring the model to:
- Decide **GP vs TPE** based on the presence of categorical variables.
- For **GP**: fit a Gaussian Process on observed trials, compute posterior mean/variance, and **Expected Improvement (EI)**; propose the next point by **argmax EI**.
- For **TPE**: split observations into good/bad by a quantile **γ**, fit **l(x)** and **g(x)** (KDE for continuous, Laplace-smoothed masses for categorical), evaluate **l/g** for candidates; propose the next point by **argmax l/g**.

**Conventions**
- Objective: *minimize* validation loss.
- GP kernel: RBF with lengthscale **ℓ=0.30**, signal variance **σ_f²=1**, observation noise **σ_n²=0.01**.
- EI (minimization): EI(x) = (f\* − μ(x)) Φ(z) + σ(x) φ(z), where z=(f\*−μ)/σ.
- TPE: γ=0.33 (unless stated), bandwidth h=0.10 for KDE, Laplace α=1.0 for categorical.
- All numbers are rounded for readability (typically 3 decimals).

---
## Q9. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.447  
- x₂=0.50 → y₂=0.780  
- x₃=0.90 → y₃=0.626  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2207, 0.5229, 0.4046]
   - Current best f* (min observed y): 0.447
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.552, σ=0.207, z=-0.508, Φ(z)=0.306, φ(z)=0.351, **EI=0.0405**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.795, σ=0.188, z=-1.852, Φ(z)=0.032, φ(z)=0.072, **EI=0.0023**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.714, σ=0.207, z=-1.289, Φ(z)=0.099, φ(z)=0.174, **EI=0.0097**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q10. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.451  
- x₂=0.50 → y₂=0.784  
- x₃=0.90 → y₃=0.608  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2195, 0.5372, 0.3808]
   - Current best f* (min observed y): 0.451
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.558, σ=0.207, z=-0.517, Φ(z)=0.302, φ(z)=0.349, **EI=0.0399**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.794, σ=0.188, z=-1.824, Φ(z)=0.034, φ(z)=0.076, **EI=0.0025**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.700, σ=0.207, z=-1.203, Φ(z)=0.115, φ(z)=0.194, **EI=0.0116**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q11. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.433  
- x₂=0.50 → y₂=0.788  
- x₃=0.90 → y₃=0.612  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.1956, 0.5514, 0.3796]
   - Current best f* (min observed y): 0.433
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.544, σ=0.207, z=-0.537, Φ(z)=0.296, φ(z)=0.345, **EI=0.0387**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.801, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.706, σ=0.207, z=-1.318, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q12. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.437  
- x₂=0.50 → y₂=0.792  
- x₃=0.90 → y₃=0.616  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.199, 0.5526, 0.383]
   - Current best f* (min observed y): 0.437
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.549, σ=0.207, z=-0.538, Φ(z)=0.295, φ(z)=0.345, **EI=0.0386**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.805, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.711, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q13. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.441  
- x₂=0.50 → y₂=0.774  
- x₃=0.90 → y₃=0.620  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2156, 0.5211, 0.3995]
   - Current best f* (min observed y): 0.441
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.546, σ=0.207, z=-0.507, Φ(z)=0.306, φ(z)=0.351, **EI=0.0406**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.789, σ=0.188, z=-1.852, Φ(z)=0.032, φ(z)=0.072, **EI=0.0024**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.708, σ=0.207, z=-1.288, Φ(z)=0.099, φ(z)=0.174, **EI=0.0097**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q14. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.445  
- x₂=0.50 → y₂=0.778  
- x₃=0.90 → y₃=0.624  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.219, 0.5223, 0.4029]
   - Current best f* (min observed y): 0.445
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.550, σ=0.207, z=-0.507, Φ(z)=0.306, φ(z)=0.351, **EI=0.0405**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.793, σ=0.188, z=-1.852, Φ(z)=0.032, φ(z)=0.072, **EI=0.0023**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.712, σ=0.207, z=-1.289, Φ(z)=0.099, φ(z)=0.174, **EI=0.0097**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q15. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.449  
- x₂=0.50 → y₂=0.782  
- x₃=0.90 → y₃=0.606  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2178, 0.5366, 0.3791]
   - Current best f* (min observed y): 0.449
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.556, σ=0.207, z=-0.517, Φ(z)=0.303, φ(z)=0.349, **EI=0.0399**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.792, σ=0.188, z=-1.824, Φ(z)=0.034, φ(z)=0.076, **EI=0.0025**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.698, σ=0.207, z=-1.202, Φ(z)=0.115, φ(z)=0.194, **EI=0.0116**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q16. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.453  
- x₂=0.50 → y₂=0.786  
- x₃=0.90 → y₃=0.610  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2212, 0.5378, 0.3825]
   - Current best f* (min observed y): 0.453
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.561, σ=0.207, z=-0.518, Φ(z)=0.302, φ(z)=0.349, **EI=0.0399**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.796, σ=0.188, z=-1.825, Φ(z)=0.034, φ(z)=0.076, **EI=0.0025**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.703, σ=0.207, z=-1.203, Φ(z)=0.114, φ(z)=0.193, **EI=0.0116**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.
