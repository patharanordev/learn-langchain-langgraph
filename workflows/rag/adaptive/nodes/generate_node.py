from pprint import pprint
from workflows.rag.adaptive.models.state import State
from llms.llm_provider import LLMProvider
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document

class GenerateNode:
    """
    RAG
    """

    human_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

    def __init__(self, chain:LLMProvider):
        chain.set_prompt(ChatPromptTemplate.from_messages(
            [
                ("human", self.human_prompt),
            ]
        ))
        self.llm = chain.settings.prompt | chain.llm

    def node(self, state:State):
        """
        Generate answer

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]

        # RAG generation
        docs_txt = self.format_docs(documents)
        state["generation"] = self.llm.invoke({"context": docs_txt, "question": question})

        pprint(state)
        
        return state

    
    # Post-processing
    def format_docs(self, docs:list[Document]):
        return "\n\n".join(doc.page_content for doc in docs)
