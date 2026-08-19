"""
Graph node implementations for Multi-Modal Travel Assistant.

Dispatches each workflow step to its dedicated Agentsway Agent role,
leveraging MCP tools and protocol contracts.
"""

import os

from dotenv import load_dotenv

from agents.environment_agent import EnvironmentAndMediaAgent
from agents.governance_agent import GovernanceAndTestingAgent
from agents.planning_agent import PlanningAgent
from agents.retrieval_agent import RetrievalAgent
from agents.web_agent import WebResearchAgent

load_dotenv()


def _get_llm(state: dict):
    """Retrieve an initialized LLM client (OpenAI or Anthropic) if API key is provided."""
    api_key = state.get("api_key") or os.getenv("OPENAI_API_KEY", "") or os.getenv("ANTHROPIC_API_KEY", "")
    api_key = api_key.strip()
    model_name = state.get("model_name") or "gpt-4o-mini"

    if api_key and not api_key.startswith("sk-your") and len(api_key) > 10:
        if "claude" in model_name.lower():
            try:
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(model=model_name, temperature=0, api_key=api_key)
            except Exception:
                pass
        else:
            try:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(model=model_name, temperature=0, api_key=api_key)
            except Exception:
                pass
    return None


def parse_input(state: dict) -> dict:
    """Node 1: Planning Agent parses input and manages conversation memory."""
    llm = _get_llm(state)
    agent = PlanningAgent(llm=llm)
    return agent.execute_plan(state)


def check_knowledge(state: dict) -> dict:
    """Node 2: Retrieval Agent queries ChromaDB via MCP and routes The Switch."""
    llm = _get_llm(state)
    agent = RetrievalAgent(llm=llm)
    return agent.check_knowledge_availability(state)


def vectorstore_retrieve(state: dict) -> dict:
    """Node 3a: Retrieval Agent synthesizes verified ChromaDB knowledge."""
    llm = _get_llm(state)
    agent = RetrievalAgent(llm=llm)
    return agent.synthesize_knowledge(state)


def web_search(state: dict) -> dict:
    """Node 3b: Web Research Agent performs live MCP tool execution (Distinction 1)."""
    llm = _get_llm(state)
    agent = WebResearchAgent(llm=llm)
    return agent.execute_research(state)


def fetch_weather(state: dict) -> dict:
    """Node 4a: Environment Agent executes parallel weather ingestion via MCP (Distinction 2)."""
    return EnvironmentAndMediaAgent.fetch_weather(state)


def fetch_images(state: dict) -> dict:
    """Node 4b: Media Agent executes parallel image asset ingestion via MCP (Distinction 2)."""
    return EnvironmentAndMediaAgent.fetch_images(state)


def aggregate_response(state: dict) -> dict:
    """Node 5: Governance & Testing Agent enforces Pydantic schema contract."""
    return GovernanceAndTestingAgent.aggregate_and_validate(state)
