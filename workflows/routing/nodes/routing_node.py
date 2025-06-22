from llms.llm_provider import LLMProvider
from workflows.routing.models.state import State
from langchain_core.messages import HumanMessage, SystemMessage

class RouterNode:
    
    def __init__(self, chain:LLMProvider):
        self.llm = chain.llm

    def node(self, state: State):
        """Route the input to the appropriate node"""

        print(state)
        input_content = state["messages"][-1]["content"]
        # Run the augmented LLM with structured output to serve as routing logic
        decision = self.llm.invoke(
            [
                SystemMessage(
                    content="Route the input to story, joke, or poem based on the user's request."
                ),
                HumanMessage(content=input_content),
            ]
        )

        return {
            "input": input_content,
            "decision": decision.step,
            **state
        }
