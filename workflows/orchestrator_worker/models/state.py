# Graph state
import operator
from typing import Annotated, TypedDict
from workflows.orchestrator_worker.models.section import Section


class State(TypedDict):
    topic: str  # Report topic
    sections: list[Section]  # List of report sections
    completed_sections: Annotated[
        list, operator.add
    ]  # All workers write to this key in parallel
    final_report: str  # Final report

