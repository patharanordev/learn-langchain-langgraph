from langgraph.constants import Send
from langchain_core.messages import HumanMessage, SystemMessage
from workflows.orchestrator_worker.models.worker_state import WorkerState
from workflows.orchestrator_worker.models.state import State

class Workers:

    def __init__(self, llm:callable, planner:callable):
        self.llm = llm
        self.planner = planner

    # Nodes
    def orchestrator(self, state: State):
        """Orchestrator that generates a plan for the report"""
        
        print('------------- orchestrator -------------')
        
        report_sections = self.planner.invoke(
            [
                SystemMessage(content="Generate a plan for the report."),
                HumanMessage(content=f"Here is the report topic: {state['topic']}"),
            ]
        )

        print(report_sections.sections)

        return {"sections": report_sections.sections}


    def llm_call(self, state: WorkerState):
        """Worker writes a section of the report"""

        print('------------- llm_call -------------')

        # Generate section
        section = self.llm.invoke(
            [
                SystemMessage(
                    content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."
                ),
                HumanMessage(
                    content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
                ),
            ]
        )
        print(section.content)

        # Write the updated section to completed sections
        return {"completed_sections": [section.content]}


    def synthesizer(self, state: State):
        """Synthesize full report from sections"""

        print('------------- synthesizer -------------')

        # List of completed sections
        completed_sections = state["completed_sections"]

        # Format completed section to str to use as context for final sections
        completed_report_sections = "\n\n---\n\n".join(completed_sections)

        print(completed_report_sections)

        return {"final_report": completed_report_sections}


    # Conditional edge function to create llm_call workers that each write a section of the report
    def assign_workers(self, state: State):
        """Assign a worker to each section in the plan"""

        print('------------- assign_workers -------------')

        # Kick off section writing in parallel via Send() API
        return [Send("llm_call", {"section": s}) for s in state["sections"]]