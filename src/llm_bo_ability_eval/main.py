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


def main():
    parser = argparse.ArgumentParser(description='Test LLMs on Bayesian Optimization problem set')
    parser.add_argument('--llm', required=True, help='LLM name to test (e.g., o4-mini, gemini-2.5-pro, claude-3-5-sonnet-20241022)')
    parser.add_argument('--experiment', choices=['100', '24'], required=True, help='Experiment type: 100-problem or 24-problem')
    parser.add_argument('--config', default='llm_config_key.yaml', help='Path to LLM configuration file')
    parser.add_argument('--problems', default='problem_set/', help='Path to problem set directory')
    parser.add_argument('--output', default='results/', help='Output directory for results')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to test (for debugging)')
    
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
    
    # Load problem files
    print(f"Loading {args.experiment}-problem experiment files...")
    problem_files = problem_loader.load_problem_files(args.experiment)
    
    if args.max_files:
        problem_files = problem_files[:args.max_files]
    
    print(f"Found {len(problem_files)} problem files to test")
    
    # Test each problem file
    results = []
    for i, problem_file in enumerate(problem_files, 1):
        print(f"Testing problem file {i}/{len(problem_files)}: {problem_file['filename']}")
        
        # Create prompt with the entire file content
        prompt = f"""Please solve all the Bayesian Optimization problems in this problem set step by step:

{problem_file['content']}

Please provide detailed step-by-step solutions for each problem following the same format as shown in the examples."""
        
        # Generate response
        response = llm_tester.generate_response(prompt)
        
        # Store result
        result = {
            'problem_file': problem_file['filename'],
            'experiment_type': args.experiment,
            'file_content': problem_file['content'],
            'llm_response': response,
            'llm_name': args.llm
        }
        results.append(result)
        
        print(f"✓ Completed problem file {i}")
    
    # Save results
    output_file = output_dir / f"{args.llm.replace(':', '_')}_{args.experiment}problems_results.yaml"
    with open(output_file, 'w') as f:
        yaml.dump(results, f, default_flow_style=False, indent=2)
    
    print(f"\nTesting completed! Results saved to: {output_file}")
    print(f"Total problem files tested: {len(results)}")


if __name__ == "__main__":
    main()
