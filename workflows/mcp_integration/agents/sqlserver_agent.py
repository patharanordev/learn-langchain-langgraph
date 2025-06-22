from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import SystemMessage
from llms.llm_provider import LLMProvider

class SQLSeverAgent:

    system_prompt = """
You are an expert in SQL Server with deep knowledge of query analysis and performance optimization. 
You assist in designing and implementing efficient, normalized database schemas that ensure data integrity. 
You provide guidance on SQL Server features such as indexing, partitioning, and replication. 
You troubleshoot and resolve performance issues, including bottlenecks, deadlocks, and connectivity errors. 
You also support database migrations between SQL Server versions or from other database platforms.
"""

    def __init__(self) -> None:
        self.save_graph_path = ""

    async def create_graph(self, chain:LLMProvider):

        mcp_client = MultiServerMCPClient({
            'sqlserver': {
                'url': 'http://localhost:4200/sse',
                'transport': 'sse'
            }
        })
        
        graph = create_react_agent(
            chain.model,
            tools=mcp_client.get_tools(),
            prompt=SystemMessage(
                content=self.system_prompt
            )
        )

        # Optional: save Mermaid diagram
        if self.save_graph_path is not None and self.save_graph_path != "":
            img_data = graph.get_graph().draw_mermaid_png()
            with open(self.save_graph_path, 'wb') as f:
                f.write(img_data)

        return graph