from typing import Optional, TypeVar, Type, Union
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import BaseModel
from enum import Enum

from models.chain_response_type import ChainResponseType

T = TypeVar('T', bound=BaseModel)
DEFAULT_OLLAMA_MODEL = 'llama3.2:latest'

class OllamaChain:
    '''
    Ref.
    - https://python.langchain.com/api_reference/ollama/chat_models/langchain_ollama.chat_models.ChatOllama.html#langchain_ollama.chat_models.ChatOllama
    '''
    
    def __init__(self, 
        model:str=DEFAULT_OLLAMA_MODEL,
        temperature:float=0.7,
        chain_response_type:ChainResponseType=ChainResponseType.DEFAULT,
        is_chat_template:bool=True, 
        structured:Union[T, None]=None, 
        tools:list=[],
        prompt:Union[PromptTemplate, None]=None, 
    ):
        self.system_prompt = ''
        self.user_prompt = ''
        self.get_roles()
        self.set_prompt(prompt, is_chat_template)

        self.model = ChatOllama(
            base_url='http://localhost:11434',
            model=model, 
            temperature=temperature
        )
        
        if len(tools) > 0:
            self.model = self.model.bind_tools(tools)
        
        if structured is not None:
            self.llm = self.model.with_structured_output(schema=structured, method='json_schema')
            print(f'set with_structured_output: {structured}')
        else:
            self.llm = self.prompt | self.model
            print('not set with_structured_output')

        if chain_response_type == ChainResponseType.STRING:
            self.llm = self.llm | StrOutputParser()
        elif chain_response_type == ChainResponseType.JSON:
            self.llm = self.llm | JsonOutputParser()
        else:
            # Default based on 
            # https://python.langchain.com/api_reference/core/messages.html
            pass

    def set_prompt(self, prompt:Union[PromptTemplate, None]=None, is_chat_template:bool=False):

        if prompt is not None:
            self.prompt = prompt
        else:
            if is_chat_template:
                self.prompt = ChatPromptTemplate.from_messages(
                    [('system', self.system_prompt), 
                    ("user", self.user_prompt)]
                )
            else:
                self.prompt = PromptTemplate.from_template("""Question: {content}

Answer:
""")

    def get_roles(self):
        # Roles
        # Ref. https://python.langchain.com/docs/concepts/messages/
        
        self.system_prompt = """You are chatbot who specialize in everythings. 
You can recommend and suggest the best solution of user's question. 
No need to refer the old-conversation, just answer the user's question.
"""

        # template effect to result
        self.user_prompt = """Question: {content}
        
Answer:
"""