
from langchain_core.messages import HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel

class RewriteNode:

    def __init__(self, model:BaseChatModel):
        self.model = model

    def rewrite(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """

        print("---TRANSFORM QUERY---")
        messages = state['messages']
        question = messages[0].content

        msg = [
            HumanMessage(
                content=f""" \n 
Look at the input and try to reason about the underlying semantic intent / meaning. \n 
Here is the initial question:
\n ------- \n
{question} 
\n ------- \n
Formulate an improved question: """,
    )
        ]

        response = self.model.invoke(msg)
        return {'messages':[response]}
