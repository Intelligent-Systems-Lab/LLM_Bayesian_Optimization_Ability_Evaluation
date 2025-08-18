import argparse
import os
import yaml
import glob
import re
from typing import List, Dict, Any
from pathlib import Path

# LLM client imports
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic


class LLMTester:
    def __init__(self, config_path: str):
        """Initialize LLM tester with configuration."""
        with open(config_path, 'r') as f:
            self.llm_configs = yaml.safe_load(f)
        self.current_config = None
        self.client = None
    
    def setup_llm(self, llm_name: str):
        """Setup the specified LLM client."""
        # Find config for the specified LLM
        config = next((c for c in self.llm_configs if c['llm_name'] == llm_name), None)
        if not config:
            raise ValueError(f"LLM '{llm_name}' not found in configuration")
        
        self.current_config = config
        
        # Setup client based on LLM type
        if 'gpt' in llm_name.lower() or 'o4' in llm_name.lower():
            self.client = OpenAI(
                base_url=config['base_url'],
                api_key=config['api_key']
            )
        elif 'gemini' in llm_name.lower():
            genai.configure(api_key=config['api_key'])
            self.client = genai.GenerativeModel(llm_name)
        elif 'claude' in llm_name.lower():
            self.client = Anthropic(api_key=config['api_key'])
        elif 'deepseek' in llm_name.lower() or 'qwen' in llm_name.lower():
            self.client = OpenAI(
                base_url=config['base_url'],
                api_key=config['api_key']
            )
        else:
            raise ValueError(f"Unsupported LLM type: {llm_name}")
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using the current LLM."""
        llm_name = self.current_config['llm_name']
        max_tokens = self.current_config.get('max_tokens', 5000)
        temperature = self.current_config.get('temperature', 0.8)
        
        try:
            if 'gemini' in llm_name.lower():
                response = self.client.generate_content(prompt)
                return response.text
            elif 'claude' in llm_name.lower():
                msg = self.client.messages.create(
                    model=llm_name,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system="You are a helpful assistant specialized in Bayesian Optimization and hyperparameter optimization.",
                    messages=[{"role": "user", "content": prompt}]
                )
                return msg.content[0].text
            else:  # OpenAI-compatible APIs (GPT, DeepSeek, Qwen, etc.)
                completion = self.client.chat.completions.create(
                    model=llm_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant specialized in Bayesian Optimization and hyperparameter optimization."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"


class ProblemSetLoader:
    def __init__(self, problem_dir: str):
        """Initialize problem set loader."""
        self.problem_dir = Path(problem_dir)
        
    def load_all_problems(self) -> List[Dict[str, Any]]:
        """Load all problems from markdown files."""
        problem_files = sorted(glob.glob(str(self.problem_dir / "*.md")))
        all_problems = []
        
        for file_path in problem_files:
            problems = self.parse_markdown_file(file_path)
            all_problems.extend(problems)
            
        return all_problems
    
    def parse_markdown_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a single markdown file and extract problems."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        problems = []
        # Split by question markers (## Q1, ## Q2, etc.)
        question_sections = re.split(r'\n## Q(\d+)\.', content)
        
        if len(question_sections) > 1:
            for i in range(1, len(question_sections), 2):
                if i + 1 < len(question_sections):
                    question_num = question_sections[i]
                    question_content = question_sections[i + 1]
                    
                    # Extract the problem part (before **Answer**)
                    problem_match = re.search(r'^(.*?)\*\*Answer', question_content, re.DOTALL)
                    if problem_match:
                        problem_text = problem_match.group(1).strip()
                        
                        # Extract the answer part
                        answer_match = re.search(r'\*\*Answer[^:]*:\*\*(.*?)(?=\n---|\Z)', question_content, re.DOTALL)
                        answer_text = answer_match.group(1).strip() if answer_match else ""
                        
                        problems.append({
                            'file': os.path.basename(file_path),
                            'question_num': int(question_num),
                            'problem': problem_text,
                            'answer': answer_text
                        })
        
        return problems


def main():
    parser = argparse.ArgumentParser(description='Test LLMs on Bayesian Optimization problem set')
    parser.add_argument('--llm', required=True, help='LLM name to test (e.g., o4-mini, gemini-2.5-pro, claude-3-5-sonnet-20241022)')
    parser.add_argument('--config', default='llm_config_key.yaml', help='Path to LLM configuration file')
    parser.add_argument('--problems', default='problem_set/', help='Path to problem set directory')
    parser.add_argument('--output', default='results/', help='Output directory for results')
    parser.add_argument('--max-problems', type=int, help='Maximum number of problems to test (for debugging)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Initialize LLM tester and problem loader
    llm_tester = LLMTester(args.config)
    problem_loader = ProblemSetLoader(args.problems)
    
    # Setup LLM
    print(f"Setting up LLM: {args.llm}")
    llm_tester.setup_llm(args.llm)
    
    # Load all problems
    print("Loading problem set...")
    all_problems = problem_loader.load_all_problems()
    
    if args.max_problems:
        all_problems = all_problems[:args.max_problems]
    
    print(f"Found {len(all_problems)} problems to test")
    
    # Test each problem
    results = []
    for i, problem in enumerate(all_problems, 1):
        print(f"Testing problem {i}/{len(all_problems)} (Q{problem['question_num']} from {problem['file']})")
        
        # Create prompt
        prompt = f"""Please solve this Bayesian Optimization problem step by step:

{problem['problem']}

Please provide a detailed step-by-step solution following the same format as shown in the examples."""
        
        # Generate response
        response = llm_tester.generate_response(prompt)
        
        # Store result
        result = {
            'problem_id': f"{problem['file']}_Q{problem['question_num']}",
            'file': problem['file'],
            'question_num': problem['question_num'],
            'problem': problem['problem'],
            'expected_answer': problem['answer'],
            'llm_response': response,
            'llm_name': args.llm
        }
        results.append(result)
        
        print(f"✓ Completed problem {i}")
    
    # Save results
    output_file = output_dir / f"{args.llm.replace(':', '_')}_results.yaml"
    with open(output_file, 'w') as f:
        yaml.dump(results, f, default_flow_style=False, indent=2)
    
    print(f"\nTesting completed! Results saved to: {output_file}")
    print(f"Total problems tested: {len(results)}")


if __name__ == "__main__":
    main()
