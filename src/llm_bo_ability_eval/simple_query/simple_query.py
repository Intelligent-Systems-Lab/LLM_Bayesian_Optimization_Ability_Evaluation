from llm_configs import LLM_MAPPING
from llm_tester import LLMTester
from openai import OpenAI, NOT_GIVEN

def simple_query_by_LLMTester(prompt: str, system_prompt: str = None, llm_name: str = "gemini"):
    """
    Simple query function using the existing LLMTester infrastructure.
    
    Args:
        prompt: The user prompt to send to the LLM
        llm_name: Which LLM to use (options: gpt, gemini, claude, deepseek, qwen)
    
    Returns:
        str: The LLM's response
    """
    # Get the LLM configuration
    llm_config = LLM_MAPPING[llm_name]
    
    # Simple system prompt for general queries
    if system_prompt is None:
        system_prompt = "You are a helpful AI assistant. Please provide clear and concise responses."
    
    # Initialize the LLM tester
    llm_tester = LLMTester(llm_config, system_prompt)
    
    # Generate and return response
    response = llm_tester.generate_response(prompt)
    return response

def simple_query(prompt: str, system_prompt: str = None, llm_name: str = "gemini"):  # --- IGNORE ---
    """
    Simple query function to test openai sdk.
    
    Args:
        prompt: The user prompt to send to the LLM
        system_prompt: The system prompt to set the behavior of the LLM
        llm_name: Which LLM to use (options: gpt, gemini, claude, deepseek, qwen)
    
    Returns:
        str: The LLM's response
    """
    # Get the LLM configuration
    llm_config = LLM_MAPPING[llm_name]
    print("LLM Config: {}".format({k:v for k,v in llm_config.items() if k != 'api_key'}))
    
    # Simple system prompt for general queries
    if system_prompt is None:
        system_prompt = "You are a helpful AI assistant. Please provide clear and concise responses."
    
    # Use OpenAI SDK directly for testing
    client = OpenAI(
        base_url=llm_config['base_url'],
        api_key=llm_config['api_key']
    )
    response = client.chat.completions.create(
        model=llm_config['model'],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        # max_tokens=llm_config.get('max_tokens', 5000),
        temperature=llm_config.get('temperature', 0.4),
        seed=llm_config.get('cache_seed', NOT_GIVEN),
    )
    return response
