from contextlib import asynccontextmanager
from langgraph.prebuilt import create_react_agent
from llms.bedrock import BedrockChain, DEFAULT_BEDROCK_MODEL
from langchain_mcp_adapters.client import MultiServerMCPClient

class SQLSeverAgent:

    def __init__(self) -> None:
        self.model_name = DEFAULT_BEDROCK_MODEL
        self.temperature = 0.7
        self.streaming = False
        self.save_graph_path = ""

        # by default
        self.system_prompt = """
    You are an expert in SQL Server with deep knowledge of query analysis and performance optimization. 
    You assist in designing and implementing efficient, normalized database schemas that ensure data integrity. 
    You provide guidance on SQL Server features such as indexing, partitioning, and replication. 
    You troubleshoot and resolve performance issues, including bottlenecks, deadlocks, and connectivity errors. 
    You also support database migrations between SQL Server versions or from other database platforms.
        """

        self.chain = None

    def set_chain(self, model_name, temperature, streaming):
        if model_name is not None:
            self.model_name = model_name
        if temperature is not None:
            self.temperature = temperature
        if streaming is not None:
            self.streaming = streaming

        print({
            "model_name": self.model_name,
            "temperature": self.temperature,
            "streaming": self.streaming
        })

        # Set up the LLM chain
        self.chain = BedrockChain(
            model=self.model_name, 
            temperature=self.temperature, 
            streaming=self.streaming
        )

        self.chain.system_prompt = self.system_prompt
        
    async def create_graph(self):

        mcp_client = MultiServerMCPClient({
            'sqlserver': {
                'url': 'http://localhost:4200/sse',
                'transport': 'sse'
            }
        })
        
        graph = create_react_agent(self.chain.model, mcp_client.get_tools())

        # Optional: save Mermaid diagram
        if self.save_graph_path is not None and self.save_graph_path != "":
            img_data = graph.get_graph().draw_mermaid_png()
            with open(self.save_graph_path, 'wb') as f:
                f.write(img_data)

        return graph