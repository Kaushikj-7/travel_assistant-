"""
Conditional routing edges for the travel assistant LangGraph.
"""

from typing import Literal


def route_by_knowledge(state: dict) -> Literal["vectorstore_retrieve", "web_search", "aggregate_response"]:
    """The 'Switch' — dynamically routes based on knowledge availability and guardrails.

    - If input guardrail rejected (e.g. 'khdfgg') → 'aggregate_response' (short-circuit)
    - If ChromaDB has the city (Paris, Tokyo, New York) → 'vectorstore_retrieve'
    - If unknown valid city (e.g. Kyoto, Snohomish, London) → 'web_search'
    """
    if not state.get("is_valid_destination", True):
        return "aggregate_response"

    source = state.get("source", "websearch")
    if source == "vectorstore":
        return "vectorstore_retrieve"
    elif source == "guardrail_rejected":
        return "aggregate_response"
    return "web_search"
