from enum import Enum

class RetrieverProviderName(str, Enum):
    CHROMA = 'chroma'
    FAISS = 'faiss'
