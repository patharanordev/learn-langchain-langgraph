from typing import TypeVar, Union
from models.chain_response_type import ChainResponseType
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class LLMSettings(BaseModel):
    model_name:str=''
    temperature:float=0.7
    chain_response_type:ChainResponseType=ChainResponseType.DEFAULT
    is_chat_template:bool=True
    structured:Union[T, None]=None 
    streaming:bool=False
    tools:list=[]
    prompt:Union[PromptTemplate, None]=None