from typing import TypeVar, Union
from langchain_aws import ChatBedrockConverse
from pydantic import BaseModel
import tiktoken
import os

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from models.chain_response_type import ChainResponseType
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"
DEFAULT_TOKENIZER_MODEL = "cl100k_base"
T = TypeVar('T', bound=BaseModel)

class BedrockChain:
  
    def __init__(self, 
        model:str=DEFAULT_BEDROCK_MODEL,
        temperature:float=0.7,
        chain_response_type:ChainResponseType=ChainResponseType.DEFAULT,
        is_chat_template:bool=True, 
        structured:Union[T, None]=None, 
        streaming=False,
        tools:list=[],
        prompt:Union[PromptTemplate, None]=None
    ):
        
        self.system_prompt = ''
        self.user_prompt = ''
        self.get_roles()
        self.set_prompt(prompt, is_chat_template)
        
        self.model_name = model
        self.temperature = temperature

        self.model = ChatBedrockConverse(
            model=self.model_name,
            temperature=self.temperature,
            region_name=os.environ.get('AWS_BEDROCK_REGION'),
            aws_access_key_id=os.environ.get('AWS_BEDROCK_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_BEDROCK_SECRET_KEY'),
            disable_streaming=not streaming,
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

    def count_tokens(self, text) -> int:
        encoding = tiktoken.get_encoding(DEFAULT_TOKENIZER_MODEL)

        tokens = encoding.encode(text)

        return len(tokens)

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