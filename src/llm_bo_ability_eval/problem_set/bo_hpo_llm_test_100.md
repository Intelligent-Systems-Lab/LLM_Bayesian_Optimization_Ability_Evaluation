# 100 BO/HPO Process Understanding Questions (with Step-by-Step Answers)
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
## Q1. GP-based BO — propose next learning rate
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
## Q2. GP-based BO — propose next learning rate
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
## Q3. GP-based BO — propose next learning rate
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
## Q4. GP-based BO — propose next learning rate
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
## Q5. GP-based BO — propose next learning rate
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

---
## Q6. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.435  
- x₂=0.50 → y₂=0.790  
- x₃=0.90 → y₃=0.614  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.1973, 0.552, 0.3813]
   - Current best f* (min observed y): 0.435
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.547, σ=0.207, z=-0.537, Φ(z)=0.296, φ(z)=0.345, **EI=0.0387**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.803, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.709, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q7. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.439  
- x₂=0.50 → y₂=0.794  
- x₃=0.90 → y₃=0.618  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2008, 0.5532, 0.3847]
   - Current best f* (min observed y): 0.439
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.551, σ=0.207, z=-0.538, Φ(z)=0.295, φ(z)=0.345, **EI=0.0386**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.807, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.713, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q8. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.443  
- x₂=0.50 → y₂=0.776  
- x₃=0.90 → y₃=0.622  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2173, 0.5217, 0.4012]
   - Current best f* (min observed y): 0.443
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.548, σ=0.207, z=-0.507, Φ(z)=0.306, φ(z)=0.351, **EI=0.0406**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.791, σ=0.188, z=-1.852, Φ(z)=0.032, φ(z)=0.072, **EI=0.0023**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.710, σ=0.207, z=-1.288, Φ(z)=0.099, φ(z)=0.174, **EI=0.0097**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

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

---
## Q17. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.435  
- x₂=0.50 → y₂=0.790  
- x₃=0.90 → y₃=0.614  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.1973, 0.552, 0.3813]
   - Current best f* (min observed y): 0.435
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.547, σ=0.207, z=-0.537, Φ(z)=0.296, φ(z)=0.345, **EI=0.0387**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.803, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.709, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q18. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.439  
- x₂=0.50 → y₂=0.794  
- x₃=0.90 → y₃=0.618  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2008, 0.5532, 0.3847]
   - Current best f* (min observed y): 0.439
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.551, σ=0.207, z=-0.538, Φ(z)=0.295, φ(z)=0.345, **EI=0.0386**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.807, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.713, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q19. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.443  
- x₂=0.50 → y₂=0.776  
- x₃=0.90 → y₃=0.622  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2173, 0.5217, 0.4012]
   - Current best f* (min observed y): 0.443
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.548, σ=0.207, z=-0.507, Φ(z)=0.306, φ(z)=0.351, **EI=0.0406**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.791, σ=0.188, z=-1.852, Φ(z)=0.032, φ(z)=0.072, **EI=0.0023**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.710, σ=0.207, z=-1.288, Φ(z)=0.099, φ(z)=0.174, **EI=0.0097**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q20. GP-based BO — propose next learning rate
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
## Q21. GP-based BO — propose next learning rate
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
## Q22. GP-based BO — propose next learning rate
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
## Q23. GP-based BO — propose next learning rate
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
## Q24. GP-based BO — propose next learning rate
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
## Q25. GP-based BO — propose next learning rate
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
## Q26. GP-based BO — propose next learning rate
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
## Q27. GP-based BO — propose next learning rate
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

---
## Q28. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.435  
- x₂=0.50 → y₂=0.790  
- x₃=0.90 → y₃=0.614  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.1973, 0.552, 0.3813]
   - Current best f* (min observed y): 0.435
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.547, σ=0.207, z=-0.537, Φ(z)=0.296, φ(z)=0.345, **EI=0.0387**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.803, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.709, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q29. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.439  
- x₂=0.50 → y₂=0.794  
- x₃=0.90 → y₃=0.618  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2008, 0.5532, 0.3847]
   - Current best f* (min observed y): 0.439
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.551, σ=0.207, z=-0.538, Φ(z)=0.295, φ(z)=0.345, **EI=0.0386**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.807, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.713, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q30. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.443  
- x₂=0.50 → y₂=0.776  
- x₃=0.90 → y₃=0.622  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2173, 0.5217, 0.4012]
   - Current best f* (min observed y): 0.443
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.548, σ=0.207, z=-0.507, Φ(z)=0.306, φ(z)=0.351, **EI=0.0406**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.791, σ=0.188, z=-1.852, Φ(z)=0.032, φ(z)=0.072, **EI=0.0023**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.710, σ=0.207, z=-1.288, Φ(z)=0.099, φ(z)=0.174, **EI=0.0097**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q31. GP-based BO — propose next learning rate
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
## Q32. GP-based BO — propose next learning rate
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
## Q33. GP-based BO — propose next learning rate
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
## Q34. GP-based BO — propose next learning rate
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
## Q35. GP-based BO — propose next learning rate
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
## Q36. GP-based BO — propose next learning rate
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
## Q37. GP-based BO — propose next learning rate
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
## Q38. GP-based BO — propose next learning rate
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

---
## Q39. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.435  
- x₂=0.50 → y₂=0.790  
- x₃=0.90 → y₃=0.614  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.1973, 0.552, 0.3813]
   - Current best f* (min observed y): 0.435
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.547, σ=0.207, z=-0.537, Φ(z)=0.296, φ(z)=0.345, **EI=0.0387**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.803, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.709, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q40. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.439  
- x₂=0.50 → y₂=0.794  
- x₃=0.90 → y₃=0.618  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2008, 0.5532, 0.3847]
   - Current best f* (min observed y): 0.439
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.551, σ=0.207, z=-0.538, Φ(z)=0.295, φ(z)=0.345, **EI=0.0386**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.807, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.713, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q41. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.443  
- x₂=0.50 → y₂=0.776  
- x₃=0.90 → y₃=0.622  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.2173, 0.5217, 0.4012]
   - Current best f* (min observed y): 0.443
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.548, σ=0.207, z=-0.507, Φ(z)=0.306, φ(z)=0.351, **EI=0.0406**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.791, σ=0.188, z=-1.852, Φ(z)=0.032, φ(z)=0.072, **EI=0.0023**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.710, σ=0.207, z=-1.288, Φ(z)=0.099, φ(z)=0.174, **EI=0.0097**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q42. GP-based BO — propose next learning rate
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
## Q43. GP-based BO — propose next learning rate
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
## Q44. GP-based BO — propose next learning rate
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
## Q45. GP-based BO — propose next learning rate
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
## Q46. GP-based BO — propose next learning rate
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
## Q47. GP-based BO — propose next learning rate
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
## Q48. GP-based BO — propose next learning rate
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
## Q49. GP-based BO — propose next learning rate
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

---
## Q50. GP-based BO — propose next learning rate
**Search space**: continuous learning rate `lr ∈ [0,1]` (log-scale not shown; 1D example).  
**Observed trials** (loss):  
- x₁=0.10 → y₁=0.435  
- x₂=0.50 → y₂=0.790  
- x₃=0.90 → y₃=0.614  

**Candidate set**: 0.20, 0.60, 0.80

**Ask**: Following the BO procedure with a GP surrogate and EI acquisition (minimization), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: all hyperparameters are continuous ⇒ use **Gaussian Process**.
2) **Fit GP** (RBF kernel, ℓ=0.30, σ_f²=1, σ_n²=0.01):
   - Kernel matrix K (rounded):
     [[1.0001, 0.4111, 0.0286], [0.4111, 1.0001, 0.4111], [0.0286, 0.4111, 1.0001]]
   - K⁻¹ (rounded):
     [[1.2386, -0.5952, 0.2093], [-0.5952, 1.4892, -0.5952], [0.2093, -0.5952, 1.2386]]
   - α = K⁻¹ y = [0.1973, 0.552, 0.3813]
   - Current best f* (min observed y): 0.435
3) **Evaluate EI** at candidates:
   - x=0.20: k=[0.946, 0.6065, 0.0657], μ=0.547, σ=0.207, z=-0.537, Φ(z)=0.296, φ(z)=0.345, **EI=0.0387**
   - x=0.60: k=[0.2494, 0.946, 0.6065], μ=0.803, σ=0.188, z=-1.957, Φ(z)=0.025, φ(z)=0.059, **EI=0.0018**
   - x=0.80: k=[0.0657, 0.6065, 0.946], μ=0.709, σ=0.207, z=-1.319, Φ(z)=0.094, φ(z)=0.167, **EI=0.0091**
4) **Select argmax EI** ⇒ **x=0.20**.
5) **Recommendation**: next trial `lr=0.20`.

