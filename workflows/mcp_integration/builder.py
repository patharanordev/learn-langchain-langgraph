from langgraph.graph import StateGraph, START, END
from llms.llm import LLM
from models.llm_settings import LLMSettings
from models.settings_request import SettingsRequest
from workflows.mcp_integration.agents.sqlserver_agent import SQLSeverAgent
from workflows.mcp_integration.models.state import State
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import traceback

# load environment variables
load_dotenv()

async def build_graph(request: SettingsRequest):
    try:
        
        llm_settings = LLMSettings(**request.model_dump())
        
        llm = LLM()
        chain = llm.create_chain(llm_settings)
    #     chain.system_prompt = """
    # You are an expert in SQL Server with deep knowledge of query analysis and performance optimization. 
    # You assist in designing and implementing efficient, normalized database schemas that ensure data integrity. 
    # You provide guidance on SQL Server features such as indexing, partitioning, and replication. 
    # You troubleshoot and resolve performance issues, including bottlenecks, deadlocks, and connectivity errors. 
    # You also support database migrations between SQL Server versions or from other database platforms.
    #     """
        
        agent = SQLSeverAgent()
        agent.save_graph_path = request.save_graph_path
        agent_graph = await agent.create_graph(chain)
    
        builder = StateGraph(State)
        builder.add_node('agent_with_mcp', agent_graph)
        
        builder.add_edge(START, 'agent_with_mcp')
        builder.add_edge('agent_with_mcp', END)

        # To support specific thread for get state from graph
        memory = InMemorySaver()
        
        graph = builder.compile(checkpointer=memory)

        return graph
    except Exception as e:
        print(f'In build graph error: {traceback.format_exc()}')
        raise e