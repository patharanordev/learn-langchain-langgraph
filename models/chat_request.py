from pydantic import BaseModel, field_validator

class ChatRequest(BaseModel):
    """
    Represents a request to the OpenAI Chat API.
    """
    message: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    is_streaming: bool = True
    
    @field_validator("message")
    def validate_num_tokens(cls, value):

        # TODO: Implement token limit check
        # token_size = len(value.split())
        # if value > config.token_limit:
        # raise ValueError(
        #     f"Your message too long. We allow {token_limit} tokens, got {token_size}.")

        return value
