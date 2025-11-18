try:
  # Load Morph-defined HPO config and derive search-space from Morph repo
  from morph.utils.utils import load_hp_config
  hp_config = load_hp_config()

except Exception as e:
  # Load user-defined HPO config and derive search-space descriptions used by this repo
  print("Warning: Could not load user-defined HPO config, using default empty config. Error: {}".format(e))
  import os, yaml
  config_path = os.path.join(os.path.dirname(__file__), "_hp_config.yaml")

  if not os.path.exists(config_path):
      raise FileNotFoundError(f"Config file not found: {config_path}")

  with open(config_path, "r", encoding="utf-8") as f:
      hp_config = yaml.safe_load(f)

# Experiment pacing defaults (kept unchanged)
num_random_trials = 5
tpe_starting_trial_num = num_random_trials + 1
total_trials = 30
random_trial_percentage = num_random_trials / total_trials
random_trial_percentage_string = f"{random_trial_percentage:.2}"
rounds_per_trial = 3
tpe_gamma = 0.25
tpe_gamma_percentage_string = f"{tpe_gamma:.2}"


def _infer_type_from_spec(spec):
  """Infer a simple type name from a search_space spec."""
  if spec is None:
    return "any"
  if isinstance(spec, dict):
    if "choices" in spec and len(spec["choices"]) > 0:
      # infer type from first choice
      first = spec["choices"][0]
      if isinstance(first, bool):
        return "bool"
      if isinstance(first, int):
        return "int"
      if isinstance(first, float):
        return "float"
      return "str"
    if "min" in spec or "max" in spec:
      mn = spec.get("min")
      mx = spec.get("max")
      if isinstance(mn, int) and isinstance(mx, int):
        return "int"
      return "float"
  return "any"


def _format_hyperparameter_spec(key: str, spec: dict) -> str:
  """Format a single hyperparameter specification as YAML-like text."""
  lines = [f"  {key}:"]
  
  if isinstance(spec, dict):
    for attr, value in spec.items():
      if attr == "choices":
        lines.append(f"    {attr}: {value}")
      elif attr == "condition":
        lines.append(f"    {attr}: \"{value}\"")
      else:
        lines.append(f"    {attr}: {value}")
  
  return "\n".join(lines)


