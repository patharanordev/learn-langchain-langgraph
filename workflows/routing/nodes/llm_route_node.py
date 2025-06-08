from llms.llm_provider import LLMProvider
from workflows.routing.states.state import State
from langchain_core.messages import HumanMessage, SystemMessage

class LlmRouteNode:
    
    def __init__(self, chain_general:LLMProvider, chain_route:LLMProvider):
        self.llm = chain_general.llm
        # Augment the LLM with schema for structured output
        self.router = chain_route.llm

    def llm_call_1(self, state: State):
        """Write a story"""
        print(f'input: {state["input"]}')
        print('select: llm_call_1')
        result = self.llm.invoke(state["input"])
        return {"output": result if isinstance(result, str) else result.content}


    def llm_call_2(self, state: State):
        """Write a joke"""
        print(f'input: {state["input"]}')
        print('select: llm_call_2')
        result = self.llm.invoke(state["input"])
        return {"output": result if isinstance(result, str) else result.content}


    def llm_call_3(self, state: State):
        """Write a poem"""
        print(f'input: {state["input"]}')
        print('select: llm_call_3')
        result = self.llm.invoke(state["input"])
        return {"output": result if isinstance(result, str) else result.content}


    def llm_call_router(self, state: State):
        """Route the input to the appropriate node"""

        print(state)
        input_content = state["messages"][-1]["content"]
        # Run the augmented LLM with structured output to serve as routing logic
        decision = self.router.invoke(
            [
                SystemMessage(
                    content="Route the input to story, joke, or poem based on the user's request."
                ),
                HumanMessage(content=input_content),
            ]
        )

        return {
            "input": input_content,
            "decision": decision.step
        }


    # Conditional edge function to route to the appropriate node
    def route_decision(self, state: State):
        # Return the node name you want to visit next
        if state["decision"] == "story":
            return "llm_call_1"
        elif state["decision"] == "joke":
            return "llm_call_2"
        elif state["decision"] == "poem":
            return "llm_call_3"
