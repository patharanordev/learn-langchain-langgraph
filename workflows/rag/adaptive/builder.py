from retrievers.retriever import retriever
from workflows.rag.adaptive.models.grade_answer import GradeAnswer
from workflows.rag.adaptive.models.grade_documents import GradeDocuments
from workflows.rag.adaptive.models.grade_hallucinations import GradeHallucinations
from workflows.rag.adaptive.models.route_query import RouteQuery
from workflows.rag.adaptive.nodes.generate_node import GenerateNode
from workflows.rag.adaptive.nodes.grade_answer_node import GradeAnswerNode
from workflows.rag.adaptive.nodes.grade_documents_node import GradeDocumentsNode
from workflows.rag.adaptive.nodes.grade_hallucinations_node import GradeHallucinationsNode
from workflows.rag.adaptive.nodes.synthesizer_node import SynthesizerNode
from workflows.rag.adaptive.nodes.transform_query import TransformQueryNode
from workflows.rag.adaptive.nodes.retrieve_node import RetrieveNode
from workflows.rag.adaptive.nodes.route_query_node import RouteQueryNode
from langgraph.graph import StateGraph, START, END

from workflows.rag.adaptive.models.state import State

from llms.llm import LLM
from models.llm_settings import LLMSettings
from models.settings_request import SettingsRequest
from langgraph.checkpoint.memory import InMemorySaver
import traceback

from workflows.rag.adaptive.nodes.web_search_node import WebSearchNode

async def build_graph(request: SettingsRequest):
    try:
        llm = LLM()
        llm_settings = LLMSettings(**request.model_dump())

        # generate
        llm_generate_settings = llm_settings.model_copy()
        chain_generate = llm.create_chain(llm_generate_settings)

        # question rewrite
        llm_question_rewrite_settings = llm_settings.model_copy()
        chain_question_rewrite = llm.create_chain(llm_question_rewrite_settings)

        # route query
        llm_route_query_settings = llm_settings.model_copy()
        llm_route_query_settings.structured = RouteQuery
        chain_route_query = llm.create_chain(llm_route_query_settings)

        # grade document
        llm_grade_doc_settings = llm_settings.model_copy()
        llm_grade_doc_settings.structured = GradeDocuments
        chain_grade_doc = llm.create_chain(llm_grade_doc_settings)

        # grade hallucinations
        llm_grade_hallucination_settings = llm_settings.model_copy()
        llm_grade_hallucination_settings.structured = GradeHallucinations
        chain_grade_hallucination = llm.create_chain(llm_grade_hallucination_settings)

        # grade answer
        llm_grade_answer_settings = llm_settings.model_copy()
        llm_grade_answer_settings.structured = GradeAnswer
        chain_grade_answer = llm.create_chain(llm_grade_answer_settings)
        
        web_search = WebSearchNode()
        retrieve = RetrieveNode(retriever)
        route_query = RouteQueryNode(chain_route_query)
        grade_documents = GradeDocumentsNode(chain_grade_doc, retriever)
        generate = GenerateNode(chain_generate)
        grade_hallucination = GradeHallucinationsNode(chain_grade_hallucination)
        grade_answer = GradeAnswerNode(chain_grade_answer)
        transform_query = TransformQueryNode(chain_question_rewrite)
        synthesizer = SynthesizerNode()

        # Build
        builder = StateGraph(State)

        # Add nodes
        builder.add_node("web_search", web_search.node)
        builder.add_node("retrieve", retrieve.node)
        # builder.add_node("route_query", route_query.node)
        builder.add_node("generate", generate.node)
        builder.add_node("grade_documents", grade_documents.node)
        builder.add_node("transform_query", transform_query.node)
        # builder.add_node("grade_hallucination", grade_hallucination.node)
        builder.add_node("grade_answer", grade_answer.node)
        builder.add_node("synthesizer", synthesizer.node)
        
        # Add edges
        builder.add_conditional_edges(
            START,
            route_query.route_question,
            {
                "web_search": "web_search",
                "vectorstore": "retrieve",
            },
        )
        builder.add_edge("web_search", "generate")
        builder.add_edge("retrieve", "grade_documents")
        builder.add_conditional_edges(
            "grade_documents",
            grade_documents.decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        builder.add_edge("transform_query", "retrieve")
        builder.add_conditional_edges(
            "generate",
            grade_hallucination.grade_generation_v_documents_and_question,
            {
                "not supported": "generate",
                "grade_answer": "grade_answer",
            },
        )
        builder.add_conditional_edges(
            "grade_answer",
            grade_answer.decision_to_address_question,
            {
                "useful": "synthesizer",
                "not useful": "transform_query",
            },
        )
        builder.add_edge("synthesizer", END)

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