---
## Q51. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.18) → loss=0.606
- (Adam, lr=0.30) → loss=0.589
- (Adam, lr=0.36) → loss=0.603
- (RMSprop, lr=0.24) → loss=0.676
- (SGD, lr=0.50) → loss=0.801
- (SGD, lr=0.42) → loss=0.804
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.589
     - (Adam, lr=0.36) → 0.603
   - Bad set (remaining):
     - (Adam, lr=0.18) → 0.606
     - (RMSprop, lr=0.24) → 0.676
     - (SGD, lr=0.50) → 0.801
     - (SGD, lr=0.42) → 0.804
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.352892, g(x)=0.856306, **l/g=0.412**
   - (SGD, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.203718, g(x)=0.754930, **l/g=0.270**
   - (Adam, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.058675, g(x)=0.570871, **l/g=1.854**
   - (Adam, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.611155, g(x)=0.503286, **l/g=1.214**
   - (RMSprop, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.352892, g(x)=0.570871, **l/g=0.618**
   - (RMSprop, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.203718, g(x)=0.503286, **l/g=0.405**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q52. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.36) → loss=0.641
- (Adam, lr=0.30) → loss=0.599
- (SGD, lr=0.24) → loss=0.813
- (Adam, lr=0.18) → loss=0.594
- (SGD, lr=0.50) → loss=0.811
- (SGD, lr=0.42) → loss=0.814
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.594
     - (Adam, lr=0.30) → 0.599
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.641
     - (SGD, lr=0.50) → 0.811
     - (SGD, lr=0.24) → 0.813
     - (SGD, lr=0.42) → 0.814
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.633013, g(x)=0.741568, **l/g=0.854**
   - (SGD, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.056375, g(x)=1.217063, **l/g=0.046**
   - (Adam, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.899040, g(x)=0.185392, **l/g=10.243**
   - (Adam, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.169125, g(x)=0.304266, **l/g=0.556**
   - (RMSprop, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.633013, g(x)=0.370784, **l/g=1.707**
   - (RMSprop, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.056375, g(x)=0.608532, **l/g=0.093**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q53. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.24) → loss=0.598
- (RMSprop, lr=0.42) → loss=0.658
- (SGD, lr=0.18) → loss=0.804
- (SGD, lr=0.50) → loss=0.811
- (Adam, lr=0.36) → loss=0.617
- (SGD, lr=0.30) → loss=0.797
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.598
     - (Adam, lr=0.36) → 0.617
   - Bad set (remaining):
     - (RMSprop, lr=0.42) → 0.658
     - (SGD, lr=0.30) → 0.797
     - (SGD, lr=0.18) → 0.804
     - (SGD, lr=0.50) → 0.811
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.479191, g(x)=0.961314, **l/g=0.498**
   - (SGD, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.163310, g(x)=1.064298, **l/g=0.153**
   - (Adam, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.437573, g(x)=0.240329, **l/g=5.982**
   - (Adam, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.489931, g(x)=0.266075, **l/g=1.841**
   - (RMSprop, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.479191, g(x)=0.480657, **l/g=0.997**
   - (RMSprop, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.163310, g(x)=0.532149, **l/g=0.307**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q54. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.36) → loss=0.613
- (RMSprop, lr=0.30) → loss=0.651
- (Adam, lr=0.42) → loss=0.614
- (SGD, lr=0.24) → loss=0.817
- (Adam, lr=0.18) → loss=0.598
- (SGD, lr=0.50) → loss=0.815
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.598
     - (Adam, lr=0.36) → 0.613
   - Bad set (remaining):
     - (Adam, lr=0.42) → 0.614
     - (RMSprop, lr=0.30) → 0.651
     - (SGD, lr=0.50) → 0.815
     - (SGD, lr=0.24) → 0.817
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.501964, g(x)=0.696586, **l/g=0.721**
   - (SGD, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.152112, g(x)=0.810223, **l/g=0.188**
   - (Adam, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.505891, g(x)=0.464391, **l/g=3.243**
   - (Adam, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.456335, g(x)=0.540148, **l/g=0.845**
   - (RMSprop, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.501964, g(x)=0.464391, **l/g=1.081**
   - (RMSprop, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.152112, g(x)=0.540148, **l/g=0.282**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q55. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.18) → loss=0.594
- (Adam, lr=0.30) → loss=0.603
- (SGD, lr=0.42) → loss=0.814
- (RMSprop, lr=0.36) → loss=0.649
- (RMSprop, lr=0.24) → loss=0.674
- (RMSprop, lr=0.50) → loss=0.641
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.594
     - (Adam, lr=0.30) → 0.603
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.641
     - (RMSprop, lr=0.36) → 0.649
     - (RMSprop, lr=0.24) → 0.674
     - (SGD, lr=0.42) → 0.814
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.571
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.633013, g(x)=0.370784, **l/g=1.707**
   - (SGD, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.056375, g(x)=0.608532, **l/g=0.093**
   - (Adam, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.899040, g(x)=0.185392, **l/g=10.243**
   - (Adam, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.169125, g(x)=0.304266, **l/g=0.556**
   - (RMSprop, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.633013, g(x)=0.741568, **l/g=0.854**
   - (RMSprop, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.056375, g(x)=1.217063, **l/g=0.046**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q56. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.18) → loss=0.814
- (SGD, lr=0.50) → loss=0.821
- (RMSprop, lr=0.42) → loss=0.646
- (SGD, lr=0.36) → loss=0.806
- (RMSprop, lr=0.24) → loss=0.658
- (RMSprop, lr=0.30) → loss=0.659
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (RMSprop, lr=0.42) → 0.646
     - (RMSprop, lr=0.24) → 0.658
   - Bad set (remaining):
     - (RMSprop, lr=0.30) → 0.659
     - (SGD, lr=0.36) → 0.806
     - (SGD, lr=0.18) → 0.814
     - (SGD, lr=0.50) → 0.821
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.200, P(Adam|bad)=0.143, P(RMSprop|good)=0.600, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.403745, g(x)=1.069094, **l/g=0.378**
   - (SGD, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.303275, g(x)=0.864350, **l/g=0.351**
   - (Adam, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.403745, g(x)=0.267274, **l/g=1.511**
   - (Adam, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.303275, g(x)=0.216087, **l/g=1.403**
   - (RMSprop, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.211234, g(x)=0.534547, **l/g=2.266**
   - (RMSprop, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.909824, g(x)=0.432175, **l/g=2.105**
5) **Select argmax l/g** ⇒ **(RMSprop, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="RMSprop", lr=0.20)`.

---
## Q57. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.24) → loss=0.612
- (RMSprop, lr=0.50) → loss=0.647
- (RMSprop, lr=0.18) → loss=0.685
- (SGD, lr=0.30) → loss=0.791
- (SGD, lr=0.36) → loss=0.800
- (Adam, lr=0.42) → loss=0.622
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.612
     - (Adam, lr=0.42) → 0.622
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.647
     - (RMSprop, lr=0.18) → 0.685
     - (SGD, lr=0.30) → 0.791
     - (SGD, lr=0.36) → 0.800
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.403745, g(x)=0.801821, **l/g=0.504**
   - (SGD, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.303275, g(x)=0.648262, **l/g=0.468**
   - (Adam, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.211234, g(x)=0.267274, **l/g=4.532**
   - (Adam, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.909824, g(x)=0.216087, **l/g=4.210**
   - (RMSprop, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.403745, g(x)=0.801821, **l/g=0.504**
   - (RMSprop, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.303275, g(x)=0.648262, **l/g=0.468**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q58. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.36) → loss=0.649
- (Adam, lr=0.24) → loss=0.606
- (SGD, lr=0.18) → loss=0.802
- (SGD, lr=0.42) → loss=0.802
- (SGD, lr=0.50) → loss=0.819
- (SGD, lr=0.30) → loss=0.795
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.606
     - (RMSprop, lr=0.36) → 0.649
   - Bad set (remaining):
     - (SGD, lr=0.30) → 0.795
     - (SGD, lr=0.18) → 0.802
     - (SGD, lr=0.42) → 0.802
     - (SGD, lr=0.50) → 0.819
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.714, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.143
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.479191, g(x)=1.201643, **l/g=0.399**
   - (SGD, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.163310, g(x)=1.330373, **l/g=0.123**
   - (Adam, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.958382, g(x)=0.240329, **l/g=3.988**
   - (Adam, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.326621, g(x)=0.266075, **l/g=1.228**
   - (RMSprop, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.958382, g(x)=0.240329, **l/g=3.988**
   - (RMSprop, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.326621, g(x)=0.266075, **l/g=1.228**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q59. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.24) → loss=0.606
- (SGD, lr=0.36) → loss=0.790
- (SGD, lr=0.50) → loss=0.809
- (SGD, lr=0.42) → loss=0.812
- (Adam, lr=0.30) → loss=0.595
- (RMSprop, lr=0.18) → loss=0.683
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.595
     - (Adam, lr=0.24) → 0.606
   - Bad set (remaining):
     - (RMSprop, lr=0.18) → 0.683
     - (SGD, lr=0.36) → 0.790
     - (SGD, lr=0.50) → 0.809
     - (SGD, lr=0.42) → 0.812
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.610241, g(x)=0.774100, **l/g=0.788**
   - (SGD, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.067574, g(x)=1.201065, **l/g=0.056**
   - (Adam, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.830723, g(x)=0.193525, **l/g=9.460**
   - (Adam, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.202722, g(x)=0.300266, **l/g=0.675**
   - (RMSprop, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.610241, g(x)=0.387050, **l/g=1.577**
   - (RMSprop, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.067574, g(x)=0.600532, **l/g=0.113**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q60. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.24) → loss=0.590
- (Adam, lr=0.30) → loss=0.601
- (Adam, lr=0.50) → loss=0.635
- (Adam, lr=0.18) → loss=0.596
- (Adam, lr=0.42) → loss=0.616
- (Adam, lr=0.36) → loss=0.593
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.590
     - (Adam, lr=0.36) → 0.593
   - Bad set (remaining):
     - (Adam, lr=0.18) → 0.596
     - (Adam, lr=0.30) → 0.601
     - (Adam, lr=0.42) → 0.616
     - (Adam, lr=0.50) → 0.635
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.143, P(Adam|good)=0.600, P(Adam|bad)=0.714, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.143
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.479191, g(x)=0.240329, **l/g=1.994**
   - (SGD, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.163310, g(x)=0.266075, **l/g=0.614**
   - (Adam, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.600, P(opt|bad)=0.714 ⇒ l(x)=1.437573, g(x)=1.201643, **l/g=1.196**
   - (Adam, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.600, P(opt|bad)=0.714 ⇒ l(x)=0.489931, g(x)=1.330373, **l/g=0.368**
   - (RMSprop, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.479191, g(x)=0.240329, **l/g=1.994**
   - (RMSprop, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.163310, g(x)=0.266075, **l/g=0.614**
5) **Select argmax l/g** ⇒ **(SGD, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="SGD", lr=0.20)`.

---
## Q61. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.18) → loss=0.602
- (Adam, lr=0.50) → loss=0.635
- (RMSprop, lr=0.24) → loss=0.662
- (Adam, lr=0.42) → loss=0.616
- (RMSprop, lr=0.36) → loss=0.641
- (SGD, lr=0.30) → loss=0.799
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.602
     - (Adam, lr=0.42) → 0.616
   - Bad set (remaining):
     - (Adam, lr=0.50) → 0.635
     - (RMSprop, lr=0.36) → 0.641
     - (RMSprop, lr=0.24) → 0.662
     - (SGD, lr=0.30) → 0.799
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.426517, g(x)=0.518281, **l/g=0.823**
   - (SGD, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.292076, g(x)=0.440174, **l/g=0.664**
   - (Adam, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.279552, g(x)=0.518281, **l/g=2.469**
   - (Adam, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.876227, g(x)=0.440174, **l/g=1.991**
   - (RMSprop, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.426517, g(x)=0.777422, **l/g=0.549**
   - (RMSprop, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.292076, g(x)=0.660261, **l/g=0.442**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q62. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.50) → loss=0.819
- (SGD, lr=0.30) → loss=0.795
- (Adam, lr=0.18) → loss=0.606
- (Adam, lr=0.24) → loss=0.588
- (RMSprop, lr=0.36) → loss=0.651
- (SGD, lr=0.42) → loss=0.810
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.588
     - (Adam, lr=0.18) → 0.606
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.651
     - (SGD, lr=0.30) → 0.795
     - (SGD, lr=0.42) → 0.810
     - (SGD, lr=0.50) → 0.819
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.759313, g(x)=0.561140, **l/g=1.353**
   - (SGD, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.015967, g(x)=1.274789, **l/g=0.013**
   - (Adam, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=2.277939, g(x)=0.140285, **l/g=16.238**
   - (Adam, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.047901, g(x)=0.318697, **l/g=0.150**
   - (RMSprop, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.759313, g(x)=0.280570, **l/g=2.706**
   - (RMSprop, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.015967, g(x)=0.637394, **l/g=0.025**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q63. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.36) → loss=0.794
- (Adam, lr=0.30) → loss=0.605
- (RMSprop, lr=0.24) → loss=0.656
- (SGD, lr=0.50) → loss=0.807
- (RMSprop, lr=0.42) → loss=0.658
- (Adam, lr=0.18) → loss=0.594
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.594
     - (Adam, lr=0.30) → 0.605
   - Bad set (remaining):
     - (RMSprop, lr=0.24) → 0.656
     - (RMSprop, lr=0.42) → 0.658
     - (SGD, lr=0.36) → 0.794
     - (SGD, lr=0.50) → 0.807
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.633013, g(x)=0.556176, **l/g=1.138**
   - (SGD, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.056375, g(x)=0.912797, **l/g=0.062**
   - (Adam, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.899040, g(x)=0.185392, **l/g=10.243**
   - (Adam, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.169125, g(x)=0.304266, **l/g=0.556**
   - (RMSprop, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.633013, g(x)=0.556176, **l/g=1.138**
   - (RMSprop, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.056375, g(x)=0.912797, **l/g=0.062**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q64. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.24) → loss=0.604
- (Adam, lr=0.50) → loss=0.613
- (Adam, lr=0.36) → loss=0.603
- (Adam, lr=0.42) → loss=0.620
- (Adam, lr=0.30) → loss=0.593
- (Adam, lr=0.18) → loss=0.604
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.593
     - (Adam, lr=0.36) → 0.603
   - Bad set (remaining):
     - (Adam, lr=0.24) → 0.604
     - (Adam, lr=0.18) → 0.604
     - (Adam, lr=0.50) → 0.613
     - (Adam, lr=0.42) → 0.620
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.143, P(Adam|good)=0.600, P(Adam|bad)=0.714, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.143
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.352892, g(x)=0.285435, **l/g=1.236**
   - (SGD, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.203718, g(x)=0.251643, **l/g=0.810**
   - (Adam, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.600, P(opt|bad)=0.714 ⇒ l(x)=1.058675, g(x)=1.427177, **l/g=0.742**
   - (Adam, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.600, P(opt|bad)=0.714 ⇒ l(x)=0.611155, g(x)=1.258216, **l/g=0.486**
   - (RMSprop, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.352892, g(x)=0.285435, **l/g=1.236**
   - (RMSprop, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.203718, g(x)=0.251643, **l/g=0.810**
5) **Select argmax l/g** ⇒ **(SGD, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="SGD", lr=0.20)`.

---
## Q65. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.36) → loss=0.641
- (RMSprop, lr=0.30) → loss=0.657
- (SGD, lr=0.24) → loss=0.813
- (Adam, lr=0.18) → loss=0.594
- (SGD, lr=0.42) → loss=0.804
- (Adam, lr=0.50) → loss=0.637
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.594
     - (Adam, lr=0.50) → 0.637
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.641
     - (RMSprop, lr=0.30) → 0.657
     - (SGD, lr=0.42) → 0.804
     - (SGD, lr=0.24) → 0.813
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.9774, g_lr=1.8916, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.395475, g(x)=0.810682, **l/g=0.488**
   - (SGD, lr=0.50): l_lr=2.0066, g_lr=1.2675, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.401326, g(x)=0.543207, **l/g=0.739**
   - (Adam, lr=0.20): l_lr=1.9774, g_lr=1.8916, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.186424, g(x)=0.270227, **l/g=4.390**
   - (Adam, lr=0.50): l_lr=2.0066, g_lr=1.2675, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.203979, g(x)=0.181069, **l/g=6.649**
   - (RMSprop, lr=0.20): l_lr=1.9774, g_lr=1.8916, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.395475, g(x)=0.810682, **l/g=0.488**
   - (RMSprop, lr=0.50): l_lr=2.0066, g_lr=1.2675, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.401326, g(x)=0.543207, **l/g=0.739**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q66. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.50) → loss=0.807
- (RMSprop, lr=0.24) → loss=0.676
- (Adam, lr=0.18) → loss=0.594
- (RMSprop, lr=0.36) → loss=0.655
- (SGD, lr=0.42) → loss=0.814
- (Adam, lr=0.30) → loss=0.597
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.594
     - (Adam, lr=0.30) → 0.597
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.655
     - (RMSprop, lr=0.24) → 0.676
     - (SGD, lr=0.50) → 0.807
     - (SGD, lr=0.42) → 0.814
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.633013, g(x)=0.556176, **l/g=1.138**
   - (SGD, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.056375, g(x)=0.912797, **l/g=0.062**
   - (Adam, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.899040, g(x)=0.185392, **l/g=10.243**
   - (Adam, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.169125, g(x)=0.304266, **l/g=0.556**
   - (RMSprop, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.633013, g(x)=0.556176, **l/g=1.138**
   - (RMSprop, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.056375, g(x)=0.912797, **l/g=0.062**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q67. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.24) → loss=0.813
- (RMSprop, lr=0.50) → loss=0.643
- (RMSprop, lr=0.36) → loss=0.655
- (RMSprop, lr=0.30) → loss=0.671
- (Adam, lr=0.42) → loss=0.608
- (SGD, lr=0.18) → loss=0.818
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.42) → 0.608
     - (RMSprop, lr=0.50) → 0.643
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.655
     - (RMSprop, lr=0.30) → 0.671
     - (SGD, lr=0.24) → 0.813
     - (SGD, lr=0.18) → 0.818
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=0.1995, g_lr=2.7805, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.039906, g(x)=1.191648, **l/g=0.033**
   - (SGD, lr=0.50): l_lr=3.4432, g_lr=0.5492, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.688634, g(x)=0.235377, **l/g=2.926**
   - (Adam, lr=0.20): l_lr=0.1995, g_lr=2.7805, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.079813, g(x)=0.397216, **l/g=0.201**
   - (Adam, lr=0.50): l_lr=3.4432, g_lr=0.5492, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=1.377268, g(x)=0.078459, **l/g=17.554**
   - (RMSprop, lr=0.20): l_lr=0.1995, g_lr=2.7805, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=0.079813, g(x)=1.191648, **l/g=0.067**
   - (RMSprop, lr=0.50): l_lr=3.4432, g_lr=0.5492, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=1.377268, g(x)=0.235377, **l/g=5.851**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
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
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.596
     - (Adam, lr=0.42) → 0.604
   - Bad set (remaining):
     - (Adam, lr=0.36) → 0.611
     - (SGD, lr=0.18) → 0.802
     - (SGD, lr=0.50) → 0.811
     - (SGD, lr=0.30) → 0.813
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.143
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.403745, g(x)=1.069094, **l/g=0.378**
   - (SGD, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.303275, g(x)=0.864350, **l/g=0.351**
   - (Adam, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.211234, g(x)=0.534547, **l/g=2.266**
   - (Adam, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.909824, g(x)=0.432175, **l/g=2.105**
   - (RMSprop, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.403745, g(x)=0.267274, **l/g=1.511**
   - (RMSprop, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.303275, g(x)=0.216087, **l/g=1.403**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q69. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.42) → loss=0.652
- (RMSprop, lr=0.30) → loss=0.671
- (SGD, lr=0.18) → loss=0.808
- (Adam, lr=0.24) → loss=0.606
- (Adam, lr=0.36) → loss=0.595
- (Adam, lr=0.50) → loss=0.625
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.36) → 0.595
     - (Adam, lr=0.24) → 0.606
   - Bad set (remaining):
     - (Adam, lr=0.50) → 0.625
     - (RMSprop, lr=0.42) → 0.652
     - (RMSprop, lr=0.30) → 0.671
     - (SGD, lr=0.18) → 0.808
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.479191, g(x)=0.480657, **l/g=0.997**
   - (SGD, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.163310, g(x)=0.532149, **l/g=0.307**
   - (Adam, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.437573, g(x)=0.480657, **l/g=2.991**
   - (Adam, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.489931, g(x)=0.532149, **l/g=0.921**
   - (RMSprop, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.479191, g(x)=0.720986, **l/g=0.665**
   - (RMSprop, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.163310, g(x)=0.798224, **l/g=0.205**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q70. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.42) → loss=0.662
- (SGD, lr=0.24) → loss=0.801
- (RMSprop, lr=0.30) → loss=0.665
- (Adam, lr=0.50) → loss=0.615
- (SGD, lr=0.18) → loss=0.812
- (RMSprop, lr=0.36) → loss=0.663
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.50) → 0.615
     - (RMSprop, lr=0.42) → 0.662
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.663
     - (RMSprop, lr=0.30) → 0.665
     - (SGD, lr=0.24) → 0.801
     - (SGD, lr=0.18) → 0.812
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=0.1995, g_lr=2.7805, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.039906, g(x)=1.191648, **l/g=0.033**
   - (SGD, lr=0.50): l_lr=3.4432, g_lr=0.5492, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.688634, g(x)=0.235377, **l/g=2.926**
   - (Adam, lr=0.20): l_lr=0.1995, g_lr=2.7805, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.079813, g(x)=0.397216, **l/g=0.201**
   - (Adam, lr=0.50): l_lr=3.4432, g_lr=0.5492, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=1.377268, g(x)=0.078459, **l/g=17.554**
   - (RMSprop, lr=0.20): l_lr=0.1995, g_lr=2.7805, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=0.079813, g(x)=1.191648, **l/g=0.067**
   - (RMSprop, lr=0.50): l_lr=3.4432, g_lr=0.5492, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=1.377268, g(x)=0.235377, **l/g=5.851**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q71. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.50) → loss=0.621
- (SGD, lr=0.36) → loss=0.806
- (SGD, lr=0.24) → loss=0.795
- (Adam, lr=0.18) → loss=0.602
- (Adam, lr=0.42) → loss=0.622
- (SGD, lr=0.30) → loss=0.795
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.602
     - (Adam, lr=0.50) → 0.621
   - Bad set (remaining):
     - (Adam, lr=0.42) → 0.622
     - (SGD, lr=0.24) → 0.795
     - (SGD, lr=0.30) → 0.795
     - (SGD, lr=0.36) → 0.806
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.143
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.9774, g_lr=1.8916, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.395475, g(x)=1.080909, **l/g=0.366**
   - (SGD, lr=0.50): l_lr=2.0066, g_lr=1.2675, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.401326, g(x)=0.724276, **l/g=0.554**
   - (Adam, lr=0.20): l_lr=1.9774, g_lr=1.8916, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.186424, g(x)=0.540454, **l/g=2.195**
   - (Adam, lr=0.50): l_lr=2.0066, g_lr=1.2675, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.203979, g(x)=0.362138, **l/g=3.325**
   - (RMSprop, lr=0.20): l_lr=1.9774, g_lr=1.8916, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.395475, g(x)=0.270227, **l/g=1.463**
   - (RMSprop, lr=0.50): l_lr=2.0066, g_lr=1.2675, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.401326, g(x)=0.181069, **l/g=2.216**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q72. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.18) → loss=0.608
- (Adam, lr=0.50) → loss=0.615
- (SGD, lr=0.30) → loss=0.801
- (Adam, lr=0.24) → loss=0.610
- (SGD, lr=0.42) → loss=0.796
- (RMSprop, lr=0.36) → loss=0.657
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.608
     - (Adam, lr=0.24) → 0.610
   - Bad set (remaining):
     - (Adam, lr=0.50) → 0.615
     - (RMSprop, lr=0.36) → 0.657
     - (SGD, lr=0.42) → 0.796
     - (SGD, lr=0.30) → 0.801
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.759313, g(x)=0.420855, **l/g=1.804**
   - (SGD, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.015967, g(x)=0.956092, **l/g=0.017**
   - (Adam, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=2.277939, g(x)=0.280570, **l/g=8.119**
   - (Adam, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.047901, g(x)=0.637394, **l/g=0.075**
   - (RMSprop, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.759313, g(x)=0.280570, **l/g=2.706**
   - (RMSprop, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.015967, g(x)=0.637394, **l/g=0.025**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q73. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.18) → loss=0.669
- (Adam, lr=0.30) → loss=0.601
- (SGD, lr=0.24) → loss=0.815
- (SGD, lr=0.42) → loss=0.796
- (RMSprop, lr=0.50) → loss=0.655
- (Adam, lr=0.36) → loss=0.593
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.36) → 0.593
     - (Adam, lr=0.30) → 0.601
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.655
     - (RMSprop, lr=0.18) → 0.669
     - (SGD, lr=0.42) → 0.796
     - (SGD, lr=0.24) → 0.815
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.352892, g(x)=0.856306, **l/g=0.412**
   - (SGD, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.203718, g(x)=0.754930, **l/g=0.270**
   - (Adam, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.058675, g(x)=0.285435, **l/g=3.709**
   - (Adam, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.611155, g(x)=0.251643, **l/g=2.429**
   - (RMSprop, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.352892, g(x)=0.856306, **l/g=0.412**
   - (RMSprop, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.203718, g(x)=0.754930, **l/g=0.270**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q74. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.42) → loss=0.612
- (Adam, lr=0.18) → loss=0.612
- (SGD, lr=0.24) → loss=0.799
- (SGD, lr=0.36) → loss=0.804
- (RMSprop, lr=0.50) → loss=0.639
- (SGD, lr=0.30) → loss=0.799
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.42) → 0.612
     - (Adam, lr=0.18) → 0.612
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.639
     - (SGD, lr=0.24) → 0.799
     - (SGD, lr=0.30) → 0.799
     - (SGD, lr=0.36) → 0.804
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.426517, g(x)=1.036562, **l/g=0.411**
   - (SGD, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.292076, g(x)=0.880348, **l/g=0.332**
   - (Adam, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.279552, g(x)=0.259141, **l/g=4.938**
   - (Adam, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.876227, g(x)=0.220087, **l/g=3.981**
   - (RMSprop, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.426517, g(x)=0.518281, **l/g=0.823**
   - (RMSprop, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.292076, g(x)=0.440174, **l/g=0.664**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q75. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.24) → loss=0.815
- (RMSprop, lr=0.36) → loss=0.647
- (Adam, lr=0.50) → loss=0.629
- (Adam, lr=0.42) → loss=0.600
- (RMSprop, lr=0.30) → loss=0.657
- (Adam, lr=0.18) → loss=0.610
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.42) → 0.600
     - (Adam, lr=0.18) → 0.610
   - Bad set (remaining):
     - (Adam, lr=0.50) → 0.629
     - (RMSprop, lr=0.36) → 0.647
     - (RMSprop, lr=0.30) → 0.657
     - (SGD, lr=0.24) → 0.815
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.426517, g(x)=0.518281, **l/g=0.823**
   - (SGD, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.292076, g(x)=0.440174, **l/g=0.664**
   - (Adam, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.279552, g(x)=0.518281, **l/g=2.469**
   - (Adam, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.876227, g(x)=0.440174, **l/g=1.991**
   - (RMSprop, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.426517, g(x)=0.777422, **l/g=0.549**
   - (RMSprop, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.292076, g(x)=0.660261, **l/g=0.442**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q76. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.50) → loss=0.645
- (Adam, lr=0.42) → loss=0.616
- (RMSprop, lr=0.30) → loss=0.647
- (SGD, lr=0.36) → loss=0.798
- (Adam, lr=0.24) → loss=0.608
- (SGD, lr=0.18) → loss=0.804
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.608
     - (Adam, lr=0.42) → 0.616
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.645
     - (RMSprop, lr=0.30) → 0.647
     - (SGD, lr=0.36) → 0.798
     - (SGD, lr=0.18) → 0.804
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.403745, g(x)=0.801821, **l/g=0.504**
   - (SGD, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.303275, g(x)=0.648262, **l/g=0.468**
   - (Adam, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.211234, g(x)=0.267274, **l/g=4.532**
   - (Adam, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.909824, g(x)=0.216087, **l/g=4.210**
   - (RMSprop, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.403745, g(x)=0.801821, **l/g=0.504**
   - (RMSprop, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.303275, g(x)=0.648262, **l/g=0.468**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q77. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.50) → loss=0.629
- (RMSprop, lr=0.30) → loss=0.647
- (SGD, lr=0.36) → loss=0.798
- (Adam, lr=0.42) → loss=0.620
- (Adam, lr=0.24) → loss=0.592
- (RMSprop, lr=0.18) → loss=0.681
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.592
     - (Adam, lr=0.42) → 0.620
   - Bad set (remaining):
     - (Adam, lr=0.50) → 0.629
     - (RMSprop, lr=0.30) → 0.647
     - (RMSprop, lr=0.18) → 0.681
     - (SGD, lr=0.36) → 0.798
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.403745, g(x)=0.534547, **l/g=0.755**
   - (SGD, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.303275, g(x)=0.432175, **l/g=0.702**
   - (Adam, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.211234, g(x)=0.534547, **l/g=2.266**
   - (Adam, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.909824, g(x)=0.432175, **l/g=2.105**
   - (RMSprop, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.403745, g(x)=0.801821, **l/g=0.504**
   - (RMSprop, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.303275, g(x)=0.648262, **l/g=0.468**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q78. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.50) → loss=0.797
- (SGD, lr=0.18) → loss=0.810
- (Adam, lr=0.36) → loss=0.613
- (Adam, lr=0.30) → loss=0.593
- (Adam, lr=0.24) → loss=0.602
- (RMSprop, lr=0.42) → loss=0.662
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.593
     - (Adam, lr=0.24) → 0.602
   - Bad set (remaining):
     - (Adam, lr=0.36) → 0.613
     - (RMSprop, lr=0.42) → 0.662
     - (SGD, lr=0.50) → 0.797
     - (SGD, lr=0.18) → 0.810
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.610241, g(x)=0.580575, **l/g=1.051**
   - (SGD, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.067574, g(x)=0.900799, **l/g=0.075**
   - (Adam, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.830723, g(x)=0.387050, **l/g=4.730**
   - (Adam, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.202722, g(x)=0.600532, **l/g=0.338**
   - (RMSprop, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.610241, g(x)=0.387050, **l/g=1.577**
   - (RMSprop, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.067574, g(x)=0.600532, **l/g=0.113**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q79. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.18) → loss=0.810
- (Adam, lr=0.42) → loss=0.620
- (SGD, lr=0.24) → loss=0.797
- (RMSprop, lr=0.50) → loss=0.653
- (Adam, lr=0.36) → loss=0.617
- (RMSprop, lr=0.30) → loss=0.655
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.36) → 0.617
     - (Adam, lr=0.42) → 0.620
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.653
     - (RMSprop, lr=0.30) → 0.655
     - (SGD, lr=0.24) → 0.797
     - (SGD, lr=0.18) → 0.810
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=0.7320, g_lr=2.5143, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.146395, g(x)=1.077552, **l/g=0.136**
   - (SGD, lr=0.50): l_lr=2.1971, g_lr=1.1723, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.439419, g(x)=0.502393, **l/g=0.875**
   - (Adam, lr=0.20): l_lr=0.7320, g_lr=2.5143, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.439186, g(x)=0.359184, **l/g=1.223**
   - (Adam, lr=0.50): l_lr=2.1971, g_lr=1.1723, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.318257, g(x)=0.167464, **l/g=7.872**
   - (RMSprop, lr=0.20): l_lr=0.7320, g_lr=2.5143, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.146395, g(x)=1.077552, **l/g=0.136**
   - (RMSprop, lr=0.50): l_lr=2.1971, g_lr=1.1723, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.439419, g(x)=0.502393, **l/g=0.875**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q80. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.18) → loss=0.820
- (Adam, lr=0.42) → loss=0.604
- (SGD, lr=0.36) → loss=0.802
- (SGD, lr=0.50) → loss=0.821
- (Adam, lr=0.30) → loss=0.597
- (RMSprop, lr=0.24) → loss=0.674
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.597
     - (Adam, lr=0.42) → 0.604
   - Bad set (remaining):
     - (RMSprop, lr=0.24) → 0.674
     - (SGD, lr=0.36) → 0.802
     - (SGD, lr=0.18) → 0.820
     - (SGD, lr=0.50) → 0.821
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.3872, g_lr=2.1867, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.277445, g(x)=1.249522, **l/g=0.222**
   - (SGD, lr=0.50): l_lr=1.7184, g_lr=1.4116, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.343683, g(x)=0.806624, **l/g=0.426**
   - (Adam, lr=0.20): l_lr=1.3872, g_lr=2.1867, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.832336, g(x)=0.312381, **l/g=2.664**
   - (Adam, lr=0.50): l_lr=1.7184, g_lr=1.4116, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.031048, g(x)=0.201656, **l/g=5.113**
   - (RMSprop, lr=0.20): l_lr=1.3872, g_lr=2.1867, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.277445, g(x)=0.624761, **l/g=0.444**
   - (RMSprop, lr=0.50): l_lr=1.7184, g_lr=1.4116, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.343683, g(x)=0.403312, **l/g=0.852**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q81. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.24) → loss=0.797
- (RMSprop, lr=0.50) → loss=0.653
- (RMSprop, lr=0.30) → loss=0.671
- (RMSprop, lr=0.18) → loss=0.675
- (SGD, lr=0.36) → loss=0.806
- (SGD, lr=0.42) → loss=0.792
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (RMSprop, lr=0.50) → 0.653
     - (RMSprop, lr=0.30) → 0.671
   - Bad set (remaining):
     - (RMSprop, lr=0.18) → 0.675
     - (SGD, lr=0.42) → 0.792
     - (SGD, lr=0.24) → 0.797
     - (SGD, lr=0.36) → 0.806
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.200, P(Adam|bad)=0.143, P(RMSprop|good)=0.600, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.2320, g_lr=2.2643, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.246403, g(x)=1.293869, **l/g=0.190**
   - (SGD, lr=0.50): l_lr=2.2647, g_lr=1.1385, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.452933, g(x)=0.650552, **l/g=0.696**
   - (Adam, lr=0.20): l_lr=1.2320, g_lr=2.2643, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.246403, g(x)=0.323467, **l/g=0.762**
   - (Adam, lr=0.50): l_lr=2.2647, g_lr=1.1385, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.452933, g(x)=0.162638, **l/g=2.785**
   - (RMSprop, lr=0.20): l_lr=1.2320, g_lr=2.2643, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.739208, g(x)=0.646934, **l/g=1.143**
   - (RMSprop, lr=0.50): l_lr=2.2647, g_lr=1.1385, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.358800, g(x)=0.325276, **l/g=4.177**
5) **Select argmax l/g** ⇒ **(RMSprop, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="RMSprop", lr=0.50)`.

---
## Q82. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.36) → loss=0.607
- (Adam, lr=0.30) → loss=0.613
- (RMSprop, lr=0.50) → loss=0.647
- (Adam, lr=0.42) → loss=0.618
- (SGD, lr=0.18) → loss=0.802
- (Adam, lr=0.24) → loss=0.600
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.600
     - (Adam, lr=0.36) → 0.607
   - Bad set (remaining):
     - (Adam, lr=0.30) → 0.613
     - (Adam, lr=0.42) → 0.618
     - (RMSprop, lr=0.50) → 0.647
     - (SGD, lr=0.18) → 0.802
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.429, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.479191, g(x)=0.480657, **l/g=0.997**
   - (SGD, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.163310, g(x)=0.532149, **l/g=0.307**
   - (Adam, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.600, P(opt|bad)=0.429 ⇒ l(x)=1.437573, g(x)=0.720986, **l/g=1.994**
   - (Adam, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.600, P(opt|bad)=0.429 ⇒ l(x)=0.489931, g(x)=0.798224, **l/g=0.614**
   - (RMSprop, lr=0.20): l_lr=2.3960, g_lr=1.6823, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.479191, g(x)=0.480657, **l/g=0.997**
   - (RMSprop, lr=0.50): l_lr=0.8166, g_lr=1.8625, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.163310, g(x)=0.532149, **l/g=0.307**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q83. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.42) → loss=0.814
- (RMSprop, lr=0.18) → loss=0.675
- (Adam, lr=0.24) → loss=0.606
- (SGD, lr=0.36) → loss=0.790
- (SGD, lr=0.30) → loss=0.801
- (RMSprop, lr=0.50) → loss=0.661
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.606
     - (RMSprop, lr=0.50) → 0.661
   - Bad set (remaining):
     - (RMSprop, lr=0.18) → 0.675
     - (SGD, lr=0.36) → 0.790
     - (SGD, lr=0.30) → 0.801
     - (SGD, lr=0.42) → 0.814
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.8635, g_lr=1.9485, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.372702, g(x)=1.113441, **l/g=0.335**
   - (SGD, lr=0.50): l_lr=2.0626, g_lr=1.2395, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.412525, g(x)=0.708277, **l/g=0.582**
   - (Adam, lr=0.20): l_lr=1.8635, g_lr=1.9485, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.745404, g(x)=0.278360, **l/g=2.678**
   - (Adam, lr=0.50): l_lr=2.0626, g_lr=1.2395, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.825050, g(x)=0.177069, **l/g=4.659**
   - (RMSprop, lr=0.20): l_lr=1.8635, g_lr=1.9485, P(opt|good)=0.400, P(opt|bad)=0.286 ⇒ l(x)=0.745404, g(x)=0.556721, **l/g=1.339**
   - (RMSprop, lr=0.50): l_lr=2.0626, g_lr=1.2395, P(opt|good)=0.400, P(opt|bad)=0.286 ⇒ l(x)=0.825050, g(x)=0.354139, **l/g=2.330**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q84. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.36) → loss=0.649
- (Adam, lr=0.50) → loss=0.631
- (Adam, lr=0.42) → loss=0.602
- (RMSprop, lr=0.30) → loss=0.659
- (SGD, lr=0.18) → loss=0.822
- (Adam, lr=0.24) → loss=0.594
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.594
     - (Adam, lr=0.42) → 0.602
   - Bad set (remaining):
     - (Adam, lr=0.50) → 0.631
     - (RMSprop, lr=0.36) → 0.649
     - (RMSprop, lr=0.30) → 0.659
     - (SGD, lr=0.18) → 0.822
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.403745, g(x)=0.534547, **l/g=0.755**
   - (SGD, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.303275, g(x)=0.432175, **l/g=0.702**
   - (Adam, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.211234, g(x)=0.534547, **l/g=2.266**
   - (Adam, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.909824, g(x)=0.432175, **l/g=2.105**
   - (RMSprop, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.403745, g(x)=0.801821, **l/g=0.504**
   - (RMSprop, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.303275, g(x)=0.648262, **l/g=0.468**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q85. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.50) → loss=0.657
- (SGD, lr=0.30) → loss=0.791
- (SGD, lr=0.42) → loss=0.802
- (RMSprop, lr=0.18) → loss=0.689
- (RMSprop, lr=0.36) → loss=0.647
- (RMSprop, lr=0.24) → loss=0.672
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (RMSprop, lr=0.36) → 0.647
     - (RMSprop, lr=0.50) → 0.657
   - Bad set (remaining):
     - (RMSprop, lr=0.24) → 0.672
     - (RMSprop, lr=0.18) → 0.689
     - (SGD, lr=0.30) → 0.791
     - (SGD, lr=0.42) → 0.802
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.200, P(Adam|bad)=0.143, P(RMSprop|good)=0.600, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=0.5768, g_lr=2.5919, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.115353, g(x)=1.110812, **l/g=0.104**
   - (SGD, lr=0.50): l_lr=2.7433, g_lr=0.8991, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.548670, g(x)=0.385339, **l/g=1.424**
   - (Adam, lr=0.20): l_lr=0.5768, g_lr=2.5919, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.115353, g(x)=0.370271, **l/g=0.312**
   - (Adam, lr=0.50): l_lr=2.7433, g_lr=0.8991, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.548670, g(x)=0.128446, **l/g=4.272**
   - (RMSprop, lr=0.20): l_lr=0.5768, g_lr=2.5919, P(opt|good)=0.600, P(opt|bad)=0.429 ⇒ l(x)=0.346058, g(x)=1.110812, **l/g=0.312**
   - (RMSprop, lr=0.50): l_lr=2.7433, g_lr=0.8991, P(opt|good)=0.600, P(opt|bad)=0.429 ⇒ l(x)=1.646009, g(x)=0.385339, **l/g=4.272**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q86. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.36) → loss=0.643
- (RMSprop, lr=0.18) → loss=0.679
- (SGD, lr=0.42) → loss=0.812
- (SGD, lr=0.24) → loss=0.799
- (SGD, lr=0.30) → loss=0.805
- (Adam, lr=0.50) → loss=0.613
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.50) → 0.613
     - (RMSprop, lr=0.36) → 0.643
   - Bad set (remaining):
     - (RMSprop, lr=0.18) → 0.679
     - (SGD, lr=0.24) → 0.799
     - (SGD, lr=0.30) → 0.805
     - (SGD, lr=0.42) → 0.812
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=0.5768, g_lr=2.5919, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.115353, g(x)=1.481083, **l/g=0.078**
   - (SGD, lr=0.50): l_lr=2.7433, g_lr=0.8991, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.548670, g(x)=0.513785, **l/g=1.068**
   - (Adam, lr=0.20): l_lr=0.5768, g_lr=2.5919, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.230705, g(x)=0.370271, **l/g=0.623**
   - (Adam, lr=0.50): l_lr=2.7433, g_lr=0.8991, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=1.097339, g(x)=0.128446, **l/g=8.543**
   - (RMSprop, lr=0.20): l_lr=0.5768, g_lr=2.5919, P(opt|good)=0.400, P(opt|bad)=0.286 ⇒ l(x)=0.230705, g(x)=0.740542, **l/g=0.312**
   - (RMSprop, lr=0.50): l_lr=2.7433, g_lr=0.8991, P(opt|good)=0.400, P(opt|bad)=0.286 ⇒ l(x)=1.097339, g(x)=0.256893, **l/g=4.272**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.50)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.50)`.

---
## Q87. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.50) → loss=0.809
- (Adam, lr=0.30) → loss=0.611
- (RMSprop, lr=0.36) → loss=0.647
- (RMSprop, lr=0.24) → loss=0.672
- (SGD, lr=0.18) → loss=0.800
- (RMSprop, lr=0.42) → loss=0.648
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.611
     - (RMSprop, lr=0.36) → 0.647
   - Bad set (remaining):
     - (RMSprop, lr=0.42) → 0.648
     - (RMSprop, lr=0.24) → 0.672
     - (SGD, lr=0.18) → 0.800
     - (SGD, lr=0.50) → 0.809
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.352892, g(x)=0.856306, **l/g=0.412**
   - (SGD, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.203718, g(x)=0.754930, **l/g=0.270**
   - (Adam, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.705783, g(x)=0.285435, **l/g=2.473**
   - (Adam, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.407437, g(x)=0.251643, **l/g=1.619**
   - (RMSprop, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=0.705783, g(x)=0.856306, **l/g=0.824**
   - (RMSprop, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=0.407437, g(x)=0.754930, **l/g=0.540**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q88. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.36) → loss=0.810
- (SGD, lr=0.24) → loss=0.799
- (RMSprop, lr=0.50) → loss=0.655
- (Adam, lr=0.18) → loss=0.590
- (SGD, lr=0.30) → loss=0.799
- (Adam, lr=0.42) → loss=0.620
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.590
     - (Adam, lr=0.42) → 0.620
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.655
     - (SGD, lr=0.24) → 0.799
     - (SGD, lr=0.30) → 0.799
     - (SGD, lr=0.36) → 0.810
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.426517, g(x)=1.036562, **l/g=0.411**
   - (SGD, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.292076, g(x)=0.880348, **l/g=0.332**
   - (Adam, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.279552, g(x)=0.259141, **l/g=4.938**
   - (Adam, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.876227, g(x)=0.220087, **l/g=3.981**
   - (RMSprop, lr=0.20): l_lr=2.1326, g_lr=1.8140, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.426517, g(x)=0.518281, **l/g=0.823**
   - (RMSprop, lr=0.50): l_lr=1.4604, g_lr=1.5406, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.292076, g(x)=0.440174, **l/g=0.664**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q89. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.42) → loss=0.644
- (Adam, lr=0.24) → loss=0.604
- (RMSprop, lr=0.30) → loss=0.647
- (SGD, lr=0.50) → loss=0.807
- (Adam, lr=0.18) → loss=0.610
- (RMSprop, lr=0.36) → loss=0.645
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.604
     - (Adam, lr=0.18) → 0.610
   - Bad set (remaining):
     - (RMSprop, lr=0.42) → 0.644
     - (RMSprop, lr=0.36) → 0.645
     - (RMSprop, lr=0.30) → 0.647
     - (SGD, lr=0.50) → 0.807
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.571
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.759313, g(x)=0.280570, **l/g=2.706**
   - (SGD, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.015967, g(x)=0.637394, **l/g=0.025**
   - (Adam, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=2.277939, g(x)=0.140285, **l/g=16.238**
   - (Adam, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.047901, g(x)=0.318697, **l/g=0.150**
   - (RMSprop, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.759313, g(x)=0.561140, **l/g=1.353**
   - (RMSprop, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.015967, g(x)=1.274789, **l/g=0.013**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q90. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.50) → loss=0.655
- (RMSprop, lr=0.36) → loss=0.641
- (SGD, lr=0.42) → loss=0.800
- (Adam, lr=0.24) → loss=0.608
- (SGD, lr=0.18) → loss=0.804
- (Adam, lr=0.30) → loss=0.603
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.603
     - (Adam, lr=0.24) → 0.608
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.641
     - (RMSprop, lr=0.50) → 0.655
     - (SGD, lr=0.42) → 0.800
     - (SGD, lr=0.18) → 0.804
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.610241, g(x)=0.580575, **l/g=1.051**
   - (SGD, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.067574, g(x)=0.900799, **l/g=0.075**
   - (Adam, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.830723, g(x)=0.193525, **l/g=9.460**
   - (Adam, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.202722, g(x)=0.300266, **l/g=0.675**
   - (RMSprop, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.610241, g(x)=0.580575, **l/g=1.051**
   - (RMSprop, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.067574, g(x)=0.900799, **l/g=0.075**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q91. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.18) → loss=0.590
- (SGD, lr=0.42) → loss=0.800
- (Adam, lr=0.24) → loss=0.608
- (Adam, lr=0.36) → loss=0.597
- (Adam, lr=0.50) → loss=0.627
- (RMSprop, lr=0.30) → loss=0.671
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.590
     - (Adam, lr=0.36) → 0.597
   - Bad set (remaining):
     - (Adam, lr=0.24) → 0.608
     - (Adam, lr=0.50) → 0.627
     - (RMSprop, lr=0.30) → 0.671
     - (SGD, lr=0.42) → 0.800
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.429, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.501964, g(x)=0.464391, **l/g=1.081**
   - (SGD, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.152112, g(x)=0.540148, **l/g=0.282**
   - (Adam, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.600, P(opt|bad)=0.429 ⇒ l(x)=1.505891, g(x)=0.696586, **l/g=2.162**
   - (Adam, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.600, P(opt|bad)=0.429 ⇒ l(x)=0.456335, g(x)=0.810223, **l/g=0.563**
   - (RMSprop, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.501964, g(x)=0.464391, **l/g=1.081**
   - (RMSprop, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.152112, g(x)=0.540148, **l/g=0.282**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q92. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.36) → loss=0.651
- (RMSprop, lr=0.50) → loss=0.659
- (RMSprop, lr=0.30) → loss=0.651
- (Adam, lr=0.24) → loss=0.602
- (SGD, lr=0.18) → loss=0.824
- (SGD, lr=0.42) → loss=0.798
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.602
     - (RMSprop, lr=0.30) → 0.651
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.651
     - (RMSprop, lr=0.50) → 0.659
     - (SGD, lr=0.42) → 0.798
     - (SGD, lr=0.18) → 0.824
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.429, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.610241, g(x)=0.580575, **l/g=1.051**
   - (SGD, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.067574, g(x)=0.900799, **l/g=0.075**
   - (Adam, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=1.220482, g(x)=0.193525, **l/g=6.307**
   - (Adam, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.135148, g(x)=0.300266, **l/g=0.450**
   - (RMSprop, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=1.220482, g(x)=0.580575, **l/g=2.102**
   - (RMSprop, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.400, P(opt|bad)=0.429 ⇒ l(x)=0.135148, g(x)=0.900799, **l/g=0.150**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q93. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.36) → loss=0.613
- (RMSprop, lr=0.50) → loss=0.643
- (RMSprop, lr=0.24) → loss=0.670
- (RMSprop, lr=0.30) → loss=0.671
- (Adam, lr=0.18) → loss=0.598
- (RMSprop, lr=0.42) → loss=0.656
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.598
     - (Adam, lr=0.36) → 0.613
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.643
     - (RMSprop, lr=0.42) → 0.656
     - (RMSprop, lr=0.24) → 0.670
     - (RMSprop, lr=0.30) → 0.671
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.143, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.714
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.501964, g(x)=0.232195, **l/g=2.162**
   - (SGD, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.152112, g(x)=0.270074, **l/g=0.563**
   - (Adam, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.505891, g(x)=0.232195, **l/g=6.485**
   - (Adam, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.456335, g(x)=0.270074, **l/g=1.690**
   - (RMSprop, lr=0.20): l_lr=2.5098, g_lr=1.6254, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.501964, g(x)=1.160977, **l/g=0.432**
   - (RMSprop, lr=0.50): l_lr=0.7606, g_lr=1.8905, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.152112, g(x)=1.350371, **l/g=0.113**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q94. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.24) → loss=0.797
- (SGD, lr=0.36) → loss=0.802
- (Adam, lr=0.30) → loss=0.613
- (Adam, lr=0.18) → loss=0.598
- (SGD, lr=0.42) → loss=0.808
- (SGD, lr=0.50) → loss=0.799
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.18) → 0.598
     - (Adam, lr=0.30) → 0.613
   - Bad set (remaining):
     - (SGD, lr=0.24) → 0.797
     - (SGD, lr=0.50) → 0.799
     - (SGD, lr=0.36) → 0.802
     - (SGD, lr=0.42) → 0.808
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.714, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.143
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.633013, g(x)=0.926960, **l/g=0.683**
   - (SGD, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.056375, g(x)=1.521329, **l/g=0.037**
   - (Adam, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.899040, g(x)=0.185392, **l/g=10.243**
   - (Adam, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.169125, g(x)=0.304266, **l/g=0.556**
   - (RMSprop, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.633013, g(x)=0.185392, **l/g=3.414**
   - (RMSprop, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.056375, g(x)=0.304266, **l/g=0.185**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
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
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.591
     - (Adam, lr=0.24) → 0.600
   - Bad set (remaining):
     - (Adam, lr=0.36) → 0.607
     - (RMSprop, lr=0.50) → 0.663
     - (RMSprop, lr=0.18) → 0.685
     - (SGD, lr=0.42) → 0.798
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.429
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.610241, g(x)=0.387050, **l/g=1.577**
   - (SGD, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.067574, g(x)=0.600532, **l/g=0.113**
   - (Adam, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.830723, g(x)=0.387050, **l/g=4.730**
   - (Adam, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.202722, g(x)=0.600532, **l/g=0.338**
   - (RMSprop, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.610241, g(x)=0.580575, **l/g=1.051**
   - (RMSprop, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.429 ⇒ l(x)=0.067574, g(x)=0.900799, **l/g=0.075**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q96. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.42) → loss=0.814
- (Adam, lr=0.24) → loss=0.596
- (SGD, lr=0.50) → loss=0.815
- (RMSprop, lr=0.36) → loss=0.643
- (SGD, lr=0.30) → loss=0.801
- (Adam, lr=0.18) → loss=0.612
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.596
     - (Adam, lr=0.18) → 0.612
   - Bad set (remaining):
     - (RMSprop, lr=0.36) → 0.643
     - (SGD, lr=0.30) → 0.801
     - (SGD, lr=0.42) → 0.814
     - (SGD, lr=0.50) → 0.815
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.759313, g(x)=0.561140, **l/g=1.353**
   - (SGD, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.015967, g(x)=1.274789, **l/g=0.013**
   - (Adam, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=2.277939, g(x)=0.140285, **l/g=16.238**
   - (Adam, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.047901, g(x)=0.318697, **l/g=0.150**
   - (RMSprop, lr=0.20): l_lr=3.7966, g_lr=0.9820, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.759313, g(x)=0.280570, **l/g=2.706**
   - (RMSprop, lr=0.50): l_lr=0.0798, g_lr=2.2309, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.015967, g(x)=0.637394, **l/g=0.025**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q97. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (Adam, lr=0.24) → loss=0.596
- (RMSprop, lr=0.18) → loss=0.685
- (Adam, lr=0.30) → loss=0.591
- (RMSprop, lr=0.42) → loss=0.650
- (Adam, lr=0.50) → loss=0.635
- (RMSprop, lr=0.36) → loss=0.647
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.591
     - (Adam, lr=0.24) → 0.596
   - Bad set (remaining):
     - (Adam, lr=0.50) → 0.635
     - (RMSprop, lr=0.36) → 0.647
     - (RMSprop, lr=0.42) → 0.650
     - (RMSprop, lr=0.18) → 0.685
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.143, P(Adam|good)=0.600, P(Adam|bad)=0.286, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.571
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.610241, g(x)=0.193525, **l/g=3.153**
   - (SGD, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.143 ⇒ l(x)=0.067574, g(x)=0.300266, **l/g=0.225**
   - (Adam, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=1.830723, g(x)=0.387050, **l/g=4.730**
   - (Adam, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.600, P(opt|bad)=0.286 ⇒ l(x)=0.202722, g(x)=0.600532, **l/g=0.338**
   - (RMSprop, lr=0.20): l_lr=3.0512, g_lr=1.3547, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.610241, g(x)=0.774100, **l/g=0.788**
   - (RMSprop, lr=0.50): l_lr=0.3379, g_lr=2.1019, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.067574, g(x)=1.201065, **l/g=0.056**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q98. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (SGD, lr=0.24) → loss=0.811
- (Adam, lr=0.30) → loss=0.591
- (SGD, lr=0.42) → loss=0.802
- (RMSprop, lr=0.18) → loss=0.689
- (SGD, lr=0.36) → loss=0.794
- (SGD, lr=0.50) → loss=0.813
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.30) → 0.591
     - (RMSprop, lr=0.18) → 0.689
   - Bad set (remaining):
     - (SGD, lr=0.36) → 0.794
     - (SGD, lr=0.42) → 0.802
     - (SGD, lr=0.24) → 0.811
     - (SGD, lr=0.50) → 0.813
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.714, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.143
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.633013, g(x)=0.926960, **l/g=0.683**
   - (SGD, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.200, P(opt|bad)=0.714 ⇒ l(x)=0.056375, g(x)=1.521329, **l/g=0.037**
   - (Adam, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=1.266027, g(x)=0.185392, **l/g=6.829**
   - (Adam, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.112750, g(x)=0.304266, **l/g=0.371**
   - (RMSprop, lr=0.20): l_lr=3.1651, g_lr=1.2977, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=1.266027, g(x)=0.185392, **l/g=6.829**
   - (RMSprop, lr=0.50): l_lr=0.2819, g_lr=2.1299, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.112750, g(x)=0.304266, **l/g=0.371**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q99. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.42) → loss=0.640
- (Adam, lr=0.24) → loss=0.600
- (SGD, lr=0.30) → loss=0.811
- (RMSprop, lr=0.18) → loss=0.673
- (SGD, lr=0.36) → loss=0.804
- (SGD, lr=0.50) → loss=0.797
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.24) → 0.600
     - (RMSprop, lr=0.42) → 0.640
   - Bad set (remaining):
     - (RMSprop, lr=0.18) → 0.673
     - (SGD, lr=0.50) → 0.797
     - (SGD, lr=0.36) → 0.804
     - (SGD, lr=0.30) → 0.811
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.571, P(Adam|good)=0.400, P(Adam|bad)=0.143, P(RMSprop|good)=0.400, P(RMSprop|bad)=0.286
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.403745, g(x)=1.069094, **l/g=0.378**
   - (SGD, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.303275, g(x)=0.864350, **l/g=0.351**
   - (Adam, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.807489, g(x)=0.267274, **l/g=3.021**
   - (Adam, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.400, P(opt|bad)=0.143 ⇒ l(x)=0.606549, g(x)=0.216087, **l/g=2.807**
   - (RMSprop, lr=0.20): l_lr=2.0187, g_lr=1.8709, P(opt|good)=0.400, P(opt|bad)=0.286 ⇒ l(x)=0.807489, g(x)=0.534547, **l/g=1.511**
   - (RMSprop, lr=0.50): l_lr=1.5164, g_lr=1.5126, P(opt|good)=0.400, P(opt|bad)=0.286 ⇒ l(x)=0.606549, g(x)=0.432175, **l/g=1.403**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
## Q100. TPE-based BO — propose next (optimizer, lr)
**Search space**: optimizer ∈ {SGD, Adam, RMSprop} (categorical), learning rate `lr ∈ [0,1]` (continuous).  
**Observed trials** (loss):
- (RMSprop, lr=0.50) → loss=0.651
- (Adam, lr=0.30) → loss=0.611
- (Adam, lr=0.36) → loss=0.599
- (RMSprop, lr=0.42) → loss=0.654
- (RMSprop, lr=0.18) → loss=0.667
- (SGD, lr=0.24) → loss=0.803
**Candidate set**:
- (SGD, 0.20), (SGD, 0.50), (Adam, 0.20), (Adam, 0.50), (RMSprop, 0.20), (RMSprop, 0.50)

**Ask**: Using TPE with γ=0.33 and Gaussian KDE (h=0.10) + Laplace-smoothed categorical masses (α=1), which candidate should be sampled next?
**Answer (step-by-step):**
1) **Choose surrogate**: categorical present ⇒ use **TPE**.
2) **Split trials** by loss (lower is better) at γ-quantile (γ=0.33 ⇒ top ~1/3 as **good**):
   - Good set (best losses):
     - (Adam, lr=0.36) → 0.599
     - (Adam, lr=0.30) → 0.611
   - Bad set (remaining):
     - (RMSprop, lr=0.50) → 0.651
     - (RMSprop, lr=0.42) → 0.654
     - (RMSprop, lr=0.18) → 0.667
     - (SGD, lr=0.24) → 0.803
3) **Fit l(x) and g(x)**:
   - Categorical masses with Laplace smoothing: P(SGD|good)=0.200, P(SGD|bad)=0.286, P(Adam|good)=0.600, P(Adam|bad)=0.143, P(RMSprop|good)=0.200, P(RMSprop|bad)=0.571
   - KDEs for `lr` (Gaussian, h=0.10) constructed from `good` vs `bad` sets.
4) **Evaluate l/g** at candidates (factorized across dims):
   - (SGD, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.352892, g(x)=0.570871, **l/g=0.618**
   - (SGD, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.286 ⇒ l(x)=0.203718, g(x)=0.503286, **l/g=0.405**
   - (Adam, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=1.058675, g(x)=0.285435, **l/g=3.709**
   - (Adam, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.600, P(opt|bad)=0.143 ⇒ l(x)=0.611155, g(x)=0.251643, **l/g=2.429**
   - (RMSprop, lr=0.20): l_lr=1.7645, g_lr=1.9980, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.352892, g(x)=1.141742, **l/g=0.309**
   - (RMSprop, lr=0.50): l_lr=1.0186, g_lr=1.7615, P(opt|good)=0.200, P(opt|bad)=0.571 ⇒ l(x)=0.203718, g(x)=1.006573, **l/g=0.202**
5) **Select argmax l/g** ⇒ **(Adam, lr=0.20)**.
6) **Recommendation**: next trial `(optimizer="Adam", lr=0.20)`.

---
