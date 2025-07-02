from workflows.human_in_the_loop.approve_or_reject.models.state import State

class RejectedNode:
    def node(self, state:State):
        print("--------- RejectedNode ---------")
        state["messages"].append("Rejected path taken.")
        return state