from contextlib import asynccontextmanager
from langgraph.prebuilt import create_react_agent
from llms.bedrock import BedrockChain
from langchain_mcp_adapters.client import MultiServerMCPClient

chain = BedrockChain()
chain.system_prompt = """
You are an expert in SQL Server with deep knowledge of query analysis and performance optimization. 
You assist in designing and implementing efficient, normalized database schemas that ensure data integrity. 
You provide guidance on SQL Server features such as indexing, partitioning, and replication. 
You troubleshoot and resolve performance issues, including bottlenecks, deadlocks, and connectivity errors. 
You also support database migrations between SQL Server versions or from other database platforms.
"""

model = chain.model

@asynccontextmanager
async def make_agent_with_mcp():
    async with MultiServerMCPClient(
        {
            'sqlserver': {
                'url': 'http://localhost:4200/sse',
                'transport': 'sse'
            },
        }
    ) as client:
        
        graph = create_react_agent(model, client.get_tools())
        img_data = graph.get_graph().draw_mermaid_png()
        with open('./output/graph-mcp-integration-inside.png', 'wb') as f:
            f.write(img_data)
            print("Graph image saved successfully!")

        yield graph   # pause: let client do work with graph