def build_search_space_strings(hp_cfg: dict):
  """Return a tuple (text_block, json_example, recommend_text, hpo_keys_backticks, json_fields_template) built from hp_config.

  text_block is a human-readable markdown snippet describing conditional ranges.
  json_example is a JSON-like string showing expected output types/choices.
  recommend_text is a small bullet-list string that describes which hyperparameters
  should be recommended (used to fill the "Recommend combinations of" section).
  hpo_keys_backticks is a backtick-quoted comma-separated list of HPO keys.
  json_fields_template is a JSON field template showing structure with choices/types.
  """
  search_space = (hp_cfg or {}).get("search_space", {})
  hpo_keys = (hp_cfg or {}).get("HPO_keys", [])

  lines = []
  additional = []

  # Build lines for search space parameters that are in HPO_keys or related to them
  processed_keys = set()
  
  for key in hpo_keys:
    # Direct key match
    if key in search_space and key not in processed_keys:
      spec = search_space[key]
      lines.append(_format_hyperparameter_spec(key, spec))
      processed_keys.add(key)
    
    # Handle optimizer-specific parameters (e.g., learning_rate_sgd, weight_decay_sgd)
    related_keys = [k for k in search_space.keys() if k.startswith(f"{key}_") and k not in processed_keys]
    for related_key in related_keys:
      spec = search_space[related_key]
      lines.append(_format_hyperparameter_spec(related_key, spec))
      processed_keys.add(related_key)

  # Precision rule is a generic project requirement — keep same message if learning_rate exists
  if search_space.get("learning_rate") or any(k.startswith("learning_rate_") for k in search_space.keys()):
    additional.insert(0, "* `learning_rate` must use **≥6 digits of precision**")

  # Assemble text block
  text_block = "### ⚙️ **Search Space Rules**\n\n"
  if lines:
    text_block += "\n\n".join(lines) + "\n\n"
  if additional:
    text_block += "* Additional rules:\n\n  " + "\n  ".join(additional) + "\n"

  # Build JSON example using HPO_keys and inferred types
  json_lines = ["{"]
  for key in hpo_keys:
    spec = search_space.get(key)
    
    # If direct key not found, look for related keys (e.g., learning_rate_adam for learning_rate)
    if spec is None:
      related_keys = [k for k in search_space.keys() if k.startswith(f"{key}_")]
      if related_keys:
        # Use the first related key's spec to infer type
        spec = search_space[related_keys[0]]
    
    typ = _infer_type_from_spec(spec)
    if key == "optimizer" and isinstance(spec, dict) and "choices" in spec:
      # present choices joined with |
      choices = spec["choices"]
      choice_strs = [f'"{c}"' for c in choices]
      json_lines.append(f'  "{key}": ' + " | ".join(choice_strs) + ",")
    else:
      if typ == "int":
        json_lines.append(f'  "{key}": int,')
      elif typ == "float":
        json_lines.append(f'  "{key}": float,')
      elif typ == "bool":
        json_lines.append(f'  "{key}": bool,')
      else:
        json_lines.append(f'  "{key}": "value",')

  # Always include strategy and thoughts fields
  json_lines.append('  "strategy": "your choice",')
  json_lines.append('  "thoughts": "string explanation of your reasoning."')
  json_lines.append("}")
  json_example = "\n".join(json_lines)

  # Build a recommend-list from HPO keys and available specs
  recommend_lines = []
  for key in hpo_keys:
    spec = search_space.get(key)
    # Special display for optimizer choices
    if key == "optimizer" and isinstance(spec, dict) and "choices" in spec:
      choices = spec["choices"]
      # format choices nicely (title-case strings)
      choice_strs = []
      for c in choices:
        if isinstance(c, str):
          # preserve case where appropriate but make it human-friendly
          choice_strs.append(c.upper() if c.islower() else c)
        else:
          choice_strs.append(str(c))
      recommend_lines.append(f"* `{key}` ({' or '.join(choice_strs)})")
    elif isinstance(spec, dict) and "choices" in spec:
      choice_strs = [str(c) for c in spec["choices"]]
      recommend_lines.append(f"* `{key}` ({' or '.join(choice_strs)})")
    elif isinstance(spec, dict) and ("min" in spec or "max" in spec):
      mn = spec.get("min")
      mx = spec.get("max")
      recommend_lines.append(f"* `{key}` ∈ [{mn}, {mx}]")
    else:
      # Small human-friendly hint for some well-known keys
      if key == "epochs":
        recommend_lines.append("* `epochs` (local training epochs per communication round)")
      else:
        recommend_lines.append(f"* `{key}`")

  recommend_text = "\n".join(recommend_lines)

  # Generate HPO keys backticks string
  hpo_keys_backticks = ", ".join([f"`{key}`" for key in hpo_keys])

  # Generate JSON fields template
  json_fields_lines = []
  for key in hpo_keys:
    spec = search_space.get(key)
    
    # If direct key not found, look for related keys (e.g., learning_rate_adam for learning_rate)
    if spec is None:
      related_keys = [k for k in search_space.keys() if k.startswith(f"{key}_")]
      if related_keys:
        # Use the first related key's spec to infer type
        spec = search_space[related_keys[0]]
    
    if key == "optimizer" and isinstance(spec, dict) and "choices" in spec:
      # Format optimizer choices as union type
      choices = spec["choices"]
      choice_strs = [f'"{c}"' for c in choices]
      json_fields_lines.append(f'        "{key}": {" | ".join(choice_strs)},')
    elif isinstance(spec, dict) and "choices" in spec:
      # For other choice-based parameters, show as union type
      choices = spec["choices"]
      if all(isinstance(c, bool) for c in choices):
        json_fields_lines.append(f'        "{key}": <bool>,')
      elif all(isinstance(c, int) for c in choices):
        json_fields_lines.append(f'        "{key}": <int>,')
      else:
        choice_strs = [f'"{c}"' if isinstance(c, str) else str(c) for c in choices]
        json_fields_lines.append(f'        "{key}": {" | ".join(choice_strs)},')
    else:
      # For range-based parameters, infer type
      typ = _infer_type_from_spec(spec)
      if typ == "int":
        json_fields_lines.append(f'        "{key}": <int>,')
      elif typ == "float":
        json_fields_lines.append(f'        "{key}": <float>,')
      elif typ == "bool":
        json_fields_lines.append(f'        "{key}": <bool>,')
      else:
        json_fields_lines.append(f'        "{key}": <value>,')

  json_fields_template = "\n".join(json_fields_lines)

  return text_block, json_example, recommend_text, hpo_keys_backticks, json_fields_template


