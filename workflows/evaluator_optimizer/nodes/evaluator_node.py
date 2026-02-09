
from llms.llm_provider import LLMProvider
from workflows.evaluator_optimizer.models.state import State

class EvaluatorNode:

    def __init__(self, chain:LLMProvider):
        self.llm = chain.llm

    def node(self, state:State):
        """LLM evaluates the joke"""

        print('------------ llm_call_evaluator ------------')
        grade = self.llm.invoke(f"Grade the joke {state['joke']}")
        print(grade)
        return {
            "funny_or_not": grade.grade,
            "feedback": grade.feedback
        }