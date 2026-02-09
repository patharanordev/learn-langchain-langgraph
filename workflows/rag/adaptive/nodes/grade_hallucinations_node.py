from pprint import pprint
from workflows.rag.adaptive.models.grade_hallucinations import GradeHallucinations
from workflows.rag.adaptive.models.state import State
from llms.llm_provider import LLMProvider
from langchain_core.prompts import ChatPromptTemplate

class GradeHallucinationsNode:

    system_prompt = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
"""

    def __init__(self, chain:LLMProvider):
        chain.set_prompt(ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
            ]
        ))

        self.llm = chain.settings.prompt | chain.llm

    def node(self, state:State):
        print('\n------------ GradeHallucinationsNode ------------\n')
        print(state)

        result:GradeHallucinations = self.llm.invoke(
            {"documents": state["docs"][1].page_content, "generation": state["generation"]}
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
    
    def grade_generation_v_documents_and_question(self, state:State):
        """
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """

        print("---CHECK HALLUCINATIONS---")
        documents = state["documents"]
        generation = state["generation"]

        score = self.llm.invoke(
            {"documents": documents, "generation": generation}
        )
        grade = score.binary_score
        result = ""

        # Check hallucination
        if grade == "yes":
            print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
            # Check question-answering
            print("---GRADE GENERATION vs QUESTION---")
            result = "grade_answer"
        else:
            pprint("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
            result = "not supported"

        print(f"result: {result}\n")
        return result