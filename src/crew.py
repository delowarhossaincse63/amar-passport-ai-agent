from __future__ import annotations

from src.agents.coordinator import CoordinatorAgent


def run_crew(message: str, session_id: str) -> dict:
    coordinator = CoordinatorAgent()
    crew_response = coordinator.run(message, session_id)
    return crew_response.model_dump()
