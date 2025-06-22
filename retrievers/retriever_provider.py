from abc import ABC

from models.retriever_settings import RetrieverSettings

class RetrieverProvider(ABC):

    def __init__(self):
        super().__init__()
        
        self.client = None
        self.retriever = None
        self.collection = None

    def create(self, retriever_settings:RetrieverSettings):
        pass

    def create_document_index_from_web_urls(self, collection_name:str, urls:list[str]):
        pass