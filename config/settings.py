from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
  app_name: str = "PoC"
  app_description: str = "Learn LangChain & LangGraph"
  app_version: str = "1.0.0"
  user_agent: str = ""
  port: int = 8000
  token_limit: int = 2048
  langsmith_tracing: bool = True
  langsmith_endpoint: str = "https://api.smith.langchain.com"
  langsmith_api_key: str = ""
  langsmith_project: str = ""
  tavily_api_key: str = ""
  aws_bedrock_region: str = "us-east-1"
  aws_bedrock_access_key: str = ""
  aws_bedrock_secret_key: str = ""
  log_level: str = "DEBUG"
#   mcp_config: dict[str, dict] = {
#     "service_name": {"url": "http://localhost:4200/sse", "transport": "sse"}
#   }

  # retriever
  retriever_provider_name: str = ""

  # chromadb
  chroma_top_k: int = 3
  chroma_host: str = "localhost"
  chroma_port: int = 38000
  chroma_ssl: bool = False
  chroma_collection: str = "poc"
  chroma_persist_directory: str = "/data"
  # chroma_tenant: str
  # chroma_database: str
  chroma_embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
  chroma_device: str = "cpu"

  # huggingface
  hf_token: str = ""
  hf_home: str = "/root/.cache/huggingface"


@lru_cache
def get_settings() -> Settings:
  return Settings()


settings = get_settings()
