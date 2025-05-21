from contextlib import asynccontextmanager
from langgraph.graph import StateGraph, START, END
from workflows.mcp_integration.models.state import State
from workflows.mcp_integration.agents.agent_with_mcp.builder import make_agent_with_mcp
from llms.ollama import OllamaChain, DEFAULT_OLLAMA_MODEL
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

# load environment variables
load_dotenv()

async def create_graph(model:str=DEFAULT_OLLAMA_MODEL, temperature:float=0.7, streaming:bool=False):
    graph, client = await make_agent_with_mcp(model=model, temperature=temperature, streaming=streaming)
    builder = StateGraph(State)
    builder.add_node('agent_with_mcp', graph)

    builder.add_edge(START, 'agent_with_mcp')
    builder.add_edge('agent_with_mcp', END)

    # To support specific thread for get state from graph
    memory = InMemorySaver()
    
    graph = builder.compile(checkpointer=memory)
    # img_data = graph.get_graph().draw_mermaid_png()
    # with open('./output/graph-integrate-with-mcp.png', 'wb') as f:
    #     f.write(img_data)
    #     print("Graph image saved successfully!")

    return graph, client