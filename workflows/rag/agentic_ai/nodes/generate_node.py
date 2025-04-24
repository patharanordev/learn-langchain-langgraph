
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.chat_models import BaseChatModel
class GenerateNode:

    def __init__(self, model:BaseChatModel):
        self.model = model

    def generate(self, state):
        """
        Generate answer

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """
        print("---GENERATE---")
        messages = state['messages']
        question = messages[0].content
        last_message = messages[-1]

        docs = last_message.content

        prompt = hub.pull('rlm/rag-prompt')

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = prompt | self.model | StrOutputParser()

        response = rag_chain.invoke({'context':docs, 'question': question})
        return {'messages': [response]}