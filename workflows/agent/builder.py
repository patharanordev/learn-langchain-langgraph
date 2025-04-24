from typing import Literal
from llms.ollama import OllamaChain
from workflows.agent.tools.math import add, divide, multiply
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, START, END, MessagesState

tools = [add, divide, multiply]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = OllamaChain(tools=tools).llm

def llm_call(state: MessagesState):
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ]
    }

def tool_node(state:dict):
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(
            ToolMessage(
                content=observation,
                tool_call_id=tool_call["id"],
            )
        )

    return {"messages": result}

def should_continue(state: MessagesState) -> Literal["environment", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "Action"
    
    return END

agent_builder = StateGraph(MessagesState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("environment", tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "Action": "environment",
        END: END
    }
)

agent_builder.add_edge("environment", "llm_call")

graph = agent_builder.compile()
img_data = graph.get_graph(xray=True).draw_mermaid_png()
with open('./output/graph-agent.png', 'wb') as f:
    f.write(img_data)
    print("Graph image saved successfully!")