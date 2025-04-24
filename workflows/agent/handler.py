from workflows.agent.builder import graph
from langchain_core.messages import HumanMessage

def start_agent():
    messages = [HumanMessage(content="Add 3 and 4.")]
    messages = graph.invoke({"messages":messages})
    for m in messages["messages"]:
        m.pretty_print()