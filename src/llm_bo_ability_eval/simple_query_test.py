from simple_query.simple_query import simple_query_by_LLMTester, simple_query
from simple_query.tuning_problems import base_prompt, problem1_3sgd_1adm_admw, problem2, problem3
from simple_query.tuning_agent_system_prompt import TUNING_AGENT_SYSTEM_MESSAGE_JUST_HPO, TUNING_AGENT_SYSTEM_MESSAGE_TPE_CLAUDE

from random_trials.prompts import (
    random_1_system_prompt,
    random_1_user_prompt,
    random_2_system_prompt,
    random_2_user_prompt,
    random_3_system_prompt,
    random_3_user_prompt,
)

"""
Usage:
1.
Edit user_prompt, system_prompt, and llm_to_use in the main block below.

2.
export OPENAI_API_KEY=AIzx... (your_api_key_here)
python simple_query_test.py
"""

if __name__ == "__main__":
    # system_prompt = "You are a helpful AI assistant. Please provide clear and concise responses."
    # system_prompt = TUNING_AGENT_SYSTEM_MESSAGE_JUST_HPO

    # user_prompt = "Hello! Can you introduce yourself?"
    # user_prompt = base_prompt + problem3

    # 1. Initial random trials for each optimizer
    system_prompt = random_2_system_prompt
    user_prompt = random_2_user_prompt
    llm_to_use = "gpt-r"
    
    # You can change the LLM here: gpt, gemini, claude, deepseek, qwen
    # llm_to_use = "gemini"
    # llm_to_use = "gpt-r"
    
    print(f"Using LLM: {llm_to_use}")
    # response = simple_query_by_LLMTester(user_prompt, llm_to_use)
    response = simple_query(user_prompt, system_prompt=system_prompt, llm_name=llm_to_use)

    print("=== LLM Response ===")
    print(response)
    print("====================")
    print(response.choices[0].message.content)
