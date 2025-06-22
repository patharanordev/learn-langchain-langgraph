from langgraph.graph import StateGraph, START, END
from llms.llm import LLM
from models.llm_settings import LLMSettings
from models.settings_request import SettingsRequest
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv
import traceback

from workflows.routing.models.state import State
from workflows.routing.models.route import Route
from workflows.routing.nodes.general_node import GeneralNode
from workflows.routing.nodes.route_decision_node import RouteDecisionNode
from workflows.routing.nodes.routing_node import RouterNode

# load environment variables
load_dotenv()

async def build_graph(request: SettingsRequest):
    try:
        
        llm_settings = LLMSettings(**request.model_dump())
        
        llm = LLM()
        chain_general = llm.create_chain(llm_settings)

        llm_settings.structured = Route
        chain_route = llm.create_chain(llm_settings)

        router = RouterNode(chain_route)
        general = GeneralNode(chain_general)
        route_decision = RouteDecisionNode()
        
        builder = StateGraph(State)
        builder.add_node("llm_call_router", router.node)
        builder.add_node('llm_call_1', general.llm_call_1)
        builder.add_node("llm_call_2", general.llm_call_2)
        builder.add_node("llm_call_3", general.llm_call_3)
        
        # Add edges to connect nodes
        builder.add_edge(START, "llm_call_router")
        builder.add_conditional_edges(
            "llm_call_router",
            route_decision.node,
            {  # Name returned by route_decision : Name of next node to visit
                "llm_call_1": "llm_call_1",
                "llm_call_2": "llm_call_2",
                "llm_call_3": "llm_call_3",
            },
        )
        builder.add_edge("llm_call_1", END)
        builder.add_edge("llm_call_2", END)
        builder.add_edge("llm_call_3", END)

        # To support specific thread for get state from graph
        memory = InMemorySaver()
        
        graph = builder.compile(checkpointer=memory)

        # Show the workflow
        img_data = graph.get_graph().draw_mermaid_png()
        with open('./output/graph-routing.png', 'wb') as f:
            f.write(img_data)
            print("Graph image saved successfully!")

        return graph
    except Exception as e:
        print(f'In build graph error: {traceback.format_exc()}')
        raise e

