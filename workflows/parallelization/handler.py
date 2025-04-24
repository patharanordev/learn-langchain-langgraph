from workflows.parallelization.builder import graph

def start_parallelization():
    # Invoke
    state = graph.invoke({"topic": "cats"})
    print(state["combined_output"])
