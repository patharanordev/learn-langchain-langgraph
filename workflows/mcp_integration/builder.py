from contextlib import asynccontextmanager
from langgraph.graph import StateGraph, START, END
from models.settings_request import SettingsRequest
from workflows.mcp_integration.agents.sqlserver_agent import SQLSeverAgent
from workflows.mcp_integration.models.state import State
from workflows.mcp_integration.agents.agent_with_mcp.builder import make_agent_with_mcp
from llms.ollama import OllamaChain, DEFAULT_OLLAMA_MODEL
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

# load environment variables
load_dotenv()

async def build_graph(request: SettingsRequest):
    try:
        agent = SQLSeverAgent()
        agent.save_graph_path = request.save_graph_path
        agent.set_chain(request.model_name, request.temperature, request.is_streaming)
        agent_graph = await agent.create_graph()
    
        builder = StateGraph(State)
        builder.add_node('agent_with_mcp', agent_graph)
        
        builder.add_edge(START, 'agent_with_mcp')
        builder.add_edge('agent_with_mcp', END)

        # To support specific thread for get state from graph
        memory = InMemorySaver()
        
        graph = builder.compile(checkpointer=memory)

        return graph
    except Exception as e:
        print(f'In build graph error: {str(e)}')
        raise e