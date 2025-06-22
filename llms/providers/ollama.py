from typing import TypeVar
from langchain_ollama import ChatOllama
from llms.llm_provider import LLMProvider
from models.llm_settings import LLMSettings
from pydantic import BaseModel
from transformers import AutoTokenizer

T = TypeVar('T', bound=BaseModel)
DEFAULT_OLLAMA_MODEL = 'llama3.2:latest'

class OllamaChain(LLMProvider):
    '''
    Ref.
    - https://python.langchain.com/api_reference/ollama/chat_models/langchain_ollama.chat_models.ChatOllama.html#langchain_ollama.chat_models.ChatOllama
    '''

    def __init__(self):
        super().__init__()
    
    def create(self, settings:LLMSettings):
        self.update_settings(settings)

        self.model = ChatOllama(
            base_url=settings.base_url,
            model=settings.model_name, 
            temperature=settings.temperature,
            streaming=settings.streaming,
        )
        

    def count_tokens(self, text) -> int:
        tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B")
    
        tokens = tokenizer.encode(text)
        
        return len(tokens)
