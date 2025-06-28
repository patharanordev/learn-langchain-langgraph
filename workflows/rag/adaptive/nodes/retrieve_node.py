from retrievers.retriever_provider import RetrieverProvider
from workflows.rag.adaptive.models.state import State

class RetrieveNode:

    def __init__(self, retriever_provider:RetrieverProvider):
        self.retriever_provider = retriever_provider

    def node(self, state:State):
        """
        Retrieve documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---RETRIEVE---")

        if "question" in state:
            question = state["question"]
        else:
            question = state["messages"][-1]["content"]

        if self.retriever_provider.retriever is None:
            return state

        documents = self.retriever_provider.retriever.invoke(question)
        return {"documents": documents, "question": question}

    