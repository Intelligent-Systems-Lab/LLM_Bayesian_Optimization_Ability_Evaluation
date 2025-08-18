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