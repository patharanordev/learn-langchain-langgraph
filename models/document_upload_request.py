from pydantic import BaseModel, field_validator

class DocumentUploadRequest(BaseModel):
    collection_name:str = "poc"
    urls: list[str] = []
    
    @field_validator("collection_name")
    def validate_collection_name(cls, value):
        if not (isinstance(value, str) and len(str(value).strip()) > 0):
            raise ValueError("collection_name must be a non-empty string")
        return value
    
    @field_validator("urls")
    def validate_model_name(cls, value):
        if len(value) < 1:
            raise ValueError("urls list must not be empty")
        return value
