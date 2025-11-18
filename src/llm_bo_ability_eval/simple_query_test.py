from simple_query.simple_query import simple_query_by_LLMTester, simple_query
from simple_query.tuning_problems import base_prompt, problem1_3sgd_1adm_admw, problem2, problem3
from simple_query.tuning_agent_system_prompt import TUNING_AGENT_SYSTEM_MESSAGE_JUST_HPO, TUNING_AGENT_SYSTEM_MESSAGE_TPE_CLAUDE

if __name__ == "__main__":
    system_prompt = "You are a helpful AI assistant. Please provide clear and concise responses."
    system_prompt = TUNING_AGENT_SYSTEM_MESSAGE_JUST_HPO

    user_prompt = "Hello! Can you introduce yourself?"
    user_prompt = base_prompt + problem3
    
    # You can change the LLM here: gpt, gemini, claude, deepseek, qwen
    llm_to_use = "gemini"
    # llm_to_use = "gpt-r"
    
    print(f"Using LLM: {llm_to_use}")
    # response = simple_query_by_LLMTester(user_prompt, llm_to_use)
    response = simple_query(user_prompt, llm_name=llm_to_use)

    print("=== LLM Response ===")
    print(response)
    print("====================")
    print(response.choices[0].message.content)
