from langgraph.graph import StateGraph, START, END

from workflows.evaluator_optimizer.models.feedback import Feedback
from workflows.evaluator_optimizer.models.state import State

from llms.llm import LLM
from models.llm_settings import LLMSettings
from models.settings_request import SettingsRequest
from langgraph.checkpoint.memory import InMemorySaver

from workflows.evaluator_optimizer.nodes.evaluator_node import EvaluatorNode
from workflows.evaluator_optimizer.nodes.generator_node import GeneratorNode
from workflows.evaluator_optimizer.nodes.route_joke_node import RouteJokeNode

from dotenv import load_dotenv
import traceback

# load environment variables
load_dotenv()

async def build_graph(request: SettingsRequest):
    try:
        
        llm_settings = LLMSettings()
        llm_settings.model_name = request.model_name
        llm_settings.temperature = request.temperature
        llm_settings.streaming = request.is_streaming
        
        llm = LLM()
        chain_generator = llm.create_chain(llm_settings)

        llm_settings.structured = Feedback
        chain_evaluator = llm.create_chain(llm_settings)

        evaluator = EvaluatorNode(chain_evaluator)
        generator = GeneratorNode(chain_generator)
        route_joke = RouteJokeNode()

        # Build
        builder = StateGraph(State)

        # Add nodes
        builder.add_node("llm_call_generator", generator.node)
        builder.add_node("llm_call_evaluator", evaluator.node)

        # Add edges
        builder.add_edge(START, "llm_call_generator")
        builder.add_edge("llm_call_generator", "llm_call_evaluator")
        builder.add_conditional_edges(
            "llm_call_evaluator",
            route_joke.node,
            {
                "Accepted": END,
                "Rejected + Feedback": "llm_call_evaluator"
            }
        )

        # To support specific thread for get state from graph
        memory = InMemorySaver()
        graph = builder.compile(checkpointer=memory)

        # Show the workflow
        img_data = graph.get_graph().draw_mermaid_png()
        with open('./output/graph-evaluator-optimizer.png', 'wb') as f:
            f.write(img_data)
            print("Graph image saved successfully!")

        return graph
    except Exception as e:
        print(f'In build graph error: {traceback.format_exc()}')
        raise e