from pprint import pprint
from typing import Literal
from langgraph.types import interrupt, Command
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from workflows.human_in_the_loop.approve_or_reject.models.state import State

class HumanApprovalNode:
    def node(self, state:State, config:RunnableConfig) -> Command[Literal["approved_path", "rejected_path"]]:
        
        print("--------- HumanApprovalNode ---------")
        pprint(state)
        
        human = interrupt({
            "question": "Do you approve the following output?",
            "llm_output": state["llm_output"].content,
            "run_id": config.get('configurable').get('run_id')
        })

        decision = human.get("interrupt_response")
        state["messages"].append(HumanMessage(content=f"Human approval: {decision}"))
        
        if decision == "approve":
            return Command(goto="approved_path", update={"decision":"approved"})
        else:
            return Command(goto="rejected_path", update={"decision":"rejected"})