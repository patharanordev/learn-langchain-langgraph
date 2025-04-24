from workflows.mcp_integration.builder import make_graph
from langchain_core.messages import HumanMessage

async def start_mcp_integration():
    async with make_graph() as graph:
        messages = await graph.ainvoke({
            "messages": [HumanMessage(content="What's the weather in Sacramento?")]
        })
        
        for m in messages['messages']:
            m.pretty_print()