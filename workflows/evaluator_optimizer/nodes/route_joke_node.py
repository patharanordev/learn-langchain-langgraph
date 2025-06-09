
from llms.llm_provider import LLMProvider
from workflows.evaluator_optimizer.models.state import State

class RouteJokeNode:

    def node(self, state: State):
        """Route back to joke generator or end based upon feedback from the evaluator"""

        if state["funny_or_not"] == "funny":
            return "Accepted"
        elif state["funny_or_not"] == "not funny":
            return "Rejected + Feedback"