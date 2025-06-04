from typing import TypeVar
from langchain_aws import ChatBedrockConverse
from llms.llm_provider import LLMProvider
from pydantic import BaseModel
import tiktoken
import os

from models.llm_settings import LLMSettings
from dotenv import load_dotenv

load_dotenv()

# DEFAULT_BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"
DEFAULT_TOKENIZER_MODEL = "cl100k_base"
T = TypeVar('T', bound=BaseModel)

class BedrockChain(LLMProvider):

    def __init__(self):
        super().__init__()

    def create(self, settings:LLMSettings):
        self.update_settings(settings)

        self.model = ChatBedrockConverse(
            model=self.settings.model_name,
            temperature=self.settings.temperature,
            region_name=os.environ.get('AWS_BEDROCK_REGION'),
            aws_access_key_id=os.environ.get('AWS_BEDROCK_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_BEDROCK_SECRET_KEY'),
            disable_streaming=not self.settings.streaming,
        )

    def count_tokens(self, text) -> int:
        encoding = tiktoken.get_encoding(DEFAULT_TOKENIZER_MODEL)

        tokens = encoding.encode(text)

        return len(tokens)
