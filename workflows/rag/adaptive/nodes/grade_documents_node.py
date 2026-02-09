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
        """
        Determines whether the retrieved documents are relevant to the question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with only filtered relevant documents
        """

        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        # Score each doc
        filtered_docs = []
        for d in documents:
            score:GradeDocuments = self.llm.invoke(
                {"question": state["question"], "document": d.page_content}
            )

            grade = score.binary_score
            if grade == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                
        return {"documents": filtered_docs, "question": question}
    
    
    def decide_to_generate(self, state:State):
        """
        Determines whether to generate an answer, or re-generate a question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """

        print("---ASSESS GRADED DOCUMENTS---")
        filtered_documents = state["documents"]

        if not filtered_documents:
            # All documents have been filtered check_relevance
            # We will re-generate a new query
            print(
                "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
            )
            return "transform_query"
        else:
            # We have relevant documents, so generate answer
            print("---DECISION: GENERATE---")
            return "generate"
