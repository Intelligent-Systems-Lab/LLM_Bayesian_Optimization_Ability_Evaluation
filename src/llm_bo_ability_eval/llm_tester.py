from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic

class LLMTester:
    def __init__(self, llm_config: dict, system_prompt: str):
        """Initialize LLM tester with configuration."""
        self.current_config = None
        self.system_prompt = system_prompt
        self.client = None
        self._setup_llm(llm_config, system_prompt)

    def _setup_llm(self, llm_config: dict, system_prompt: str):
        """Setup the specified LLM client."""
        # Find config for the specified LLM
        llm_name = llm_config['model']
        self.current_config = llm_config
        
        # Setup client based on LLM type
        if 'gpt' in llm_name.lower() or 'o4' in llm_name.lower():
            self.client = OpenAI(
                base_url=llm_config['base_url'],
                api_key=llm_config['api_key']
            )
        elif 'gemini' in llm_name.lower():
            genai.configure(api_key=llm_config['api_key'])
            self.client = genai.GenerativeModel(llm_name, system_instruction=system_prompt)
        elif 'claude' in llm_name.lower():
            self.client = Anthropic(api_key=llm_config['api_key'])
        elif 'deepseek' in llm_name.lower() or 'qwen' in llm_name.lower():
            self.client = OpenAI(
                base_url=llm_config['base_url'],
                api_key=llm_config['api_key']
            )
        else:
            raise ValueError(f"Unsupported LLM type: {llm_name}")
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using the current LLM."""
        llm_name = self.current_config['model']
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
                    system=self.system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                return msg.content[0].text
            else:  # OpenAI-compatible APIs (GPT, DeepSeek, Qwen, etc.)
                completion = self.client.chat.completions.create(
                    model=llm_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
