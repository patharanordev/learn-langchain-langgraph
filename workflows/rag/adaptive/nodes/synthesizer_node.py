from workflows.rag.adaptive.models.state import State

class SynthesizerNode:
    def node(self, state:State):
        print('\n------------ SynthesizerNode ------------\n')
        print(state)

        state['messages'].append(state["generation"])
        
        return state