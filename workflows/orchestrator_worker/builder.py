from langgraph.graph import StateGraph, START, END

from llms.ollama import OllamaChain
from workflows.orchestrator_worker.models.section import Sections
from workflows.orchestrator_worker.models.state import State
from workflows.orchestrator_worker.workers import Workers

# setup llm chain
llm = OllamaChain(temperature=0).llm
# Augment the LLM with schema for structured output
planner = OllamaChain(temperature=0, structured=Sections).llm

workers = Workers(llm=llm, planner=planner)

# Build workflow
orchestrator_worker_builder = StateGraph(State)

# Add the nodes
orchestrator_worker_builder.add_node("orchestrator", workers.orchestrator)
orchestrator_worker_builder.add_node("llm_call", workers.llm_call)
orchestrator_worker_builder.add_node("synthesizer", workers.synthesizer)

# Add edges to connect nodes
orchestrator_worker_builder.add_edge(START, "orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator", workers.assign_workers, ["llm_call"]
)
orchestrator_worker_builder.add_edge("llm_call", "synthesizer")
orchestrator_worker_builder.add_edge("synthesizer", END)

# Compile the workflow
graph = orchestrator_worker_builder.compile()

# Show the workflow
img_data = graph.get_graph().draw_mermaid_png()
with open('./output/graph-orchestrator.png', 'wb') as f:
    f.write(img_data)
    print("Graph image saved successfully!")
