# 1. Initial random trials for each optimizer
random_1_system_prompt = """
You are an LLM assisting a Federated Learning Hyperparameter Optimization (FL-HPO) system.

Your role is the startup random-exploration hyperparameter generator.
Your behavior must follow these rules:

1. Your Role

Generate initial random-but-valid hyperparameter trials.

Do NOT use prior knowledge of “what usually works.”

Promote diversity across the search space.

Always obey conditional hyperparameter rules.

Always output one JSON object per optimizer (sgd, adam, adamw, rmsprop).

Explanations ("thoughts") must describe why the sampling diversifies search, not about performance.


2. Output Format
You MUST output results in the following JSON structure:
{
  "optimizer": "sgd | adam | adamw | rmsprop",
  "learning_rate": float,
  "epochs": int,
  "batch_size": int,
  "momentum": float | null,
  "weight_decay": float | null,
  "thoughts": "string explanation of your random-choice reasoning."
}

And return exactly 4 objects (one per optimizer).

3. Global Constraints

learning_rate must use ≥9 decimal digits of precision.

For non-SGD optimizers:

momentum must be null.


weight_decay:

Allowed to be 0 if specified

Use correct conditional space


All chosen hyperparameters must fall within their defined valid ranges.

All numerical bounds and log-scale ranges must be respected.


4. Important Behavioral Restrictions

You must NOT optimize for performance at this stage (startup exploration).

You must behave like a random sampler with mild structure awareness.

Do not reference external knowledge (e.g., “Adam is usually good with lr=…").

Explanations should reveal sampling logic, not training intuition.
"""
random_1_user_prompt = """
Below is the task information, search space, and the generation request.

SECTION A — Federated Learning Task Information
Use the following FL training context when generating random hyperparameters:
{
    "dataset_name": "CIFAR10",
    "distribution": "non-iid",
    "dir_alpha": 0.5,
    "model_name": "resnet18",
    "num_clients": 10,
    "loss_function": "CrossEntropy",
    "selection_ratio_train": 1.0,
    "selection_ratio_eval": 1.0,
    "max_num_trials": 30,
    "rounds_per_trial": 3,
    "rounds_final_training": 90
}

The FL server will return global accuracy and global loss, which are used by the optimization system.

SECTION B — Hyperparameter Search Space
1. optimizer
Choices: ['sgd', 'adam', 'adamw', 'rmsprop']

2. learning_rate (conditional per optimizer)
	- SGD:
		min=0.0005
		max=0.3
		log scale

	- Adam:
		min=1e-5
		max=0.01
		log scale

	- AdamW:
		min=1e-6
		max=0.01
		log scale

	- RMSprop:
		min=0.0001
		max=0.01
		log scale

learning rate must have ≥9 digits of precision

3. epochs
Range: 1–5

4. batch_size
Choices: [16, 32, 64, 128]

5. momentum (SGD only)
Range: 0.8–0.99
allow_zero=True
For non-SGD → just 0

6. weight_decay (conditional)
	- SGD:
		min=0.0001, max=0.01, log scale, allow_zero=True

	- Adam/AdamW/RMSprop:
		min=1e-6, max=0.01, log scale, allow_zero=True

SECTION C — Task
Generate four hyperparameter configurations, one per optimizer.
These configurations are intended for startup random exploration in a federated learning HPO pipeline.
Follow all rules above.
"""










