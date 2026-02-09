from langgraph.graph import StateGraph
from langgraph.constants import END
from langgraph.checkpoint.memory import MemorySaver

import traceback
from models.settings_request import SettingsRequest
from workflows.human_in_the_loop.approve_or_reject.models.state import State
from workflows.human_in_the_loop.approve_or_reject.nodes.approved_node import ApprovedNode
from workflows.human_in_the_loop.approve_or_reject.nodes.generate_node import GenerateNode
from workflows.human_in_the_loop.approve_or_reject.nodes.human_approval_node import HumanApprovalNode
from workflows.human_in_the_loop.approve_or_reject.nodes.rejected_node import RejectedNode

async def build_graph(request: SettingsRequest):
    try:
        generate = GenerateNode()
        human_approval = HumanApprovalNode()
        approved = ApprovedNode()
        rejected = RejectedNode()

        builder = StateGraph(State)
        builder.add_node("generate_llm_output", generate.node)
        builder.add_node("human_approval", human_approval.node)
        builder.add_node("approved_path", approved.node)
        builder.add_node("rejected_path", rejected.node)

        builder.set_entry_point("generate_llm_output")
        builder.add_edge("generate_llm_output", "human_approval")
        builder.add_edge("approved_path", END)
        builder.add_edge("rejected_path", END)

        checkpointer = MemorySaver()
        graph = builder.compile(checkpointer=checkpointer)

        img_data = graph.get_graph().draw_mermaid_png()
        with open('./output/graph-human-approval.png', 'wb') as f:
            f.write(img_data)
            print("Graph image saved successfully!")

        return graph

    except Exception as e:
        print(f'In build graph error: {traceback.format_exc()}')
        raise e