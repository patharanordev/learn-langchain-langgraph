from langgraph.graph import StateGraph, START, END

from llms.ollama import OllamaChain
from workflows.evaluator_optimizer.models.feedback import Feedback
from workflows.evaluator_optimizer.models.state import State

llm = OllamaChain(temperature=0).llm
evaluator = OllamaChain(temperature=0, structured=Feedback).llm

def llm_call_generator(state:State):
    """LLM generates a joke"""

    if state.get('feedback'):
        msg = llm.invoke(
            f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}"
        )
    else:
        msg = llm.invoke(f"Write a joke about {state['topic']}")

    return {"joke":msg.content}

def llm_call_evaluator(state: State):
    """LLM evaluates the joke"""

    print('------------ llm_call_evaluator ------------')
    grade = evaluator.invoke(f"Grade the joke {state['joke']}")
    print(grade)
    return {
        "funny_or_not": grade.grade,
        "feedback": grade.feedback
    }

def route_joke(state: State):
    """Route back to joke generator or end based upon feedback from the evaluator"""

    if state["funny_or_not"] == "funny":
        return "Accepted"
    elif state["funny_or_not"] == "not funny":
        return "Rejected + Feedback"

# Build
optimizer_builder = StateGraph(State)

# Add nodes
optimizer_builder.add_node("llm_call_generator", llm_call_generator)
optimizer_builder.add_node("llm_call_evaluator", llm_call_evaluator)

# Add edges
optimizer_builder.add_edge(START, "llm_call_generator")
optimizer_builder.add_edge("llm_call_generator", "llm_call_evaluator")
optimizer_builder.add_conditional_edges(
    "llm_call_evaluator",
    route_joke,
    {
        "Accepted": END,
        "Rejected + Feedback": "llm_call_evaluator"
    }
)

graph = optimizer_builder.compile()

img_data = graph.get_graph().draw_mermaid_png()
with open('./output/graph-evaluator-optimizer.png', 'wb') as f:
    f.write(img_data)
    print("Graph image saved successfully!")