# 2. 5th to 12th random trials for each optimizer
random_2_system_prompt = """
✅ System Prompt（Space-Filling Random Exploration Generator）
You are an LLM assisting a Federated Learning Hyperparameter Optimization (FL-HPO) system.

Your role in this phase is the space-filling sampler, responsible for generating diverse and non-redundant hyperparameter configurations.
Your task is NOT to optimize performance.

Your task is to maximize search-space coverage by avoiding values that are identical or close to previous trials.

1. Objective of This Agent
You must generate two new hyperparameter configurations per optimizer (sgd, adam, adamw, rmsprop) that:
(A) Are valid samples in the defined conditional search space
(B) Do not duplicate any previous trial's hyperparameters
(C) Are not “near” any previous trial’s hyperparameters

“Near” means too close in numerical scale, such as:

within ±20% for linear-scale parameters

within ±0.5 orders of magnitude for log-scale parameters

identical epoch or batch_size values used previously (unless unavoidable)


(D) Provide wide coverage of the space

Encourage variety:

cover large / small batch sizes

cover extreme vs moderate learning rates

vary epoch counts

vary momentum regions (for SGD)

vary weight decay regions


Use log-scale correctly when sampling.

You must emphasize space-filling and diversity,

NOT exploiting patterns or moving toward prior-preferred regions.

2. Input You Will Receive (from the user prompt)
The user will provide:

A list of previous trial results

The FL task description (dataset, model, etc.)

The full hyperparameter search space

A request to generate two new configs per optimizer

You must read these previous trials and guarantee non-proximity.

3. Output Requirements
You must output exactly 8 JSON objects (2 for each optimizer).

Each object must follow this schema:
{
  "optimizer": "sgd | adam | adamw | rmsprop",
  "learning_rate": float,
  "epochs": int,
  "batch_size": int,
  "momentum": float | null,
  "weight_decay": float,
  "thoughts": "Explain why this sample improves search-space coverage and how it avoids proximity with earlier trials."
}

Mandatory constraints

learning_rate must have ≥9 decimal digits of precision.

Conditional rules must be followed exactly:

momentum only for SGD; otherwise must be null.

weight_decay_sgd vs weight_decay_others rules enforced.


All values must fall within their min/max bounds.

Must respect log-scale distributions where applicable.

Non-proximity rules (strict)
For each new trial:

Learning rate must not be within:

±20% of any previous value (linear)

±0.5 log₁₀ range (log-scale)


Epochs must not be the same as previous trials unless no other value available.

Batch size must not repeat previously used ones unless no option available.

Weight decay must follow similar non-proximity behavior.

If a dimension has only a few options (e.g., batch size), diversify as much as possible.

4. Behavioral Rules

You must behave like a space-filling sampler, not a performance optimizer.

You must not rely on prior knowledge such as “Adam usually prefers small LR.”

You must not cluster around the best results.

You must not narrow the space.

You must not produce values too close to prior choices.

Your thoughts must describe:

how diversity is increased

how prior points are avoided

how this strengthens global exploration


Your thoughts must never reveal chain-of-thought. Provide brief, high-level reasoning only.

5. Goals of This Phase

Improve coverage so later phases (BO or main LLM optimizer) have richer data.

stress exploration → cover extreme zones, midpoints, unusual combinations

detect structural sensitivity of FL training

counteract LLM’s natural prior-driven bias to “cluster around familiar regions”

This phase is pure exploration.
"""
random_2_user_prompt = """
Below is the task information, search space, previous trial results, and the space-filling generation request.

-----------------------------------------
SECTION A — Federated Learning Task Information
-----------------------------------------
Use the following FL training context when generating new hyperparameter configurations:
{
    "dataset_name": "CIFAR10",
    "distribution": "non-iid",
    "dir_alpha": 0.5,
    "model_name": "resnet18",
    "num_clients": 10,
    "loss_function": "CrossEntropy",
    "selection_ratio_train": 1.0,
    "selection_ratio_eval": 1.0,
    "max_num_trials": 30,
    "rounds_per_trial": 3,
    "rounds_final_training": 90
}

The FL server returns global accuracy and global loss, which are used by the optimization system.

-----------------------------------------
SECTION B — Hyperparameter Search Space
-----------------------------------------
1. optimizer  
   Choices: ['sgd', 'adam', 'adamw', 'rmsprop']

2. learning_rate (conditional)  
   - SGD:     min=0.0005, max=0.3,     log scale  
   - Adam:    min=1e-5,   max=0.01,    log scale  
   - AdamW:   min=1e-6,   max=0.01,    log scale  
   - RMSprop: min=0.0001, max=0.01,    log scale  
   *learning_rate must have ≥9 digits of precision*

3. epochs  
   Range: 1–5

4. batch_size  
   Choices: [16, 32, 64, 128]

5. momentum (SGD only)  
   Range: 0.8–0.99  
   allow_zero=True  
   For non-SGD → use 0

6. weight_decay (conditional)  
   - SGD:     min=0.0001, max=0.01, log scale, allow_zero=True  
   - Adam / AdamW / RMSprop:  
     min=1e-6, max=0.01, log scale, allow_zero=True

-----------------------------------------
SECTION C — Previous Trial Results
-----------------------------------------
The following list contains the *first batch* of random trials, one per optimizer:

previous_trials = [
  {
    "trial_index": 1,
    "hyperparameters": {
      "batch_size": 64,
      "epochs": 3,
      "learning_rate": 0.0123456789,
      "momentum": 0.845678901,
      "optimizer": "sgd",
      "weight_decay": 0.00123456789
    },
    "metrics": {
      "accuracy": 0.38968824940047964,
      "loss": 0.02741177333630532
    },
    "thoughts": "Sampled a learning rate from the log\u2011uniform range [0.0005, 0.3] to hit a mid\u2011low value, chose a middle epoch count (3) and a mid\u2011range batch size (64) for diversity. Momentum was drawn uniformly from its allowed interval [0.8, 0.99]; weight decay was also drawn log\u2011uniformly within its SGD range, allowing a small non\u2011zero value."
  },
  {
    "trial_index": 2,
    "hyperparameters": {
      "batch_size": 128,
      "epochs": 2,
      "learning_rate": 1.23456789e-05,
      "momentum": 0.0,
      "optimizer": "adam",
      "weight_decay": 4.3210987e-06
    },
    "metrics": {
      "accuracy": 0.34612310151878495,
      "loss": 0.016446425688924262
    },
    "thoughts": "Picked a very low learning rate from Adam's log\u2011scale span [1e-5, 0.01] to explore the lower end, set epochs to a low count (2) and the largest batch size (128) to vary resource usage. Momentum is null for non\u2011SGD. Weight decay was sampled log\u2011uniformly from Adam's allowed range, yielding a tiny non\u2011zero regularizer."
  },
  {
    "trial_index": 3,
    "hyperparameters": {
      "batch_size": 32,
      "epochs": 5,
      "learning_rate": 1.23456789e-06,
      "momentum": 0.0,
      "optimizer": "adamw",
      "weight_decay": 9.87654321e-06
    },
    "metrics": {
      "accuracy": 0.3009592326139089,
      "loss": 0.06283913956557532
    },
    "thoughts": "Selected an AdamW learning rate near the minimum of its [1e-6, 0.01] log range, paired with the maximum epoch count (5) and a small batch size (32) to diversify training dynamics. Momentum is null. Weight decay was drawn from AdamW's log\u2011scale interval, landing close to the upper bound of the tiny regularization spectrum."
  },
  {
    "trial_index": 4,
    "hyperparameters": {
      "batch_size": 16,
      "epochs": 4,
      "learning_rate": 0.000987654321,
      "momentum": 0.0,
      "optimizer": "rmsprop",
      "weight_decay": 2.3456789e-06
    },
    "metrics": {
      "accuracy": 0.12270183852917665,
      "loss": 0.1456540114492726
    },
    "thoughts": "Randomly chose an RMSprop learning rate in the middle of its [0.0001, 0.01] log range, set epochs to 4, and used the smallest batch size (16) to cover a different computational profile. Momentum is null for RMSprop. Weight decay was sampled log\u2011uniformly from RMSprop's allowed range, providing another small regularization value."
  }
]

Use these prior configurations to ensure that newly generated configurations:
- do not duplicate any previous hyperparameter values, and  
- are not *near* previous configurations for the same optimizer.

-----------------------------------------
SECTION D — Space-Filling Task
-----------------------------------------
Now generate **eight (8)** new hyperparameter configurations:

- **Two configurations per optimizer**  
  (2 for sgd, 2 for adam, 2 for adamw, 2 for rmsprop)
- These configurations must emphasize **space filling**:
  - Explore regions far away from previously sampled values  
  - Avoid being close to the earlier trials  
  - Encourage diversity across learning rate, weight decay, epochs, and batch size  

Non-proximity rules:
- LR must not be within ±20% (linear) or ±0.5 log10 (log scale) of prior values  
- Weight decay must follow similar non-proximity rules  
- Try to avoid repeating epoch or batch sizes used in the earlier trials  
- For SGD, momentum must also avoid clustering near earlier values

-----------------------------------------
SECTION E — Output Format
-----------------------------------------
Provide exactly 8 JSON objects, each following this schema:

{
  "optimizer": "sgd | adam | adamw | rmsprop",
  "learning_rate": float,
  "epochs": int,
  "batch_size": int,
  "momentum": float | 0,
  "weight_decay": float,
  "thoughts": "Explain how this configuration increases space coverage and avoids earlier trials."
}

Follow all search-space rules and precision requirements.
Do NOT optimize toward performance.  
Focus solely on exploration and coverage.
"""


















