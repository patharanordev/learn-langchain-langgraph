from pydantic import BaseModel
from typing import Any

class State(BaseModel):
    messages: Any