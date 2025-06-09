from workflows.routing.models.state import State

class RouteDecisionNode:
    
    # Conditional edge function to route to the appropriate node
    def node(self, state: State):
        # Return the node name you want to visit next
        if state["decision"] == "story":
            return "llm_call_1"
        elif state["decision"] == "joke":
            return "llm_call_2"
        elif state["decision"] == "poem":
            return "llm_call_3"
