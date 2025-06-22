from retrievers.retriever_provider import RetrieverProvider
from workflows.rag.adaptive.models.grade_documents import GradeDocuments
from workflows.rag.adaptive.models.state import State
from llms.llm_provider import LLMProvider
from langchain_core.prompts import ChatPromptTemplate

class GradeDocumentsNode:

    system_prompt = """You are a grader assessing relevance of a retrieved document to a user question. \n 
If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

    def __init__(self, chain:LLMProvider, retriever_provider:RetrieverProvider):
        chain.set_prompt(ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
            ]
        ))

        self.llm = chain.settings.prompt | chain.llm
        self.retriever_provider = retriever_provider

    def node(self, state:State):
        print('\n------------ GradeDocumentsNode ------------\n')
        print(state)

        if self.retriever_provider.retriever is None:
            return state

        docs = self.retriever_provider.retriever.invoke(state["question"])
        doc_txt = docs[1].page_content

        print('\nDocument:\n')
        print(doc_txt)

        result:GradeDocuments = self.llm.invoke(
            {"question": state["question"], "document": doc_txt}
        )

        print('\nResult:\n')
        print(result)

        state["messages"].append({
            "content": result.binary_score
        })
        
        return {
            "binary_score": result.binary_score,
            **state
        }
    