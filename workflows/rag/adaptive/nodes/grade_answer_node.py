from workflows.rag.adaptive.models.grade_answer import GradeAnswer
from workflows.rag.adaptive.models.state import State
from llms.llm_provider import LLMProvider
from langchain_core.prompts import ChatPromptTemplate

class GradeAnswerNode:

    system_prompt = """You are a grader assessing whether an answer addresses / resolves a question \n 
Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question.
"""

    def __init__(self, chain:LLMProvider):
        chain.set_prompt(ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
            ]
        ))

        self.llm = chain.settings.prompt | chain.llm

    def node(self, state:State):
        print('\n------------ GradeAnswerNode ------------\n')
        print(state)

        result:GradeAnswer = self.llm.invoke(
           {"question": state["question"], "generation": state["generation"]}
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
    
    def decision_to_address_question(self, state:State):
        grade = state["binary_score"]
        result = ""
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            result = "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            result = "not useful"

        print(f"result: {result}\n")
        return result