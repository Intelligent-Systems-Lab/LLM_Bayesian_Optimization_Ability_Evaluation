import os

OPENAI_REASONING_LLM_CONFIG_REASONING = {
    "model": "o4-mini",
    "base_url": "https://api.openai.com/v1",
    "api_key": os.environ.get('OPENAI_API_KEY', None),
}

GEMINI_LLM_CONFIG = {
    "model": "gemini-2.5-pro",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "api_key": os.environ.get('OPENAI_API_KEY', None),
}

CLAUDE_LLM_CONFIG = {
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.7,
    "max_tokens": 15000,
    "api_key": os.environ.get('OPENAI_API_KEY', None),
}

DEEPSEEKR1_LLM_CONFIG = {
    "model": "deepseek-r1:70b",
    "temperature": 0.7,
    "max_tokens": 15000,
    "base_url": "http://hc4.isl.lab.nycu.edu.tw:11434/v1/",
    "api_key": "dummy_api_key",
}

OLLAMA_HC_QWEN_LLM_CONFIG = {
    "model": "qwen3:32b",
    "temperature": 0.7,
    "max_tokens": 15000,
    "base_url": "http://hc4.isl.lab.nycu.edu.tw:11434/v1/",
    "api_key": "dummy_api_key",
}

LLM_MAPPING = {
    "gpt": OPENAI_REASONING_LLM_CONFIG_REASONING,
    "gemini": GEMINI_LLM_CONFIG,
    "claude": CLAUDE_LLM_CONFIG,
    "deepseek": DEEPSEEKR1_LLM_CONFIG,
    "qwen": OLLAMA_HC_QWEN_LLM_CONFIG,
}
