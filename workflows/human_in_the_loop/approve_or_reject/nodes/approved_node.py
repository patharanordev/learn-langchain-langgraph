from workflows.human_in_the_loop.approve_or_reject.models.state import State

class ApprovedNode:
    def node(self, state:State):
        print("--------- ApprovedNode ---------")
        state["messages"].append("Approved path taken.")
        return state