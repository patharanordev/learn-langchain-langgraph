from abc import ABC, abstractmethod
from typing import TypeVar, Union
from models.llm_settings import LLMSettings
from pydantic import BaseModel

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

T = TypeVar('T', bound=BaseModel)

class LLMProvider(ABC):

    def __init__(self):
        super().__init__()
        
        self.settings:LLMSettings = LLMSettings()
        self.system_prompt:str = ''
        self.user_prompt:str = ''
        self.model = None
        self.llm = None

        self.get_roles()

    def update_settings(self, settings:LLMSettings):
        self.settings = settings
        self.set_prompt(self.settings.prompt, self.settings.is_chat_template)
    
    @abstractmethod
    def count_tokens(self, text) -> int:
        pass

    def set_prompt(self, prompt:Union[PromptTemplate, None]=None, is_chat_template:bool=False):

        if prompt is not None:
            self.settings.prompt = prompt
        else:
            if is_chat_template:
                self.settings.prompt = ChatPromptTemplate.from_messages(
                    [('system', self.system_prompt), 
                    ("user", self.user_prompt)]
                )
            else:
                self.settings.prompt = PromptTemplate.from_template("Question: {content}\n\n\nAnswer:\n")

    def get_roles(self):
        # Roles
        # Ref. https://python.langchain.com/docs/concepts/messages/
        
        self.system_prompt = (
            "You are chatbot who specialize in everythings.\n" +
            "You can recommend and suggest the best solution of user's question.\n" +
            "No need to refer the old-conversation, just answer the user's question.\n"
        )

        # template effect to result
        self.user_prompt = "Question: {content}\n\n\nAnswer:\n"