from functools import lru_cache
from models.retriever_provider_name import RetrieverProviderName
from models.retriever_settings import RetrieverSettings
from retrievers.providers.chroma import ChromaDB
from retrievers.providers.faiss import FAISS
from retrievers.retriever_provider import RetrieverProvider
from config.settings import settings

class Retriever:
    def __init__(self):
        self.retriever_provider = None

    def create(self, retriever_settings:RetrieverSettings) -> RetrieverProvider:
        
        if settings.retriever_provider_name == RetrieverProviderName.FAISS:
            self.retriever_provider = FAISS()
        elif settings.retriever_provider_name == RetrieverProviderName.CHROMA:
            self.retriever_provider = ChromaDB()

        if self.retriever_provider is not None:
            self.retriever_provider.create(retriever_settings)

        return self.retriever_provider
    
    def create_document_index_from_web_urls(self, collection_name:str, urls:list[str]):
        if self.retriever_provider is not None:
            self.retriever_provider.create_document_index_from_web_urls(
                collection_name=collection_name,
                urls=urls
            )

@lru_cache
def connect_retriever() -> RetrieverProvider:
    retriever_settings = RetrieverSettings()
    retriever = Retriever().create(retriever_settings)
    return retriever

retriever = connect_retriever()