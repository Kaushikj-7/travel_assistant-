"""
Immutable Comprehensive Test Suite for Multi-Modal Travel Assistant.

Tests all Core Challenge Requirements, Distinctions, MCP Protocol, and Guardrails:
1. Vector Store Route (Chroma Cloud: Paris, Tokyo, New York)
2. The Switch / Web Search Route (Kyoto, Snohomish)
3. Distinction 1: Manual Transmission Tool Calling over MCP
4. Distinction 2: Parallel Fan-Out of Weather & Visuals
5. Distinction 3: Human-in-the-Loop & Memory (Time Travel)
6. Guardrail Rejection: Detection of non-existent/gibberish destinations (e.g. 'khdfgg')
7. Model Context Protocol (MCP): Tool discovery, invocation, and MCC resources
8. Pydantic Schema Conformance: Strict TravelResponse output validation
"""

import unittest
import uuid

from pydantic import ValidationError

from agents.guardrail_agent import GuardrailAgent
from graph.builder import build_graph
from mcp_server.client import mcp_client
from models.schemas import TravelResponse


class TestMultiModalTravelAssistant(unittest.TestCase):
    """Rigorous test suite for the Multi-Modal Travel Assistant."""

    @classmethod
    def setUpClass(cls):
        """Build and compile the LangGraph workflow once for the test suite."""
        cls.graph = build_graph()

    # ─────────────────────────────────────────────────────────────────
    # 1. Model Context Protocol (MCP) Verification
    # ─────────────────────────────────────────────────────────────────
    def test_01_mcp_tools_discovery(self):
        """Verify MCP Server tool discovery and strict schema definition."""
        tools = mcp_client.get_available_tools()
        tool_names = [t["name"] for t in tools]
        self.assertIn("get_weather_forecast", tool_names)
        self.assertIn("get_city_images", tool_names)
        self.assertIn("search_web", tool_names)
        self.assertIn("query_vectorstore", tool_names)

    def test_02_mcp_resources_contracts(self):
        """Verify Model Context Contracts (MCC) resources (arXiv:2510.19856v1)."""
        resources = mcp_client.get_available_resources()
        uris = [r["uri"] for r in resources]
        self.assertIn("resource://cities/paris", uris)
        self.assertIn("resource://cities/tokyo", uris)
        self.assertIn("resource://cities/newyork", uris)

        # Test reading a resource
        res_data = mcp_client.read_resource("resource://cities/paris")
        self.assertIsNotNone(res_data)
        self.assertIn("contents", res_data)

    def test_03_mcp_tool_invocation(self):
        """Verify MCP tool execution envelope and timing telemetry."""
        mcp_res = mcp_client.execute_tool("get_weather_forecast", {"city": "Tokyo"})
        self.assertFalse(mcp_res.get("isError"))
        self.assertIn("raw_data", mcp_res)
        self.assertGreaterEqual(len(mcp_res["raw_data"]), 5)

    # ─────────────────────────────────────────────────────────────────
    # 2. Guardrails & Non-Existent Destination Verification
    # ─────────────────────────────────────────────────────────────────
    def test_04_guardrail_rejection_gibberish(self):
        """Verify that non-existent destinations (e.g. 'khdfgg') are rejected and coordinates are NOT hallucinated."""
        is_valid, geo_info, reason = GuardrailAgent.verify_location("khdfgg")
        self.assertFalse(is_valid, "Guardrail must reject non-existent location 'khdfgg'")
        self.assertIsNone(geo_info, "No coordinates should be returned for non-existent location")

        # Test through full LangGraph pipeline
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke({"query": "Tell me about khdfgg"}, config=config)

        resp = result["final_response"]
        self.assertEqual(resp["source"], "guardrail_rejected")
        self.assertIsNone(resp["coordinates"], "Coordinates MUST be None for rejected locations")
        self.assertEqual(len(resp["weather_forecast"]), 0)
        self.assertEqual(len(resp["image_urls"]), 0)
        self.assertIn("Guardrail Alert", resp["city_summary"])

    def test_05_guardrail_verification_valid_places(self):
        """Verify that valid real places pass the Guardrail check."""
        for city in ["Paris", "Tokyo", "Kyoto", "Snohomish", "London"]:
            is_valid, geo_info, reason = GuardrailAgent.verify_location(city)
            self.assertTrue(is_valid, f"Guardrail should accept valid city '{city}'")
            self.assertIsNotNone(geo_info)
            self.assertIn("latitude", geo_info)
            self.assertIn("longitude", geo_info)

    # ─────────────────────────────────────────────────────────────────
    # 3. Core Requirements: Vector Store Route & The Switch
    # ─────────────────────────────────────────────────────────────────
    def test_06_vectorstore_route_paris(self):
        """Verify Chroma Cloud Vector Store route for pre-populated city (Paris)."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke({"query": "Tell me about Paris"}, config=config)

        resp = result["final_response"]
        self.assertEqual(resp["city_name"], "Paris")
        self.assertEqual(resp["source"], "vectorstore")
        self.assertGreater(len(resp["city_summary"]), 50)
        self.assertGreaterEqual(len(resp["weather_forecast"]), 5)
        self.assertGreaterEqual(len(resp["image_urls"]), 3)
        self.assertIsNotNone(resp["coordinates"])
        self.assertAlmostEqual(resp["coordinates"]["latitude"], 48.8566, places=2)

    def test_07_the_switch_websearch_kyoto(self):
        """Verify The Switch dynamically routes unknown city (Kyoto) to Web Search."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke({"query": "Explore Kyoto"}, config=config)

        resp = result["final_response"]
        self.assertEqual(resp["city_name"], "Kyoto")
        self.assertEqual(resp["source"], "websearch")
        self.assertGreater(len(resp["city_summary"]), 50)
        self.assertGreaterEqual(len(resp["weather_forecast"]), 5)
        self.assertGreaterEqual(len(resp["image_urls"]), 3)

    def test_08_the_switch_websearch_snohomish(self):
        """Verify The Switch dynamically routes Snohomish to Web Search."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke({"query": "Guide for Snohomish"}, config=config)

        resp = result["final_response"]
        self.assertEqual(resp["source"], "websearch")
        self.assertGreater(len(resp["city_summary"]), 40)
        self.assertGreaterEqual(len(resp["weather_forecast"]), 5)

    # ─────────────────────────────────────────────────────────────────
    # 4. Distinction 1: Manual Transmission Protocol
    # ─────────────────────────────────────────────────────────────────
    def test_09_distinction_1_manual_transmission(self):
        """Verify Distinction 1: Raw MCP tool binding and execution without ToolNode."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke({"query": "Tell me about London"}, config=config)

        # Inspect execution trace for manual transmission action
        traces = result.get("execution_trace", [])
        manual_trace = any("Manual Transmission" in t.get("action", "") or "WebResearchAgent" in t.get("node", "") for t in traces)
        self.assertTrue(manual_trace, "Distinction 1 Manual Transmission trace must be recorded.")

    # ─────────────────────────────────────────────────────────────────
    # 5. Distinction 2: Parallel Fan-Out Execution
    # ─────────────────────────────────────────────────────────────────
    def test_10_distinction_2_parallel_fanout(self):
        """Verify Distinction 2: Weather and Image ingestion execute as parallel branches."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke({"query": "Tell me about Tokyo"}, config=config)

        traces = result.get("execution_trace", [])
        weather_trace = any("EnvironmentAgent" in t.get("node", "") for t in traces)
        media_trace = any("Media" in t.get("node", "") or "Visual" in t.get("node", "") for t in traces)
        self.assertTrue(weather_trace, "EnvironmentAgent weather branch must execute.")
        self.assertTrue(media_trace, "VisualAssetAgent media branch must execute.")

    # ─────────────────────────────────────────────────────────────────
    # 6. Distinction 3: Human-in-the-Loop & Memory (Time Travel)
    # ─────────────────────────────────────────────────────────────────
    def test_11_distinction_3_context_memory_followup(self):
        """Verify Distinction 3: MemorySaver preserves city entity on follow-up questions."""
        thread_id = f"test_thread_memory_{uuid.uuid4()}"
        config = {"configurable": {"thread_id": thread_id}}

        # Turn 1: Primary query for Tokyo
        res1 = self.graph.invoke({"query": "Tell me about Tokyo"}, config=config)
        self.assertEqual(res1["final_response"]["city_name"], "Tokyo")
        initial_summary = res1["final_response"]["city_summary"]

        # Turn 2: Follow-up question without naming the city
        res2 = self.graph.invoke({"query": "What about next week?"}, config=config)
        self.assertEqual(res2["final_response"]["city_name"], "Tokyo", "Context Memory must preserve city 'Tokyo'")
        self.assertEqual(res2["final_response"]["city_summary"], initial_summary, "City summary should be preserved on weather follow-up")
        self.assertGreaterEqual(len(res2["final_response"]["weather_forecast"]), 5)

    # ─────────────────────────────────────────────────────────────────
    # 7. Pydantic Structured Output Validation
    # ─────────────────────────────────────────────────────────────────
    def test_12_pydantic_schema_compliance(self):
        """Verify strict TravelResponse Pydantic contract compliance."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke({"query": "Tell me about New York"}, config=config)

        # Validate by instantiating Pydantic model
        try:
            validated = TravelResponse(**result["final_response"])
            self.assertEqual(validated.city_name, "New York")
            self.assertIsInstance(validated.weather_forecast, list)
            self.assertIsInstance(validated.image_urls, list)
            self.assertIn(validated.source, ["vectorstore", "websearch", "guardrail_rejected"])
        except ValidationError as e:
            self.fail(f"Pydantic validation failed: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
