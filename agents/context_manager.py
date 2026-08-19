"""
Context Management & Multi-Turn Intent Classifier Engine.

Handles multi-turn conversational context transfer, destination memory retention,
and parameter updates across conversation turns.

Intent Classes:
- NEW_DESTINATION: User is asking for a new city/place.
- WEATHER_UPDATE: User is modifying the date/weather parameter for the active city (Distinction 3: Time Travel).
- TOPIC_INQUIRY: User is asking about food, transit, attractions, history, or logistics for the active city.
- INVALID_INPUT: Input is gibberish, non-text, or non-existent destination.
"""

import re
from typing import Any, Dict, List, Optional

from agents.guardrail_agent import (
    FICTIONAL_LOCATIONS,
    VERIFIED_GLOBAL_REGISTRY,
    GuardrailAgent,
)


class ContextManager:
    """Manages conversational state, context resolution, and entity tracking across turns."""

    WEATHER_TRIGGERS = [
        "next week", "tomorrow", "forecast", "weekend", "temperature",
        "rain", "sunny", "weather", "hot", "cold", "climate", "umbrella",
        "degrees", "humidity", "wind", "snow", "next 5 days", "next 7 days"
    ]

    TOPIC_TRIGGERS = [
        "food", "eat", "restaurant", "restaurants", "cuisine", "dishes", "dining", "breakfast", "lunch", "dinner",
        "transport", "metro", "subway", "bus", "train", "transit", "getting around", "airport", "taxi",
        "landmark", "landmarks", "museum", "museums", "attractions", "places to visit", "sights", "see", "do", "itinerary",
        "hotel", "hotels", "stay", "accommodation", "hostel", "neighborhood", "area",
        "currency", "money", "cost", "expensive", "budget", "price", "cash", "card",
        "history", "culture", "heritage", "language", "safety", "safe", "tips", "pack", "packing"
    ]

    PRONOUNS_REFERENCING_CONTEXT = [
        "there", " it", "it ", "this city", "the city", "that place", "here", "the location", "its"
    ]

    @classmethod
    def resolve_intent_and_entity(
        cls,
        query: str,
        active_city: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Classify intent and resolve target entity with conversational memory.
        
        # NOTE: chat_history is currently unused. Multi-turn context is maintained
        # through LangGraph's MemorySaver checkpointer which persists the full
        # AgentState (including 'city') across conversation turns. The 'active_city'
        # parameter provides the context needed for follow-up resolution.
        """
        clean_query = query.strip()
        query_lower = clean_query.lower()

        # ── 1. Weather Parameter Follow-up (Distinction 3: Time Travel) ──
        has_weather_trigger = any(w in query_lower for w in cls.WEATHER_TRIGGERS)
        explicit_other_city = cls._extract_explicit_new_city(clean_query, active_city)

        if active_city and has_weather_trigger and not explicit_other_city:
            return {
                "intent": "WEATHER_UPDATE",
                "target_city": active_city,
                "is_context_preserved": True,
                "sub_topic": "weather",
                "is_valid": True,
                "reason": f"Preserved active destination '{active_city}' for meteorological forecast update."
            }

        # ── 2. Topic Inquiry on Active Destination ───────────────────
        has_topic_trigger = any(t in query_lower for t in cls.TOPIC_TRIGGERS)
        has_explicit_context_ref = any(p in query_lower for p in cls.PRONOUNS_REFERENCING_CONTEXT)

        if active_city and (has_topic_trigger or has_explicit_context_ref) and not explicit_other_city:
            subtopic = "general"
            for t in cls.TOPIC_TRIGGERS:
                if t in query_lower:
                    subtopic = t
                    break

            return {
                "intent": "TOPIC_INQUIRY",
                "target_city": active_city,
                "is_context_preserved": True,
                "sub_topic": subtopic,
                "is_valid": True,
                "reason": f"Contextual inquiry on '{subtopic}' for active destination '{active_city}'."
            }

        # ── 3. Explicit Destination Search ───────────────────────────
        cand = explicit_other_city or cls._extract_city_name(clean_query)

        if not cand:
            if active_city:
                cand = active_city
            else:
                cand = clean_query

        # Guardrail Validation on Candidate
        is_valid, geo_info, guardrail_reason = GuardrailAgent.verify_location(cand)

        if not is_valid:
            return {
                "intent": "INVALID_INPUT",
                "target_city": cand,
                "is_context_preserved": False,
                "sub_topic": None,
                "is_valid": False,
                "reason": guardrail_reason,
                "geo_metadata": None,
            }

        verified_name = geo_info.get("name", cand.title()) if geo_info else cand.title()
        is_preserved = (verified_name.lower() == active_city.lower()) if active_city else False

        return {
            "intent": "NEW_DESTINATION",
            "target_city": verified_name,
            "is_context_preserved": is_preserved,
            "sub_topic": None,
            "is_valid": True,
            "reason": guardrail_reason,
            "geo_metadata": geo_info,
        }

    @classmethod
    def _extract_explicit_new_city(cls, query: str, active_city: Optional[str]) -> Optional[str]:
        """Detect if the query explicitly mentions a DIFFERENT city from the active city."""
        clean = query.strip()
        for known_city in VERIFIED_GLOBAL_REGISTRY.keys():
            if re.search(rf"\b{re.escape(known_city)}\b", clean, re.IGNORECASE):
                name = VERIFIED_GLOBAL_REGISTRY[known_city]["name"]
                if not active_city or name.lower() != active_city.lower():
                    return name
        return None

    @classmethod
    def _extract_city_name(cls, query: str) -> str:
        """Extract destination candidate using regex & lexical analysis."""
        clean = query.strip().rstrip("?.!")

        # 1. Direct match in verified global registry
        for known_city in VERIFIED_GLOBAL_REGISTRY.keys():
            if re.search(rf"\b{re.escape(known_city)}\b", clean, re.IGNORECASE):
                return VERIFIED_GLOBAL_REGISTRY[known_city]["name"]

        # 2. Check fictional places
        for fictional in FICTIONAL_LOCATIONS.keys():
            if re.search(rf"\b{re.escape(fictional)}\b", clean, re.IGNORECASE):
                return fictional.title()

        # 3. Regex extraction patterns
        patterns = [
            r"(?:tell me about|guide for|guide to|explore|visit|travel to|trip to|information on|how about|what about)\s+([A-Za-z\s]+)",
            r"^(?:in|for|to)\s+([A-Za-z\s]+)",
        ]
        for pat in patterns:
            m = re.search(pat, clean, re.IGNORECASE)
            if m:
                cand = m.group(1).strip()
                # Exclude question filler words
                if not any(w in cand.lower() for w in cls.WEATHER_TRIGGERS + cls.TOPIC_TRIGGERS):
                    return cand

        # If single/double word and not a trigger word
        tokens = clean.split()
        if len(tokens) <= 2 and not any(w in clean.lower() for w in cls.WEATHER_TRIGGERS + cls.TOPIC_TRIGGERS):
            return clean

        return ""
