"""
Planning Agent — Agentsway Methodology (2510.23664v1) & Context Transfer Architecture.

Role:
- Classifies user intent across conversation turns using LLM (when available) or regex fallback
- Manages seamless context transfer & entity retention (Human-in-the-Loop & Time Travel: Distinction 3)
- Enforces Input Guardrail & real-world location verification
- Formulates multi-modal execution plans
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage

from agents.context_manager import ContextManager

logger = logging.getLogger("travel_agent")

# System prompt for LLM-based intent classification
PLANNING_SYSTEM_PROMPT = """You are the Planning Agent in a multi-agent travel assistant system.
Your job is to classify the user's intent and extract the target city.

Given the user's query and the currently active city (if any), determine:
1. intent: One of "NEW_DESTINATION", "WEATHER_UPDATE", "TOPIC_INQUIRY", or "INVALID_INPUT"
2. target_city: The city the user is asking about
3. is_context_preserved: True if the user is asking a follow-up about the same active city

Rules:
- If the user mentions a new city name, intent = "NEW_DESTINATION"
- If the user asks about weather/forecast/temperature for the active city, intent = "WEATHER_UPDATE"
- If the user asks about food/transit/landmarks for the active city, intent = "TOPIC_INQUIRY"
- If the input is gibberish or not a real place, intent = "INVALID_INPUT"
- If there's an active city and no new city is mentioned, preserve the active city

Respond in this exact JSON format:
{"intent": "...", "target_city": "...", "is_context_preserved": true/false, "sub_topic": "..." or null}"""


class PlanningAgent:
    """Agent responsible for query interpretation, entity extraction, context memory, and strategy planning.

    Uses LLM for intent classification when available, with deterministic
    regex/keyword fallback via ContextManager when no LLM is provided.
    """

    def __init__(self, llm=None):
        self.llm = llm

    def _classify_with_llm(self, query: str, active_city: str) -> Optional[Dict[str, Any]]:
        """Attempt LLM-based intent classification. Returns None on failure."""
        if not self.llm:
            return None
        try:
            response = self.llm.invoke([
                SystemMessage(content=PLANNING_SYSTEM_PROMPT),
                HumanMessage(content=f"Active city: {active_city or 'None'}\nUser query: {query}")
            ])
            # Parse the LLM's JSON response
            import json
            content = response.content.strip()
            # Handle markdown code blocks
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            result = json.loads(content)
            logger.info(f"LLM intent classification: {result.get('intent')} -> {result.get('target_city')}")
            return result
        except Exception as e:
            logger.warning(f"LLM intent classification failed, falling back to regex: {e}")
            return None

    def execute_plan(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state.get("query", "").strip()
        messages = state.get("messages", [])
        current_city = state.get("city", "")

        # ── Attempt LLM-based classification, fallback to regex ──────
        llm_result = self._classify_with_llm(query, current_city)
        classification_method = "llm" if llm_result else "regex"

        # ── Context Resolution & Multi-Turn Intent Classification ────
        # Always run ContextManager for guardrail verification (geocoding check)
        resolution = ContextManager.resolve_intent_and_entity(
            query=query,
            active_city=current_city,
            chat_history=messages
        )

        from agents.guardrail_agent import GuardrailAgent

        # If LLM classification succeeded, use its intent/city and verify with GuardrailAgent
        if llm_result:
            intent = llm_result.get("intent", resolution["intent"])
            llm_city = (llm_result.get("target_city") or "").strip()
            is_context_preserved = llm_result.get("is_context_preserved", resolution["is_context_preserved"])
            sub_topic = llm_result.get("sub_topic", resolution["sub_topic"])

            if llm_city and not is_context_preserved:
                # Direct geocoding verification on LLM-extracted candidate
                is_valid, geo_info, reason = GuardrailAgent.verify_location(llm_city)
                target_city = geo_info.get("name", llm_city.title()) if geo_info else llm_city.title()
            else:
                is_valid = resolution["is_valid"]
                reason = resolution["reason"]
                geo_info = resolution.get("geo_metadata")
                target_city = resolution["target_city"]
        else:
            intent = resolution["intent"]
            target_city = resolution["target_city"]
            is_context_preserved = resolution["is_context_preserved"]
            sub_topic = resolution["sub_topic"]
            is_valid = resolution["is_valid"]
            reason = resolution["reason"]
            geo_info = resolution.get("geo_metadata")

        # Trace action formatting
        if not is_valid:
            action_desc = f"⚠️ Guardrail Rejection: Input '{target_city}' is not a valid geographical destination ({reason})."
        elif is_context_preserved:
            action_desc = f"🧠 Context Preserved: Intent '{intent}' on active destination '{target_city}' ({reason})."
        else:
            action_desc = f"🚀 New Destination Plan: Target city '{target_city}' ({reason})."

        trace_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "node": "PlanningAgent",
            "agent_role": "Planning, Context Transfer & Intent Resolution",
            "action": action_desc,
            "details": {
                "query": query,
                "intent": intent,
                "target_city": target_city,
                "is_context_preserved": is_context_preserved,
                "sub_topic": sub_topic,
                "is_valid_destination": is_valid,
                "guardrail_status": "PASSED" if is_valid else "REJECTED",
                "guardrail_reason": reason,
                "geo_metadata": geo_info,
                "classification_method": classification_method,
            }
        }

        return {
            "city": target_city,
            "query": query,
            "is_valid_destination": is_valid,
            "guardrail_error": None if is_valid else reason,
            "geo_metadata": geo_info,
            "is_weather_followup": (intent == "WEATHER_UPDATE"),
            "execution_trace": [trace_entry],
            "messages": [HumanMessage(content=query)],
        }

