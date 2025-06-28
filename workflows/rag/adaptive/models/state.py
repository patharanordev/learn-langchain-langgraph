from typing import Any, List, TypedDict
from langchain.schema import Document

class State(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[Document]
    
    messages: Any
    docs: Any
    datasource: str
    binary_score: str