from enum import Enum

class LLMProviderName(str, Enum):
    OLLAMA = 'ollama'
    BEDROCK = 'bedrock'
