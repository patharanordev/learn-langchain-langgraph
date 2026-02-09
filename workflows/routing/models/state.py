from typing_extensions import TypedDict
from typing import Any

class State(TypedDict):
    messages: Any
    input: str
    decision: str