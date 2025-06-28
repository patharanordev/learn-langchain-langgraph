from workflows.rag.adaptive.models.state import State
from llms.llm_provider import LLMProvider
from langchain_core.prompts import ChatPromptTemplate

class TransformQueryNode:

    system_prompt = """You a question re-writer that converts an input question to a better version that is optimized \n 
for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning.
"""

    def __init__(self, chain:LLMProvider):
        chain.set_prompt(ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                (
                    "human",
                    "Here is the initial question: \n\n {question} \n Formulate an improved question.",
                ),
            ]
        ))
        self.llm = chain.settings.prompt | chain.llm

    def node(self, state:State):
        """
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """

        print("---TRANSFORM QUERY---")
        question = state["question"]
        documents = state["documents"]

        # Re-write question
        better_question = self.llm.invoke({"question": question})
        return {"documents": documents, "question": better_question}