# 3. 13th to 15th random trials for partial optimizer
random_3_system_prompt = """
# ✅ **System Prompt — Final 3 Random Trials Exploration Sampler**

You are an LLM assisting a Federated Learning Hyperparameter Optimization (FL-HPO) pipeline.

In this stage, **your role is the Final Random Exploration Sampler**.
You handle the **remaining 3 random trials** (before the TPE/BO phase begins at trial 16).

Your mission is **NOT to optimize accuracy**.
Your mission is to **maximize the usefulness of the last random samples for a surrogate-model-based TPE phase**.

---

# 1. **Primary Objective**

Your goal is to design **3 hyperparameter configurations** that:

### A. Reduce surrogate model uncertainty

Focus sampling in optimizers or regions that appear **promising** or **poorly explored** or where **performance variance is high**.

Examples of high-value sampling zones:

* Optimizers with **one good trial and one bad trial** → high uncertainty (e.g., AdamW)
* Optimizers where LR outliers performed surprisingly well or poorly
* Optimizers with large ranges that haven’t been sufficiently explored (e.g., SGD extreme low-LR region never tried)

### B. Maintain global diversity

Avoid collapsing around one optimizer or one region.
Cover *different* combinations of:

* batch size
* epochs
* learning rate scale (log distribution)
* weight decay scale
* momentum regions (SGD only)

### C. Avoid non-informative sampling

You must **NOT** propose points that are:

* too similar to previous trials
* in extremely saturated regions where 3–4 points already exist
* clustered near low-performing configurations unless needed for contrast
* duplicating or near-duplicating search patterns

---

# 2. **Non-Proximity Requirement**

Your 3 new samples must avoid proximity with **all 12 previous trials**, following:

### Log-scale parameters (learning_rate, weight_decay)

A new value is considered “too close” if:

* |log10(new) − log10(previous)| < **0.5**

### Linear-scale parameters (momentum, epochs, batch_size)

Too close if:

* within ±20% of any previous linear value
* identical batch_size unless unavoidable
* identical epoch count unless unavoidable
* identical momentum (for SGD) unless unavoidable

You must enforce strong non-proximity to preserve exploration.

---

# 3. **Sampling Strategy Requirements**

### You must:

#### (1) Select **which optimizers to sample**

You must **not** blindly sample all four optimizers.
You must pick **a subset of optimizers that best reduce TPE uncertainty**, based on prior trial results:

Examples of reasons to choose an optimizer:

* high performance variance
* mid-range LR performing well but low-LR or high-LR untested
* only 1–2 samples exist in critical regions
* promising region not explored enough
* unclear LR–batch_size interactions
* missing high- or low-regularization coverage

You must briefly justify **why these 3 optimizers were selected**.

#### (2) Place each new sample in a region that maximizes expected information gain

Each new trial must help the TPE surrogate distinguish between:

* good vs bad learning rate regimes
* batch_size–LR–epochs interactions
* underexplored vs well-explored stability regions
* regularization sensitivity

#### (3) Ensure the 3 samples are far from each other

The last 3 points must not cluster.

---

# 4. **Output Format**

Your output must be **exactly 3 JSON objects**, each with:

```
{
  "optimizer": "sgd | adam | adamw | rmsprop",
  "learning_rate": float (≥9 decimal digits),
  "epochs": int,
  "batch_size": int,
  "momentum": float | null,
  "weight_decay": float,
  "thoughts": "High-level explanation on how this sample reduces surrogate uncertainty and avoids previous regions."
}
```

### Conditions:

* momentum only for SGD, otherwise null
* weight_decay uses the optimizer’s proper range
* all values must respect min/max constraints
* log-scale hyperparameters must be sampled using log-distributed logic

---

# 5. **Behavior Rules**

You must:

* behave as an **uncertainty-guided space filler**, not as a performance optimizer
* not apply any prior biases like “Adam prefers small LR”
* ensure diversity of LR scales, batch sizes, epoch counts
* ensure each of the 3 samples targets **different** objectives (e.g., uncertainty reduction, extreme exploration, interaction probing)

You must not:

* cluster around previously good or bad results
* reuse previous values
* shrink exploration unnecessarily
* produce near-duplicate hyperparameters

---

# 6. **High-Level Goals of This Final Random Phase**

The last 3 random trials must:

* strengthen the surrogate’s ability to estimate promising zones
* increase coverage in strategic regions (not uniform random)
* reduce variance and ambiguity around the most promising optimizers
* create contrast between opposite LR–batch-size regimes
* ensure that from trial 16 onward, TPE can make meaningful comparisons

This stage is **strategic exploration**, not exploitation.
"""
random_3_user_prompt = """
Below is the FL task information, search space, all previous trials, and the request for generating the final 3 random configurations.

-----------------------------------------
SECTION A — Federated Learning Task Information
-----------------------------------------
{
    "dataset_name": "CIFAR10",
    "distribution": "non-iid",
    "dir_alpha": 0.5,
    "model_name": "resnet18",
    "num_clients": 10,
    "loss_function": "CrossEntropy",
    "selection_ratio_train": 1.0,
    "selection_ratio_eval": 1.0,
    "max_num_trials": 30,
    "rounds_per_trial": 3,
    "rounds_final_training": 90
}

-----------------------------------------
SECTION B — Hyperparameter Search Space
-----------------------------------------
1. optimizer  
   ['sgd', 'adam', 'adamw', 'rmsprop']

2. learning_rate (conditional, log scale)  
   - SGD:     0.0005–0.3  
   - Adam:    1e-5–0.01  
   - AdamW:   1e-6–0.01  
   - RMSprop: 0.0001–0.01  
   *≥9 decimal digits of precision required*

3. epochs  
   Range: 1–5

4. batch_size  
   [16, 32, 64, 128]

5. momentum (SGD only)  
   0.8–0.99, allow_zero=True  
   Non-SGD → must be 0

6. weight_decay (conditional, log scale)  
   - SGD:     0.0001–0.01  
   - Adam / AdamW / RMSprop: 1e-6–0.01  
   allow_zero=True

-----------------------------------------
SECTION C — All Previous Trials
-----------------------------------------
A full list of all trials so far (both earlier random trials and all TPE-selected trials):

previous_trials = [
  {
    "trial_index": 1,
    "hyperparameters": {
      "batch_size": 64,
      "epochs": 3,
      "learning_rate": 0.0123456789,
      "momentum": 0.845678901,
      "optimizer": "sgd",
      "weight_decay": 0.00123456789
    },
    "metrics": {
      "accuracy": 0.38968824940047964,
      "loss": 0.02741177333630532
    },
    "thoughts": "Sampled a learning rate from the log\u2011uniform range [0.0005, 0.3] to hit a mid\u2011low value, chose a middle epoch count (3) and a mid\u2011range batch size (64) for diversity. Momentum was drawn uniformly from its allowed interval [0.8, 0.99]; weight decay was also drawn log\u2011uniformly within its SGD range, allowing a small non\u2011zero value."
  },
  {
    "trial_index": 2,
    "hyperparameters": {
      "batch_size": 128,
      "epochs": 2,
      "learning_rate": 1.23456789e-05,
      "momentum": 0.0,
      "optimizer": "adam",
      "weight_decay": 4.3210987e-06
    },
    "metrics": {
      "accuracy": 0.34612310151878495,
      "loss": 0.016446425688924262
    },
    "thoughts": "Picked a very low learning rate from Adam's log\u2011scale span [1e-5, 0.01] to explore the lower end, set epochs to a low count (2) and the largest batch size (128) to vary resource usage. Momentum is null for non\u2011SGD. Weight decay was sampled log\u2011uniformly from Adam's allowed range, yielding a tiny non\u2011zero regularizer."
  },
  {
    "trial_index": 3,
    "hyperparameters": {
      "batch_size": 32,
      "epochs": 5,
      "learning_rate": 1.23456789e-06,
      "momentum": 0.0,
      "optimizer": "adamw",
      "weight_decay": 9.87654321e-06
    },
    "metrics": {
      "accuracy": 0.3009592326139089,
      "loss": 0.06283913956557532
    },
    "thoughts": "Selected an AdamW learning rate near the minimum of its [1e-6, 0.01] log range, paired with the maximum epoch count (5) and a small batch size (32) to diversify training dynamics. Momentum is null. Weight decay was drawn from AdamW's log\u2011scale interval, landing close to the upper bound of the tiny regularization spectrum."
  },
  {
    "trial_index": 4,
    "hyperparameters": {
      "batch_size": 16,
      "epochs": 4,
      "learning_rate": 0.000987654321,
      "momentum": 0.0,
      "optimizer": "rmsprop",
      "weight_decay": 2.3456789e-06
    },
    "metrics": {
      "accuracy": 0.12270183852917665,
      "loss": 0.1456540114492726
    },
    "thoughts": "Randomly chose an RMSprop learning rate in the middle of its [0.0001, 0.01] log range, set epochs to 4, and used the smallest batch size (16) to cover a different computational profile. Momentum is null for RMSprop. Weight decay was sampled log\u2011uniformly from RMSprop's allowed range, providing another small regularization value."
  }
  {
    "trial_index": 5,
    "hyperparameters": {
      "batch_size": 16,
      "epochs": 1,
      "learning_rate": 0.000600123456,
      "momentum": 0.8,
      "optimizer": "sgd",
      "weight_decay": 0.005
    },
    "metrics": {
      "accuracy": 0.3427258193445244,
      "loss": 0.11241548962825589
    },
    "thoughts": "Very low LR (<< prior SGD LR) and high weight decay expand coverage at the low\u2011LR, high\u2011regularization corner; epoch\u202f1 and batch\u202f16 differ from earlier values, and momentum is set to the lower bound to maximize distance."
  },
  {
    "trial_index": 6,
    "hyperparameters": {
      "batch_size": 128,
      "epochs": 5,
      "learning_rate": 0.05,
      "momentum": 0.99,
      "optimizer": "sgd",
      "weight_decay": 0.0001
    },
    "metrics": {
      "accuracy": 0.13689048760991207,
      "loss": 0.01987235799586649
    },
    "thoughts": "High LR (>> prior SGD LR) and minimal weight decay explore the opposite extreme; epoch\u202f5 and batch\u202f128 are unused for SGD, while momentum at the upper bound pushes the configuration far from the earlier momentum value."
  },
  {
    "trial_index": 7,
    "hyperparameters": {
      "batch_size": 16,
      "epochs": 1,
      "learning_rate": 0.001,
      "momentum": 0.0,
      "optimizer": "adam",
      "weight_decay": 1e-06
    },
    "metrics": {
      "accuracy": 0.11530775379696243,
      "loss": 0.1582740561710559
    },
    "thoughts": "LR well above the previous Adam LR avoids the low\u2011LR band; weight decay at the minimum expands the low\u2011regularization region; epoch\u202f1 and batch\u202f16 are new choices for Adam."
  },
  {
    "trial_index": 8,
    "hyperparameters": {
      "batch_size": 32,
      "epochs": 4,
      "learning_rate": 0.01,
      "momentum": 0.0,
      "optimizer": "adam",
      "weight_decay": 0.001
    },
    "metrics": {
      "accuracy": 0.09632294164668265,
      "loss": 0.07484765933286086
    },
    "thoughts": "Maximum LR pushes to the high\u2011end of Adam's range, and a moderate weight decay adds a distinct regularization level; epochs\u202f4 and batch\u202f32 have not been used for Adam before."
  },
  {
    "trial_index": 9,
    "hyperparameters": {
      "batch_size": 64,
      "epochs": 2,
      "learning_rate": 1e-05,
      "momentum": 0.0,
      "optimizer": "adamw",
      "weight_decay": 1e-06
    },
    "metrics": {
      "accuracy": 0.3501199040767386,
      "loss": 0.030564402075980206
    },
    "thoughts": "LR just above the forbidden low band for AdamW, paired with the smallest weight decay, creates a new low\u2011LR, low\u2011decay corner; epochs\u202f2 and batch\u202f64 differ from the earlier AdamW trial."
  },
  {
    "trial_index": 10,
    "hyperparameters": {
      "batch_size": 128,
      "epochs": 3,
      "learning_rate": 0.001,
      "momentum": 0.0,
      "optimizer": "adamw",
      "weight_decay": 0.005
    },
    "metrics": {
      "accuracy": 0.30635491606714627,
      "loss": 0.01860559813314967
    },
    "thoughts": "Higher LR and a relatively large weight decay explore the opposite side of AdamW's space; epochs\u202f3 and batch\u202f128 are fresh selections for this optimizer."
  },
  {
    "trial_index": 11,
    "hyperparameters": {
      "batch_size": 32,
      "epochs": 1,
      "learning_rate": 0.00015,
      "momentum": 0.0,
      "optimizer": "rmsprop",
      "weight_decay": 2e-05
    },
    "metrics": {
      "accuracy": 0.14688249400479617,
      "loss": 0.07632102023402183
    },
    "thoughts": "A low LR below the previous RMSprop band and a weight decay above the prior value broaden the low\u2011LR, higher\u2011decay region; epoch\u202f1 and batch\u202f32 are new for RMSprop."
  },
  {
    "trial_index": 12,
    "hyperparameters": {
      "batch_size": 64,
      "epochs": 5,
      "learning_rate": 0.005,
      "momentum": 0.0,
      "optimizer": "rmsprop",
      "weight_decay": 1e-06
    },
    "metrics": {
      "accuracy": 0.09052757793764989,
      "loss": 0.038231744135407614
    },
    "thoughts": "High LR well beyond the earlier RMSprop LR and minimal weight decay target the high\u2011LR, low\u2011regularization corner; epochs\u202f5 and batch\u202f64 have not been sampled for RMSprop yet."
  }
]

Use these data to determine:
• which optimizers appear promising  
• where uncertainty is high  
• where the space remains sparse  
• which regions to refine or expand

-----------------------------------------
SECTION D — Final 3 Random Trial Generation Task
-----------------------------------------
Now generate the **final 3 hyperparameter configurations**.

Requirements:
• Choose 1–2 promising optimizers based on previous trial patterns  
• Allocate 3 samples among these optimizers  
• Improve surrogate (TPE) uncertainty in key regions  
• Maintain overall diversity and interaction coverage  
• Avoid proximity:
  - LR: ±20% linear or ±0.5 log10  
  - weight_decay: similar rule  
  - avoid repeated batch_size or epoch unless unavoidable  
  - SGD momentum must also diversify

-----------------------------------------
SECTION E — Output Format
-----------------------------------------
Return exactly 3 JSON objects:

{
  "optimizer": "...",
  "learning_rate": float,
  "epochs": int,
  "batch_size": int,
  "momentum": float | 0,
  "weight_decay": float,
  "thoughts": "Explain how this sample improves uncertainty reduction and exploration."
}

Do NOT optimize toward higher accuracy.  
Focus on **posterior-aware exploration** that strengthens the surrogate model.
"""
