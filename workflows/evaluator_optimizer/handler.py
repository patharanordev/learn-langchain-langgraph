from workflows.evaluator_optimizer.builder import graph

def start_evaluator_optimizer():
    state = graph.invoke({'topic': 'Cats'})
    print(state['joke'])