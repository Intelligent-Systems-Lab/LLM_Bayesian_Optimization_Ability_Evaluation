import yaml
from pathlib import Path
from typing import List, Dict, Any


def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """Load and return the contents of a YAML file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def save_yaml_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a YAML file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def add_answers_to_experiments(
    experiment_file_path: str,
    answer_file_path: str,
    problem_indexes: List[int]
) -> None:
    """
    Add answers to experiment results based on problem indexes.
    
    Args:
        experiment_file_path: Path to the experiment results YAML file
        answer_file_path: Path to the answers YAML file
        problem_indexes: List of problem numbers to add answers for
    """
    # Load the experiment results and answers
    experiments = load_yaml_file(experiment_file_path)
    answers = load_yaml_file(answer_file_path)
    
    # Create a mapping of problem indexes to experiment entries
    # Assuming experiments is a list and we match by index
    if isinstance(experiments, list):
        for i, problem_index in enumerate(problem_indexes):
            if i < len(experiments):
                answer_key = f"Q{problem_index}"
                if answer_key in answers:
                    experiments[i]['answer'] = answers[answer_key]
                else:
                    print(f"Warning: Answer for {answer_key} not found in answer file")
            else:
                print(f"Warning: Experiment index #{i}: {problem_index} exceeds available experiments")

    # Save the updated experiments back to file
    save_yaml_file(experiments, experiment_file_path)
    print(f"Successfully added answers to {len(problem_indexes)} experiments")


def main():
    """
    Example usage of the add_answers_to_experiments function.
    """
    # Example file paths
    experiment_file = "/home/jack/jacklab/flowerHome/LLM_Bayesian_Optimization_Ability_Evaluation/src/llm_bo_ability_eval/results/qwen_100p_only_do_6.yaml"
    answer_file = "/home/jack/jacklab/flowerHome/LLM_Bayesian_Optimization_Ability_Evaluation/src/llm_bo_ability_eval/problem_set/100problems/bo_hpo_llm_test_100_answers.yaml"
    
    # Example: Add answers for problems 1, 2, 3
    problem_indexes = [1, 2, 3, 13, 14, 15]
    # problem_indexes = [1, 2, 3, 51, 52, 53]
    
    add_answers_to_experiments(experiment_file, answer_file, problem_indexes)


if __name__ == "__main__":
    main()
