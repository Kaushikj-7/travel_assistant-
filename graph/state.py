"""
Graph state definition for the Multi-Modal Travel Assistant.

Uses TypedDict with Annotated reducers for message appending and
parallel fan-out branch state merging.
"""

import operator
from typing import Annotated, Optional, TypedDict

from langgraph.graph import add_messages


class AgentState(TypedDict):
    """
    Shared state flowing through every node of the LangGraph.

    Fields
    ------
    messages : list
        LangChain message history (HumanMessage, AIMessage, ToolMessage).
        Uses add_messages reducer for append semantics.
    query : str
        The raw user query (e.g. 'Tell me about Kyoto').
    city : str
        Extracted city name.
    is_valid_destination : bool
        Guardrail validation flag (True if destination exists in reality).
    guardrail_error : str | None
        Reason if guardrail rejects input.
    geo_metadata : dict | None
        Verified geographical coordinates and metadata.
    source : str
        Either 'vectorstore' or 'websearch'.
    city_info : str
        Raw factual information retrieved.
    city_summary : str
        Generated travel guide summary.
    weather_forecast : list
        List of daily forecast dicts (merged via operator.add for fan-out).
    image_urls : list
        List of image URLs (merged via operator.add for fan-out).
    media_items : list
        List of structured media items with category and title.
    execution_trace : list
        Step-by-step diagnostic log of node executions, routing decisions,
        and tool calls.
    api_key : str
        Optional runtime OpenAI API key provided by user.
    model_name : str
        Selected LLM model (e.g. 'gpt-4o', 'gpt-4o-mini').
    is_weather_followup : bool | None
        Flag indicating conversation context preservation.
    final_response : dict | None
        The serialized TravelResponse Pydantic object.
    """

    messages: Annotated[list, add_messages]
    query: str
    city: str
    is_valid_destination: Optional[bool]
    guardrail_error: Optional[str]
    geo_metadata: Optional[dict]
    source: str
    city_info: str
    city_summary: str
    weather_forecast: Annotated[list, operator.add]
    image_urls: Annotated[list, operator.add]
    media_items: Optional[list]
    execution_trace: Annotated[list, operator.add]
    api_key: Optional[str]
    model_name: Optional[str]
    is_weather_followup: Optional[bool]
    final_response: Optional[dict]
