from typing import TypeVar
from config.settings import settings
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class RetrieverSettings(BaseModel):
    embedding_model_name:str = settings.chroma_embeddings_model
    collection_name:str = settings.chroma_collection
    persist_directory:str = settings.chroma_persist_directory
    chroma_device:str = settings.chroma_device