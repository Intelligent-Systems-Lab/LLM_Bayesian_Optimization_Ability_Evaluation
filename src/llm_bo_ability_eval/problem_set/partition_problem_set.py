#!/usr/bin/env python3
"""
Script to partition bo_hpo_llm_test_5.md into introduction and individual problem files.
"""

import os
import re
from pathlib import Path

def partition_problem_set(input_file: str, output_dir: str = None):
    """
    Partition the problem set file into introduction and individual problem files.
    
    Args:
        input_file: Path to the input markdown file
        output_dir: Directory to save partitioned files (defaults to same directory as input)
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
            
            # Remove the answer section (everything from "**Answer (step-by-step):**" onwards)
            answer_pattern = r'\*\*Answer \(steps\):\*\*.*'
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

if __name__ == "__main__":
    # Partition the main problem set file
    input_file = "bo_hpo_llm_test_arch_v3_24.md"
    partition_problem_set(input_file)
