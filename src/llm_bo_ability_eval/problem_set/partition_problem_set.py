#!/usr/bin/env python3
"""
Script to partition bo_hpo_llm_test_5.md into introduction and individual problem files.
"""

import re
import yaml
from pathlib import Path

def partition_problem_set(input_file: str, output_dir: str = None, answer_format: str = "steps"):
    """
    Partition the problem set file into introduction and individual problem files.
    
    Args:
        input_file: Path to the input markdown file
        output_dir: Directory to save partitioned files (defaults to same directory as input)
        answer_format: Format of answer section - "steps" or "step-by-step" (default: "steps")
    """
    input_path = Path(input_file)
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Read the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content at the first "---" separator
    parts = content.split('---', 1)
    if len(parts) < 2:
        print("Warning: No '---' separator found. Using entire content as introduction.")
        introduction = content
        problem_section = ""
    else:
        introduction = parts[0].strip()
        problem_section = parts[1].strip()
    
    # Save introduction file
    intro_filename = f"{input_path.stem}_introduction.md"
    intro_path = output_dir / intro_filename
    with open(intro_path, 'w', encoding='utf-8') as f:
        f.write(introduction)
    print(f"Created introduction file: {intro_path}")
    
    # Split problem section by "## Q" pattern
    if problem_section:
        # Find all problem sections
        problem_pattern = r'(## Q\d+\..*?)(?=## Q\d+\.|$)'
        problems = re.findall(problem_pattern, problem_section, re.DOTALL)
        
        # Save each problem to a separate file
        for i, problem in enumerate(problems, 1):
            problem_filename = f"{input_path.stem}_problem_{i:03d}.md"
            problem_path = output_dir / problem_filename
            
            # Clean up the problem content (remove extra whitespace)
            problem_content = problem.strip()
            
            # Remove the answer section (everything from "**Answer (...)**" onwards)
            answer_pattern = rf'\*\*Answer \({re.escape(answer_format)}\):\*\*.*'
            problem_content = re.sub(answer_pattern, '', problem_content, flags=re.DOTALL)
            
            # Clean up any trailing whitespace and separators
            problem_content = problem_content.rstrip().rstrip('-').strip()
            
            with open(problem_path, 'w', encoding='utf-8') as f:
                f.write(problem_content)
            print(f"Created problem file {i}: {problem_path}")
        
        print(f"\nPartitioning complete!")
        print(f"Created 1 introduction file and {len(problems)} problem files.")
    else:
        print("No problem section found.")

def extract_answers(input_file: str, output_file: str = None, answer_format: str = "steps"):
    """
    Extract answers from the problem set file and save them to a YAML file.
    
    Args:
        input_file: Path to the input markdown file
        output_file: Path to save the YAML file with answers (defaults to same name with .yaml extension)
        answer_format: Format of answer section - "steps" or "step-by-step" (default: "steps")
    """
    input_path = Path(input_file)
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_answers.yaml"
    else:
        output_file = Path(output_file)
    
    # Read the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content at the first "---" separator to get problem section
    parts = content.split('---', 1)
    if len(parts) < 2:
        print("Warning: No '---' separator found. No problems to extract answers from.")
        return
    
    problem_section = parts[1].strip()
    
    # Find all problem sections with their answers
    problem_pattern = rf'## (Q\d+)\..*?\*\*Answer \({re.escape(answer_format)}\):\*\*(.*?)(?=## Q\d+\.|$)'
    matches = re.findall(problem_pattern, problem_section, re.DOTALL)
    
    answers = {}
    for problem_id, answer_content in matches:
        # Clean up the answer content
        answer_text = answer_content.strip()
        answers[problem_id] = answer_text
    
    # Save answers to YAML file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(answers, f, default_flow_style=False, allow_unicode=True, indent=2)
    
    print(f"Extracted {len(answers)} answers and saved to: {output_file}")
    return answers

if __name__ == "__main__":
    # Example usage for bo_hpo_llm_test_arch_v3_24.md (uses "steps")
    input_file = "bo_hpo_llm_test_arch_v3_24.md"
    partition_problem_set(input_file, answer_format="steps")
    extract_answers(input_file, answer_format="steps")
    
    # Example usage for bo_hpo_llm_test_100.md (uses "step-by-step")
    # input_file = "bo_hpo_llm_test_100.md"
    # partition_problem_set(input_file, answer_format="step-by-step")
    # extract_answers(input_file, answer_format="step-by-step")
