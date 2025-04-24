from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from llms.ollama import OllamaChain
from workflows.rag.agentic_ai.edges.document import grade_documents
from workflows.rag.agentic_ai.states.agent_state import AgentState
from workflows.rag.agentic_ai.nodes.agent_node import AgentNode
from workflows.rag.agentic_ai.nodes.rewrite_node import RewriteNode
from workflows.rag.agentic_ai.nodes.generate_node import GenerateNode
from workflows.rag.agentic_ai.retriever.ollama_chroma import tools, retriever_tool
from langgraph.prebuilt import tools_condition

model = OllamaChain(temperature=0).model
agent_node = AgentNode(model, tools=tools)
rewrite_node = RewriteNode(model)
generate_node = GenerateNode(model)

workflow = StateGraph(AgentState)

# add node
retriever = ToolNode(tools)
workflow.add_node('agent', agent_node.agent)
workflow.add_node('retriever', retriever)
workflow.add_node('rewrite', rewrite_node.rewrite)
workflow.add_node('generate', generate_node.generate)

# add edge
workflow.add_edge(START, 'agent')
workflow.add_condition_edges(
    'agent',
    tools_condition,
    {
        'tools': 'retriever',
        END: END
    }
)
workflow.add_condition_edges(
    'retriever',
    grade_documents
)

workflow.add_edge('generate', END)
workflow.add_edge('rewrite', 'agent')

graph = workflow.compile()
img_data = graph.get_graph(xray=True).draw_mermaid_png()
with open('./output/graph-rag-agentic-ai.png', 'wb') as f:
    f.write(img_data)
    print("Graph image saved successfully!")