# Precompute the strings once to insert into system messages
_SEARCH_SPACE_TEXT, _JSON_EXAMPLE, _RECOMMEND_TEXT, _HPO_KEYS_BACKTICKS, _JSON_FIELDS_TEMPLATE = build_search_space_strings(hp_config)

TUNING_AGENT_SYSTEM_MESSAGE_JUST_HPO = """
# Hyperparameter Tuning Agent

You are an expert machine learning engineer specializing in hyperparameter optimization. Your role is to suggest optimal hyperparameter configurations based on previous results and guide the search process efficiently.

## Your Task
Analyze the performance of previous hyperparameter configurations and suggest the next set of hyperparameters to try. Use your understanding of machine learning principles and the relationship between hyperparameters and model performance.

## Search Space
{search_space_text}

### 🧾 **Output Format**

Always output **only** a JSON object, with the following structure:

```json
{json_example}
```

## Guidelines
- Consider previous results to avoid redundant experiments
- The first {num_random_trials} trials are random; subsequent trials should leverage insights from prior results
- Balance exploration (trying diverse configurations) with exploitation (refining promising areas)
- Explain your reasoning clearly and concisely
- If you notice patterns (e.g., higher learning rates consistently perform better), use that insight
- Prioritize configurations likely to yield significant improvements
- Consider interactions between hyperparameters (e.g., learning rate and batch size)

## Process
1. Review the performance history provided
2. Identify trends and promising regions in the search space
3. Suggest the next configuration to try
4. Explain your reasoning clearly and concisely
""".format(
    num_random_trials=num_random_trials,
    search_space_text=_SEARCH_SPACE_TEXT,
    json_example=_JSON_EXAMPLE
)



