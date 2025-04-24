from contextlib import asynccontextmanager
from langgraph.prebuilt import create_react_agent
from llms.ollama import OllamaChain
from langchain_mcp_adapters.client import MultiServerMCPClient

model = OllamaChain().model

@asynccontextmanager
async def make_agent_with_mcp():
    async with MultiServerMCPClient(
        {
            'weather': {
                'url': 'http://localhost:7300/sse',
                'transport': 'sse'
            }
        }
    ) as client:
        
        graph = create_react_agent(model, client.get_tools())
        img_data = graph.get_graph().draw_mermaid_png()
        with open('./output/graph-mcp-integration-inside.png', 'wb') as f:
            f.write(img_data)
            print("Graph image saved successfully!")

        yield graph   # pause: let client do work with graph

        # then
        # cleanup something if exit/close