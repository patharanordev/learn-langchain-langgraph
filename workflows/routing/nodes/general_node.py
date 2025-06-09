from llms.llm_provider import LLMProvider
from workflows.routing.models.state import State

class GeneralNode:
    
    def __init__(self, chain:LLMProvider):
        self.llm = chain.llm

    def llm_call_1(self, state: State):
        """Write a story"""
        print(f'input: {state["input"]}')
        print('select: llm_call_1')
        result = self.llm.invoke(state["input"])
        if isinstance(result, str):
            return { "messages": [{ "content": result }] }
        else:
            return {
                "messages": [{
                    "content": result.content
                }]
            }


    def llm_call_2(self, state: State):
        """Write a joke"""
        print(f'input: {state["input"]}')
        print('select: llm_call_2')
        result = self.llm.invoke(state["input"])
        if isinstance(result, str):
            return { "messages": [{ "content": result }] }
        else:
            return {
                "messages": [{
                    "content": result.content
                }]
            }


    def llm_call_3(self, state: State):
        """Write a poem"""
        print(f'input: {state["input"]}')
        print('select: llm_call_3')
        result = self.llm.invoke(state["input"])
        if isinstance(result, str):
            return { "messages": [{ "content": result }] }
        else:
            return {
                "messages": [{
                    "content": result.content
                }]
            }
