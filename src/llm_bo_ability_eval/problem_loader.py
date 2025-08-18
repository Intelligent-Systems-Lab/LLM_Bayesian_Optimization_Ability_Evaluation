import os
import glob
from pathlib import Path
from typing import List, Dict, Any

class ProblemSetLoader:
    def __init__(self, problem_dir: str):
        """Initialize problem set loader."""
        self.problem_dir = Path(problem_dir)
        
    def load_introduction(self) -> str:
        """Load the introduction file."""
        # Look for introduction file in the problem directory and subdirectories
        intro_patterns = ["*introduction.md", "**/bo_hpo_llm_test_5_introduction.md"]
        
        for pattern in intro_patterns:
            intro_files = glob.glob(str(self.problem_dir / pattern), recursive=True)
            if intro_files:
                intro_file = intro_files[0]  # Take the first match
                with open(intro_file, 'r', encoding='utf-8') as f:
                    return f.read()
        
        raise FileNotFoundError(f"No introduction file found in {self.problem_dir}")
        
    def load_problem_files(self, experiment_type: str) -> List[Dict[str, Any]]:
        """Load problem files as strings based on experiment type."""
        if experiment_type == "100":
            pattern = "**/*problem_*.md"
        elif experiment_type == "24":
            pattern = "**/*problem_*.md"
        elif experiment_type == "5":
            # For the 5-problem set, load individual problem files
            pattern = "**/*problem_*.md"
        else:
            raise ValueError(f"Invalid experiment type: {experiment_type}. Use '100', '24', or '5'.")
        
        # Find matching files
        problem_files = sorted(glob.glob(str(self.problem_dir / pattern), recursive=True))
        
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
