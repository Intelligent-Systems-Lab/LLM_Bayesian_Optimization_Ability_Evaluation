import argparse
import yaml
from pathlib import Path

from llm_configs import LLM_MAPPING
from llm_system_prompt import bo_calculation_system_prompt
from llm_tester import LLMTester
from problem_loader import ProblemSetLoader

def main():
    parser = argparse.ArgumentParser(description='Test LLMs on Bayesian Optimization problem set')
    parser.add_argument("--llm", type=str, choices=["gpt", "gemini", "claude", "deepseek", "qwen"], default="qwen3", help="LLM name to test.")
    parser.add_argument('--experiment', choices=['100', '24'], required=True, help='Experiment type: 100-problem or 24-problem')
    parser.add_argument('--problems', default='problem_set/', help='Path to problem set directory')
    parser.add_argument('--output', default='results/', help='Output directory for results')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to test (for debugging)')

    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Initialize LLM tester and problem loader
    llm_config_using = LLM_MAPPING[args.llm]
    llm_tester = LLMTester(llm_config_using, bo_calculation_system_prompt)
    problem_loader = ProblemSetLoader(args.problems)
    
    # Setup LLM
    print(f"Setting up LLM: {args.llm}")
    
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
