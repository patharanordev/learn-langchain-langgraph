import operator
from typing import Annotated, TypedDict
from workflows.orchestrator_worker.models.section import Section

class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]
