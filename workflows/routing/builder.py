from pydantic import BaseModel, Field
from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from llms.ollama import OllamaChain


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(
        None, description="The next step in the routing process"
    )

# setup llm chain
llm = OllamaChain().llm

# Augment the LLM with schema for structured output
router = OllamaChain(structured=Route).llm

# State
class State(TypedDict):
    input: str
    decision: str
    output: str


# Nodes
def llm_call_1(state: State):
    """Write a story"""
    print(f'input: {state["input"]}')
    print('select: llm_call_1')
    result = llm.invoke(state["input"])
    return {"output": result if isinstance(result, str) else result.content}


def llm_call_2(state: State):
    """Write a joke"""
    print(f'input: {state["input"]}')
    print('select: llm_call_2')
    result = llm.invoke(state["input"])
    return {"output": result if isinstance(result, str) else result.content}


def llm_call_3(state: State):
    """Write a poem"""
    print(f'input: {state["input"]}')
    print('select: llm_call_3')
    result = llm.invoke(state["input"])
    return {"output": result if isinstance(result, str) else result.content}


def llm_call_router(state: State):
    """Route the input to the appropriate node"""

    # Run the augmented LLM with structured output to serve as routing logic
    decision = router.invoke(
        [
            SystemMessage(
                content="Route the input to story, joke, or poem based on the user's request."
            ),
            HumanMessage(content=state["input"]),
        ]
    )

    return {"decision": decision.step}


# Conditional edge function to route to the appropriate node
def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "story":
        return "llm_call_1"
    elif state["decision"] == "joke":
        return "llm_call_2"
    elif state["decision"] == "poem":
        return "llm_call_3"


# Build workflow
router_builder = StateGraph(State)

# Add nodes
router_builder.add_node("llm_call_1", llm_call_1)
router_builder.add_node("llm_call_2", llm_call_2)
router_builder.add_node("llm_call_3", llm_call_3)
router_builder.add_node("llm_call_router", llm_call_router)

# Add edges to connect nodes
router_builder.add_edge(START, "llm_call_router")
router_builder.add_conditional_edges(
    "llm_call_router",
    route_decision,
    {  # Name returned by route_decision : Name of next node to visit
        "llm_call_1": "llm_call_1",
        "llm_call_2": "llm_call_2",
        "llm_call_3": "llm_call_3",
    },
)
router_builder.add_edge("llm_call_1", END)
router_builder.add_edge("llm_call_2", END)
router_builder.add_edge("llm_call_3", END)

# Compile workflow
graph = router_builder.compile()

# Show the workflow
img_data = graph.get_graph().draw_mermaid_png()
with open('./output/graph-routing.png', 'wb') as f:
    f.write(img_data)
    print("Graph image saved successfully!")