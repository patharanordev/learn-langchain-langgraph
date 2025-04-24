from workflows.chatbot.state import ChatbotState

class ChatbotNode:
    def __init__(self, llm:callable):
        self.llm = llm
    
    def get_node(self, state: ChatbotState) -> ChatbotState:
        result = self.llm.invoke(state["messages"])
        return {"messages": [result]}

