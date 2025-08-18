import os
import glob
from pathlib import Path
from typing import List

class ProblemSetLoader:
    def __init__(self, problem_dir: str):
        """Initialize problem set loader."""
        self.problem_dir = Path(problem_dir)
        
    def load_problem_files(self, experiment_type: str) -> List[str]:
        """Load problem files as strings based on experiment type."""
        if experiment_type == "100":
            pattern = "*100*part*.md"
        elif experiment_type == "24":
            pattern = "*24*part*.md"
        else:
            raise ValueError(f"Invalid experiment type: {experiment_type}. Use '100' or '24'.")
        
        # Find matching files
        problem_files = sorted(glob.glob(str(self.problem_dir / pattern)))
        
        if not problem_files:
            raise FileNotFoundError(f"No problem files found matching pattern: {pattern}")
        
        # Load file contents as strings
        problem_contents = []
        for file_path in problem_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                problem_contents.append({
                    'filename': os.path.basename(file_path),
                    'content': content
                })
        
        return problem_contents
