from pprint import pprint
from workflows.rag.adaptive.models.state import State
from tools.web_search.tavily import web_search_tool
from langchain.schema import Document

class WebSearchNode:
    def node(self, state:State):
        """
        Web search based on the re-phrased question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with appended web results
        """

        print("---WEB SEARCH---")

        state["question"] = state["messages"][-1]["content"]
        question = state["question"]

        # Web search
        docs = web_search_tool.invoke({"query": question})
        web_results = [Document(page_content=d["content"]) for d in docs]
        state["documents"] = web_results
        state["question"] = question
        pprint(state)

        return state