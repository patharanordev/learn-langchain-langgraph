from pydantic import BaseModel, field_validator

class SettingsRequest(BaseModel):
    model_name: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    temperature: float = 0.7
    is_streaming: bool = True
    save_graph_path: str = ""
    use_agent: str = "mcp_integration"
    
    @field_validator("model_name")
    def validate_model_name(cls, value):

        # TODO: Model name should exists in our service

        return value
