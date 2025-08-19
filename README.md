# LLM Bayesian Optimization Ability Evaluation

This project evaluates the ability of Large Language Models (LLMs) to solve Bayesian Optimization problems. It tests various LLMs on predefined problem sets and generates detailed results for analysis.

## Features

- Test multiple LLMs on Bayesian Optimization problems
- Support for different problem set sizes (24 or 100 problems)
- Configurable output and result tracking
- Debug mode with limited problem testing

## Supported LLMs

- **gpt**: OpenAI GPT models
- **gemini**: Google Gemini models  
- **claude**: Anthropic Claude models
- **deepseek**: DeepSeek models
- **qwen**: Qwen models (default)

Note: check `src/llm_bo_ability_eval/llm_configs.py`

## Problem Sets

The project includes two problem sets:
- `src/llm_bo_ability_eval/problem_set/24problems/` - 24 Bayesian Optimization harder problems
- `src/llm_bo_ability_eval/problem_set/100problems/` - 100 Bayesian Optimization easy problems

## Requirements

- Python 3.10 or higher
- Required packages listed in `requirements.txt`
- API keys for the LLM services you want to use

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd LLM_Bayesian_Optimization_Ability_Evaluation
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys as environment variables (see Setup section below)

## Usage

### Basic Usage

Run all problems in the 24-problem set using Qwen:
```bash
cd src/llm_bo_ability_eval
export OPENAI_API_KEY=dummy_api_key
python main.py -l qwen -e 24
```

Run all problems in the 100-problem set using Gemini:
```bash
cd src/llm_bo_ability_eval
export OPENAI_API_KEY=<your_google_api_key>
python main.py -l gemini -e 100
```

### Testing Mode

Run only the first 2 problems for testing:
```bash
cd src/llm_bo_ability_eval
export OPENAI_API_KEY=<your_google_api_key>
python main.py -l gemini -e 100 -m 2
```

### Command Line Arguments

- `-l, --llm`: LLM to test (choices: gpt, gemini, claude, deepseek, qwen) [default: qwen]
- `-e, --experiment`: Problem set size (choices: 24, 100) [default: 24]
- `-p, --problems`: Path to problem set directory [default: problem_set/24problems]
- `-o, --output`: Output directory for results [default: results/]
- `-m, --max-files`: Maximum number of files to test (for debugging)

## Output

Results are saved in the `results/` directory with timestamps. Each run generates:
- Individual result files for each problem: `{experiment}problems_{timestamp}_{llm}_{index}_result.yaml`
- Combined results file: `{experiment}problems_{timestamp}_{llm}_all_results.yaml`

## Setup

### API Keys

Set appropriate API keys as environment variables based on the LLM you want to use:

**For OpenAI GPT models:**
```bash
export OPENAI_API_KEY=your_openai_api_key
```

**For Google Gemini models:**
```bash
export OPENAI_API_KEY=your_google_api_key  # Note: uses OPENAI_API_KEY variable
```

**For Anthropic Claude models:**
```bash
export OPENAI_API_KEY=your_anthropic_api_key  # Note: uses OPENAI_API_KEY variable
```

**For other models:**
Check the specific requirements in `src/llm_bo_ability_eval/llm_configs.py`

### Running the Script

Navigate to the source directory and run:
```bash
cd src/llm_bo_ability_eval
python main.py [options]
```

## Project Structure

```
src/llm_bo_ability_eval/
├── main.py                    # Main execution script
├── llm_configs.py            # LLM configuration mappings
├── llm_tester.py             # LLM testing functionality
├── llm_tester_system_prompt.py # System prompts for LLMs
├── problem_loader.py         # Problem set loading utilities
└── problem_set/
    ├── 24problems/           # 24-problem test set
    └── 100problems/          # 100-problem test set
```

## Example Output

The system will display progress as it processes each problem:
```
Setting up LLM: gemini
Loading introduction...
Loading 100-problem experiment files...
Found 100 problem files to test
Testing problem file 1/100: problem_001.txt
✓ Completed problem file 1
...
Testing completed! Results saved to: results/123456789/100problems_123456789_gemini_all_results.yaml
Total problem files tested: 100
```