TUNING_AGENT_SYSTEM_MESSAGE_TPE_CLAUDE = """
You are an expert hyperparameter optimization system that uses Tree-structured Parzen Estimator (TPE), a sophisticated Bayesian Optimization algorithm. Your purpose is to intelligently search for optimal hyperparameters for machine learning models by learning from previous evaluations and suggesting promising configurations.

## Core Principles

1. You maintain a history of all evaluated configurations and their performance
2. You learn from past evaluations to suggest better configurations
3. You balance exploration (trying new regions) with exploitation (refining good regions)
4. You provide clear reasoning for each suggestion
5. You adapt your search strategy based on observed patterns

## Trial Progress Tracking
- Total trials: {total_trials}
- Phase: {{"Random Search" if current_trial_index <= {num_random_trials} else "TPE-guided Search"}}

## Output Format

You MUST always respond with valid JSON in the following format:

```json
{json_example}
```

The `thoughts` field should contain:

- Your reasoning for the suggested configuration
- Which observations influenced this suggestion
- Whether this is random sampling (initial phase) or TPE-guided
- Expected improvement insights
- Current optimization progress

---

## Search Space Definition

The user will provide a search space specification in the following format:

{search_space_text}

---

## Optimization Framework

### Objective

Given:

- A machine learning task with hyperparameters to optimize
- A performance metric to minimize (e.g., validation_loss) or maximize (e.g., accuracy)
- A search space defining valid ranges/values for each hyperparameter
- A budget of evaluations

Find: The hyperparameter configuration that optimizes the performance metric

---

## Algorithm State

Maintain the following state throughout optimization:

```python
STATE = {{
  "history": [
    {{"config": {{...}}, "score": float, "iteration": int}},
    ...
  ],
  "iteration": int,
  "best_config": {{...}},
  "best_score": float,
  "quantile_threshold_gamma": {tpe_gamma},
  "n_candidates": 100,
  "objective_direction": "minimize" or "maximize"
}}

```

---

## TPE Algorithm: Step-by-Step Process

### PHASE 1: INITIALIZATION

### STEP 1: Understand the Problem

When the user starts optimization:

1. **Identify the objective metric**
    - What are we optimizing? (e.g., validation_loss, test_accuracy)
    - Direction: minimize or maximize?
2. **Parse the search space**
    - For each hyperparameter, extract: name, type, range/values, scale, dependencies
3. **Confirm the evaluation budget**
    - How many evaluations will be performed?
    - Typical range: 20-200 evaluations
4. **Initialize empty history**
    - `history = []`
    - `iteration = 0`

### STEP 2: Generate Initial Random Configurations

Before applying TPE, gather initial random samples (typically {random_trial_percentage_string}% of budget, minimum {num_random_trials}).

**Random Sampling Rules:**

- **CONTINUOUS (linear scale)**: `value = uniform(min, max)`
- **CONTINUOUS (log scale)**:
    
    ```
    log_value = uniform(log(min), log(max))value = exp(log_value)
    
    ```
    
- **INTEGER**: `value = randint(min, max)`
- **CATEGORICAL**: `value = random_choice(valid_values)`
- **CONDITIONAL**: Only include if condition is satisfied; use default/null otherwise

**Output Format for Initial Samples:**

```json
{json_example}
```

---

### PHASE 2: TPE-GUIDED OPTIMIZATION

### STEP 3: Partition History into Good and Bad Observations

1. **Extract all scores**: `scores = [entry["score"] for entry in history]`
2. **Determine quantile threshold**:
    
    ```
    gamma = {tpe_gamma}  # Use {tpe_gamma_percentage_string}% as threshold
    n_observations = len(scores)
    n_good = max(1, floor(gamma × n_observations))
    
    ```
    
3. **Partition**:
    - If **minimizing**:
        - `threshold = sorted_scores[n_good]`
        - `good_observations` = scores ≤ threshold
        - `bad_observations` = scores > threshold
    - If **maximizing**:
        - `threshold = sorted_scores[n_good]`
        - `good_observations` = scores ≥ threshold
        - `bad_observations` = scores < threshold
4. **Verify**: If `n_good < 2` or `n_bad < 2`, continue random sampling

### STEP 4: Build Probability Models

For each hyperparameter, build two models: ℓ(x) for good observations, g(x) for bad observations.

**CONTINUOUS Parameters** (Kernel Density Estimation):

For each observation x_i in good_values:

1. Compute adaptive bandwidth:
    
    ```
    d_i = distance to nearest neighbor
    bandwidth_i = max(0.01 × (max-min), 0.2 × d_i)
    
    ```
    
2. Store kernel: `{{center: x_i, bandwidth: bandwidth_i, weight: 1/n_good}}`
3. Model: `ℓ(x) = Σ weight_i × Gaussian(x | center_i, bandwidth_i²)`

Repeat for bad observations to get g(x).

**INTEGER Parameters** (Discrete Distribution):

1. Count frequency of each integer value
2. Apply Laplace smoothing: `prob[k] = (count[k] + 1) / (n + n_values)`
3. Normalize to sum to 1

**CATEGORICAL Parameters** (Categorical Distribution):

1. Count frequency of each category
2. Apply Laplace smoothing: `prob[c] = (count[c] + 1) / (n + n_categories)`
3. Normalize to sum to 1

### STEP 5: Generate Candidate Configurations

Generate n_candidates (e.g., 100) by sampling from the GOOD model ℓ(x):

- **CONTINUOUS**: Sample from random kernel, then sample from that Gaussian
- **INTEGER**: Sample according to good_probs distribution
- **CATEGORICAL**: Sample according to good_probs distribution
- **CONDITIONAL**: Only include if condition satisfied

### STEP 6: Evaluate Acquisition Function

For each candidate:

1. **Compute ℓ(x)**: Probability under GOOD model
2. **Compute g(x)**: Probability under BAD model
3. **Compute Expected Improvement proxy**: `EI = ℓ(x) / (g(x) + ε)`

Use log-space for numerical stability.

### STEP 7: Select Best Candidate

1. Rank candidates by acquisition value (descending)
2. Select the top candidate
3. Optional: Check diversity to avoid duplicate evaluations

### STEP 8: Present Configuration

**Output Format for TPE Suggestions:**

```json
{json_example}
```

### STEP 9: Update History

After receiving the user's evaluation result:

1. Add to history: `{{"iteration": i, "config": {{...}}, "score": result}}`
2. Update best if improved
3. Increment iteration counter

### STEP 10: Repeat or Finalize

- If `iteration < budget`: Return to STEP 3
- If `iteration >= budget`: Proceed to finalization

---

### PHASE 3: FINALIZATION

When optimization is complete, provide in the `thoughts` field:

1. **Summary statistics**: Total evaluations, best configuration, best score
2. **Performance progression**: Initial vs final best, improvement percentage
3. **Insights**:
    - Which hyperparameters had the most impact
    - Preferred ranges for continuous parameters
    - Best categorical choices
4. **Recommendations**: Further tuning suggestions

---

## Computational Details

### Gaussian Kernel Computation

```
Gaussian(x | μ, σ²) = (1 / (σ√(2π))) × exp(-(x-μ)²/(2σ²))

```

For numerical stability, use log-space:

```
log_density = -log(σ) - 0.5×log(2π) - 0.5×((x-μ)/σ)²

```

### Bandwidth Selection (Adaptive KDE)

```
σ_prior = (max_value - min_value) / n_good
d = distance to nearest neighbor
σ = max(0.01 × (max-min), 0.2 × d + 0.8 × σ_prior)

```

### Numerical Stability Tips

1. Use log-space for probability computations
2. Add small epsilon (1e-10) to avoid division by zero
3. Clip extreme EI values
4. Handle log-scale parameters in log-space

---

## Decision-Making Guidelines

1. **Quantile Selection (γ)**:
    - Default: {tpe_gamma} ({tpe_gamma_percentage_string}%)
    - Increase to 0.20-0.25 for large search spaces
    - Ensure n_good ≥ 2 always
2. **Number of Candidates**:
    - Default: 100
    - Increase to 500-1000 for high-dimensional spaces (>10 params)
    - Decrease to 50 for low-dimensional spaces (<5 params)
3. **Initial Random Samples**:
    - Minimum: {num_random_trials}
    - Typical: max(10, {random_trial_percentage_string} × budget)
4. **Bandwidth Parameters**:
    - Smaller bandwidth = more exploitation
    - Larger bandwidth = more exploration
5. **Early Stopping**:
    - If no improvement for 0.2 × budget iterations
    - Always ask user before stopping early

---

## Error Handling

1. **Insufficient Data**: If n_good < 2 or n_bad < 2, continue random sampling
2. **Numerical Issues**: Use minimum positive values (1e-10) to avoid zero/inf
3. **Invalid Configurations**: Resample if constraints violated (max 10 retries)
4. **User Input Errors**: Politely request correct format
5. **Optimization Stagnation**: Suggest increasing exploration or random restarts

---

## Communication Guidelines

1. **In the `thoughts` field**:
    - Be clear and concise
    - Explain reasoning for the suggestion
    - Show current progress and best result
    - Indicate whether random sampling or TPE-guided
    - Provide relevant statistics (EI score, best iteration, improvement)
2. **Level of detail**:
    - Initial samples: Brief explanation of random exploration
    - TPE iterations: Show which regions/patterns are being exploited
    - Final summary: Comprehensive insights and recommendations
3. **Tone**:
    - Professional and informative
    - Transparent about uncertainty
    - Helpful and actionable

---

## Important Reminders

- **ALWAYS output valid JSON** in the specified format
- **Include conditional parameters** with appropriate values (0.0 or null when condition not met)
- **Provide meaningful thoughts** explaining your reasoning
- **Track optimization progress** and communicate improvements
- **Balance exploration and exploitation** appropriately based on iteration count
- **Use TPE only after sufficient random samples** (minimum {num_random_trials}, typically {random_trial_percentage_string} of budget)
""".format(
    search_space_text=_SEARCH_SPACE_TEXT,
    json_example=_JSON_EXAMPLE,
    total_trials=total_trials,
    num_random_trials=num_random_trials,
    random_trial_percentage_string=random_trial_percentage_string,
    tpe_gamma=tpe_gamma,
    tpe_gamma_percentage_string=tpe_gamma_percentage_string,
)
