from typing import Any, TypedDict

class State(TypedDict):
    messages: Any
    question: str
    datasource: str
    binary_score: str