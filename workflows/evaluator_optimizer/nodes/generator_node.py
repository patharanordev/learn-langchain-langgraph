
from llms.llm_provider import LLMProvider
from workflows.evaluator_optimizer.models.state import State

class GeneratorNode:

    def __init__(self, chain:LLMProvider):
        self.llm = chain.llm

    def node(self, state:State):
        """LLM generates a joke"""

        print(state)

        input_content = state["messages"][-1]["content"]
        state['topic'] = input_content

        if state.get('feedback'):
            msg = self.llm.invoke(
                f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}"
            )
        else:
            msg = self.llm.invoke(f"Write a joke about {state['topic']}")

        return {
            "joke":msg.content,
            "messages": [{
                "content": msg.content
            }]
        }