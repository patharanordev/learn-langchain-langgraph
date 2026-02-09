from typing import Any, TypedDict
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: list[BaseMessage]
    llm_output: str
    decision: str