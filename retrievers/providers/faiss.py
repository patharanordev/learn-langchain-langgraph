from models.retriever_settings import RetrieverSettings
from retrievers.retriever_provider import RetrieverProvider

class FAISS(RetrieverProvider):

    def __init__(self):
        super().__init__()
    
    def create(self, settings:RetrieverSettings):
        pass