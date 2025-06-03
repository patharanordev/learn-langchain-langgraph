from contextlib import asynccontextmanager
from langgraph.prebuilt import create_react_agent
from llms.bedrock import BedrockChain, DEFAULT_BEDROCK_MODEL
from langchain_mcp_adapters.client import MultiServerMCPClient

@asynccontextmanager
async def make_agent_with_mcp(
    model: str = DEFAULT_BEDROCK_MODEL,
    temperature: float = 0.7,
    streaming: bool = False,
    save_graph_path: str = "",  # Optional dev debug
):
    # Set up the LLM chain
    chain = BedrockChain(model=model, temperature=temperature, streaming=streaming)
    chain.system_prompt = """
You are an expert in SQL Server with deep knowledge of query analysis and performance optimization. 
You assist in designing and implementing efficient, normalized database schemas that ensure data integrity. 
You provide guidance on SQL Server features such as indexing, partitioning, and replication. 
You troubleshoot and resolve performance issues, including bottlenecks, deadlocks, and connectivity errors. 
You also support database migrations between SQL Server versions or from other database platforms.
    """

    # Extract model from chain
    llm_model = chain.model

    # Use MCP client safely
    async with MultiServerMCPClient({
        'sqlserver': {
            'url': 'http://localhost:4200/sse',
            'transport': 'sse'
        }
    }) as mcp_client:

        # Create agent with tools from MCP
        graph = create_react_agent(llm_model, mcp_client.get_tools())

        # Optional: save Mermaid diagram
        if save_graph_path:
            img_data = graph.get_graph().draw_mermaid_png()
            with open(save_graph_path, 'wb') as f:
                f.write(img_data)

        yield graph