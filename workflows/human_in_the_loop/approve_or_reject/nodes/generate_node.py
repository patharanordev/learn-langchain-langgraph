from langchain_core.messages import AIMessage
from llms.llm_provider import LLMProvider
from workflows.human_in_the_loop.approve_or_reject.models.state import State

class GenerateNode:
    def node(self, state:State):
        print("--------- GenerateNode ---------")
        state['messages'].append(AIMessage(content="This is the generated output."))
        state['llm_output'] = state['messages'][-1]
        state['llm_output'].pretty_print()
        return state