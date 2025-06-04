from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

class SQLSeverAgent:

    def __init__(self) -> None:
        self.save_graph_path = ""

    async def create_graph(self, llm_model):

        mcp_client = MultiServerMCPClient({
            'sqlserver': {
                'url': 'http://localhost:4200/sse',
                'transport': 'sse'
            }
        })
        
        graph = create_react_agent(llm_model, mcp_client.get_tools())

        # Optional: save Mermaid diagram
        if self.save_graph_path is not None and self.save_graph_path != "":
            img_data = graph.get_graph().draw_mermaid_png()
            with open(self.save_graph_path, 'wb') as f:
                f.write(img_data)

        return graph