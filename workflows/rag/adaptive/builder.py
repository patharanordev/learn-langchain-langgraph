from retrievers.retriever import retriever
from workflows.rag.adaptive.models.grade_documents import GradeDocuments
from workflows.rag.adaptive.models.route_query import RouteQuery
from workflows.rag.adaptive.nodes.grade_documents_node import GradeDocumentsNode
from workflows.rag.adaptive.nodes.route_query_node import RouteQueryNode
from langgraph.graph import StateGraph, START, END

from workflows.evaluator_optimizer.models.state import State

from llms.llm import LLM
from models.llm_settings import LLMSettings
from models.settings_request import SettingsRequest
from langgraph.checkpoint.memory import InMemorySaver
import traceback

async def build_graph(request: SettingsRequest):
    try:
        llm = LLM()
        llm_settings = LLMSettings(**request.model_dump())

        # route query
        llm_settings.structured = RouteQuery
        chain_route_query = llm.create_chain(llm_settings)

        # grade document
        llm_grade_doc_settings = llm_settings.model_copy()
        llm_grade_doc_settings.structured = GradeDocuments
        chain_grade_doc = llm.create_chain(llm_grade_doc_settings)

        route_query = RouteQueryNode(chain_route_query)
        grade_doc = GradeDocumentsNode(chain_grade_doc, retriever)

        # Build
        builder = StateGraph(State)

        # Add nodes
        builder.add_node("route_query", route_query.node)
        builder.add_node("grade_doc", grade_doc.node)
        
        # Add edges
        builder.add_edge(START, "route_query")
        builder.add_edge("route_query", "grade_doc")
        builder.add_edge("grade_doc", END)

        # To support specific thread for get state from graph
        memory = InMemorySaver()
        graph = builder.compile(checkpointer=memory)

        # Show the workflow
        img_data = graph.get_graph().draw_mermaid_png()
        with open('./output/graph-adaptive-rag.png', 'wb') as f:
            f.write(img_data)
            print("Graph image saved successfully!")

        return graph
    except Exception as e:
        print(f'In build graph error: {traceback.format_exc()}')
        raise e