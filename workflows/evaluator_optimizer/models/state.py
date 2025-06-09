from typing import Any, TypedDict

class State(TypedDict):
    messages: Any
    joke: str
    topic: str
    feedback: str
    funny_or_not: str