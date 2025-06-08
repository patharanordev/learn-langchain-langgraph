from pydantic import BaseModel, Field
from typing_extensions import Literal

class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(
        None, description="The next step in the routing process"
    )
