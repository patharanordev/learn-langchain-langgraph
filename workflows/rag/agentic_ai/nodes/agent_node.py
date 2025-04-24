from typing import Union
from langchain_core.language_models.chat_models import BaseChatModel

class AgentNode:
    def __init__(self, model:BaseChatModel, tools:Union[list, None]=None):
        self.model = model
        self.tools = tools

    def agent(self, state):
        """
        Invokes the agent model to generate a response based on the current state. Given
        the question, it will decide to retrieve using the retriever tool, or simply end.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the agent response appended to messages
        """
        print("---CALL AGENT---")
        messages = state['messages']

        if self.tools is not None:
            self.model = self.model.bind_tools(self.tools)

        response = self.model.invoke(messages)
        return {'messages': [response]}
