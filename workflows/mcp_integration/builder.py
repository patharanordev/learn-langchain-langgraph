from contextlib import asynccontextmanager
from langgraph.graph import StateGraph, START, END
from workflows.mcp_integration.models.state import State
from workflows.mcp_integration.agents.agent_with_mcp.builder import make_agent_with_mcp

@asynccontextmanager
async def make_graph():
    async with make_agent_with_mcp() as agent:

        builder = StateGraph(State)
        builder.add_node('agent_with_mcp', agent)

        builder.add_edge(START, 'agent_with_mcp')
        builder.add_edge('agent_with_mcp', END)

        graph = builder.compile()
        
        yield graph