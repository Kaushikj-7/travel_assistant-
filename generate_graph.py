"""
Research-Grade Architectural Topology & Workflow Diagram Generator.

Generates a publication-quality, 300-DPI architectural diagram of the
Voyager AI LangGraph multi-agent multi-modal system, illustrating:
1. Input Guardrails & Intent Extraction (Planning & Security)
2. The Switch: Dual-Track Retrieval (ChromaDB vs. Raw FastMCP Web Search)
3. Distinction 1: Manual Transmission Tool Calling Protocol
4. Distinction 2: Asynchronous Parallel Fan-Out (Open-Meteo & Wikimedia)
5. Distinction 3: State Memory Checkpointer & Time-Travel Context Preservation
6. Governance & Pydantic JSON Contract Aggregation
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def create_research_grade_diagram(output_path: str = "graph.png"):
    fig = plt.figure(figsize=(26, 17), dpi=300, facecolor="#080c14")
    ax = fig.add_axes([0, 0, 1, 1], facecolor="#080c14")
    ax.set_xlim(0, 260)
    ax.set_ylim(0, 170)
    ax.axis("off")

    # ── Color Palette (Academic Dark Luxury) ──────────────────────────
    C_TEXT_WHITE = "#f8fafc"
    C_TEXT_MUTED = "#94a3b8"
    C_TEXT_CYAN = "#38bdf8"

    C_INDIGO = "#4f46e5"
    C_CYAN = "#0284c7"
    C_EMERALD = "#059669"
    C_AMBER = "#d97706"
    C_ROSE = "#e11d48"
    C_PURPLE = "#7c3aed"
    C_SLATE = "#334155"
    C_GOLD = "#f59e0b"

    # ── Header & Academic Title ──────────────────────────────────────
    ax.text(130, 164, "VOYAGER AI — MULTI-MODAL AGENTIC ARCHITECTURE TOPOLOGY",
            ha="center", va="center", fontsize=22, fontweight="bold",
            color=C_TEXT_WHITE, family="sans-serif")
    
    subtitle = "Autonomous Multi-Agent Collaborative System with LangGraph StateGraph, FastMCP Protocol & Dual-Track Routing"
    ax.text(130, 159.5, subtitle,
            ha="center", va="center", fontsize=11.5, fontweight="medium",
            color=C_TEXT_MUTED, family="sans-serif")

    # State Tuple Mathematical Formulation
    math_state = r"$\mathbf{AgentState} = \langle \mathcal{Q}_{query}, \mathcal{M}_{messages}, \mathcal{C}_{city}, \mathcal{V}_{valid}, \mathcal{S}_{source}, \mathcal{W}_{weather}, \mathcal{I}_{images}, \mathcal{T}_{trace} \rangle$"
    ax.text(130, 155, math_state,
            ha="center", va="center", fontsize=11, fontweight="bold",
            color=C_TEXT_CYAN, family="sans-serif")

    # ── Group Box Helper ─────────────────────────────────────────────
    def draw_group_box(x, y, w, h, title, subtitle_txt, border_color, fill_color="#0f172a", alpha=0.92):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=2.5",
                             facecolor=fill_color, edgecolor=border_color, linewidth=1.5,
                             linestyle="--", alpha=alpha, zorder=1)
        ax.add_patch(box)
        ax.text(x + 3, y + h - 3.0, title.upper(), fontsize=9.2, fontweight="bold",
                color=border_color, family="sans-serif", zorder=2)
        if subtitle_txt:
            ax.text(x + 3, y + h - 5.8, subtitle_txt, fontsize=7.8, fontweight="normal",
                    color=C_TEXT_MUTED, family="sans-serif", zorder=2)

    # ── Node Card Helper ─────────────────────────────────────────────
    def draw_node_card(x, y, w, h, title, badge, desc_lines, header_color, bg_color="#1e293b", zorder=3):
        # Card Body
        card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=2.0",
                              facecolor=bg_color, edgecolor="#334155", linewidth=1.2,
                              zorder=zorder)
        ax.add_patch(card)
        
        # Card Header Accent
        header_h = 5.5
        hbar = FancyBboxPatch((x, y + h - header_h), w, header_h, boxstyle="round,pad=0.6,rounding_size=2.0",
                              facecolor=header_color, edgecolor=header_color, linewidth=0,
                              zorder=zorder + 1)
        ax.add_patch(hbar)
        ax.fill_between([x, x + w], [y + h - header_h, y + h - header_h], [y + h - 3.5, y + h - 3.5],
                        color=header_color, zorder=zorder + 1)

        # Title
        ax.text(x + 2.2, y + h - 3.0, title, fontsize=10.2, fontweight="bold",
                color="#ffffff", family="sans-serif", zorder=zorder + 2)
        
        # Badge
        if badge:
            bx = x + w - 2.2
            ax.text(bx, y + h - 3.0, badge, fontsize=7.5, fontweight="bold",
                    color="#ffffff", family="sans-serif", ha="right",
                    bbox=dict(boxstyle="round,pad=0.22", facecolor=(0, 0, 0, 0.4), edgecolor="none"),
                    zorder=zorder + 2)

        # Description Bullet Lines
        curr_y = y + h - 8.5
        for line in desc_lines:
            ax.text(x + 2.2, curr_y, line, fontsize=8.0, color=C_TEXT_MUTED,
                    family="sans-serif", zorder=zorder + 2)
            curr_y -= 2.8

    # ── Directed Arrow Helper ────────────────────────────────────────
    def draw_arrow(p1, p2, label="", color="#64748b", lw=2, curve=0, style="-|>", zorder=4):
        connectionstyle = f"arc3,rad={curve}" if curve != 0 else "arc3,rad=0"
        arrow = FancyArrowPatch(p1, p2,
                                arrowstyle=style,
                                connectionstyle=connectionstyle,
                                facecolor=color, edgecolor=color,
                                linewidth=lw, mutation_scale=13, zorder=zorder)
        ax.add_patch(arrow)
        if label:
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2 + (curve * 12)
            ax.text(mid_x, mid_y, label, fontsize=7.6, fontweight="bold",
                    color=color, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="#080c14", edgecolor=color, alpha=0.95),
                    zorder=zorder + 1)

    # ═════════════════════════════════════════════════════════════════
    # 1. SUBSYSTEM BOUNDARIES (GROUP BOXES)
    # ═════════════════════════════════════════════════════════════════

    # Top Row Subsystems: y = 80 to 148 (h = 68)
    # Subsystem 1: Input Ingestion & Planning
    draw_group_box(8, 80, 68, 68, "Subsystem 1: Planning & Security Guardrails",
                   "Intent Extraction, Geocoding & Fictional Entity Filtering", C_INDIGO)

    # Subsystem 2: The Switch (Dual-Track Knowledge Retrieval)
    draw_group_box(80, 80, 86, 68, "Subsystem 2: The Switch — Dual-Track Retrieval",
                   "Conditional Edge: Local ChromaDB vs. Raw FastMCP Web Intelligence", C_AMBER)

    # Subsystem 3: Asynchronous Parallel Fan-Out Subsystem
    draw_group_box(170, 80, 82, 68, "Subsystem 3: Asynchronous Parallel Fan-Out",
                   "Concurrent Non-Blocking Ingestion (Open-Meteo & Wikimedia)", C_PURPLE)

    # Bottom Row Subsystems: y = 14 to 68 (h = 54)
    # Subsystem 4: Governance & Pydantic Validation Subsystem
    draw_group_box(118, 14, 134, 54, "Subsystem 4: Governance, Validation & Synthesis",
                   "Schema Validation, Pydantic Contract & Multi-Modal Assembly", C_EMERALD)

    # Subsystem 5: Interactive Presentation & UI Layer
    draw_group_box(8, 14, 106, 54, "Subsystem 5: Interactive User Presentation Layer",
                   "Streamlit GUI, Plotly Weather Radar, Spatial Map & Follow-Up Loop", C_CYAN)

    # ═════════════════════════════════════════════════════════════════
    # 2. LANGGRAPH NODES (CARDS)
    # ═════════════════════════════════════════════════════════════════

    # Node: START
    draw_node_card(12, 94, 25, 38, "START", "Entrypoint", [
        "• User Query Input",
        "• Thread ID Binding",
        "• State Initialized",
        "• MemorySaver Seed"
    ], C_SLATE)

    # Node: parse_input
    draw_node_card(41, 88, 31, 48, "parse_input", "PlanningAgent", [
        "• LLM Intent Extraction",
        "• Guardrail Location Check",
        "• Open-Meteo Geocoding",
        "• Fictional Entity Filter",
        "• Time-Travel Parameter",
        "• Active City Memory"
    ], C_INDIGO)

    # Node: check_knowledge (The Switch Router)
    draw_node_card(84, 88, 31, 48, "check_knowledge", "Router Gate", [
        "• Chroma Cloud Semantic Query",
        "• Cosine Distance Evaluation",
        "• Exact Supported City Match",
        "• Guardrail Decision Flag",
        "• Branch: vector / web",
        "• Execution Trace Logging"
    ], C_AMBER)

    # Path A: vectorstore_retrieve
    draw_node_card(119, 118, 43, 20, "vectorstore_retrieve", "ChromaDB Path", [
        "• Chroma Cloud Tenant a84184bf...",
        "• Curated chunks: Paris, Tokyo, NYC",
        "• Zero-Latency Local Knowledge Assembly"
    ], C_EMERALD)

    # Path B: web_search (Distinction 1: Manual Transmission)
    draw_node_card(119, 90, 43, 22, "web_search", "Distinction 1", [
        "• FastMCP Protocol: `search_web`",
        "• Manual Tool Calls Payload Parsing",
        "• Explicit ToolMessage Construction",
        "• Zero Framework Abstraction Crutch"
    ], C_CYAN)

    # Distinction 2: Parallel Fan-Out Nodes
    # Node 1: fetch_weather
    draw_node_card(174, 118, 74, 20, "fetch_weather", "Fan-Out 1 (Weather)", [
        "• Open-Meteo Live API Ingestion & WMO Codes",
        "• 7-Day High/Low Temperatures & Precipitation",
        "• Deterministic Humidity & Wind Speed Modeling"
    ], C_PURPLE)

    # Node 2: fetch_images
    draw_node_card(174, 90, 74, 22, "fetch_images", "Fan-Out 2 (Visuals)", [
        "• Wikimedia Commons & Wikipedia PageImages API",
        "• Categorized Visual Assets (Landmarks, Skyline)",
        "• High-Res Image URLs & Licensing Metadata"
    ], C_ROSE)

    # Node: guardrail_rejected (Centered in clean middle corridor)
    draw_node_card(84, 70, 78, 8.5, "guardrail_rejected", "Security Block", [
        "• Short-circuit unverified/fictional destination • Zero-Hallucination Safe Explanations"
    ], C_ROSE)

    # Node: aggregate_response (Governance)
    draw_node_card(122, 16, 62, 42, "aggregate_response", "GovernanceAgent", [
        "• Pydantic Schema Validation (`TravelResponse`)",
        "• `city_summary`: Verified Curated Content",
        "• `weather_forecast`: 7-Day Meteorological Data",
        "• `image_urls`: High-Resolution Visual Gallery",
        "• `itinerary`: Multi-Day Thematic Schedule",
        "• `landmarks` & `cuisine` Structured Tables",
        "• Hallucination Prevention & Contract Enforcement"
    ], C_EMERALD)

    # Node: END
    draw_node_card(190, 20, 56, 34, "END", "Terminal", [
        "• State Persisted to MemorySaver",
        "• Multi-Turn Checkpoint Saved",
        "• Structured JSON Delivered",
        "• Streamlit GUI Render Triggered"
    ], C_SLATE)

    # UI Presentation Component Card
    draw_node_card(12, 16, 98, 42, "Streamlit Frontend GUI", "User Interface", [
        "• Cinematic Destination Hero Canvas with Weather & Badges",
        "• Destination Overview & Fast Facts Directory Table",
        "• 7-Day Meteorological Radar: Plotly Spline & Data Table",
        "• Spatial Landmark Attractions Map & Sights Directory Table",
        "• Authentic Gastronomy & Regional Cuisine Highlights Table",
        "• Curated Multi-Day Travel Itinerary Schedule Table",
        "• Verified High-Resolution Photography Gallery Grid",
        "• Distinction 3: Multi-Turn Time-Travel Follow-Up Loop"
    ], C_CYAN)

    # ═════════════════════════════════════════════════════════════════
    # 3. DIRECTED EDGES & DATA FLOW ARROWS
    # ═════════════════════════════════════════════════════════════════

    # START -> parse_input
    draw_arrow((37, 112), (41, 112), "Query", C_INDIGO, lw=2.2)

    # parse_input -> check_knowledge
    draw_arrow((72, 112), (84, 112), "Clean State", C_INDIGO, lw=2.2)

    # check_knowledge -> vectorstore_retrieve (Conditional Route A)
    draw_arrow((115, 128), (119, 128), "Found (Vector)", C_EMERALD, lw=2.2)

    # check_knowledge -> web_search (Conditional Route B - The Switch)
    draw_arrow((115, 101), (119, 101), "Miss (Web)", C_CYAN, lw=2.2)

    # check_knowledge -> guardrail_rejected (Conditional Route C)
    draw_arrow((99, 88), (99, 78.5), "Invalid", C_ROSE, lw=2.0)

    # Parallel Fan-Out from vectorstore_retrieve
    draw_arrow((162, 128), (174, 128), "Async Weather", C_PURPLE, lw=1.8)
    draw_arrow((162, 120), (174, 104), "", C_ROSE, lw=1.6, curve=-0.12)

    # Parallel Fan-Out from web_search
    draw_arrow((162, 104), (174, 120), "", C_PURPLE, lw=1.6, curve=0.12)
    draw_arrow((162, 96), (174, 96), "Async Images", C_ROSE, lw=1.8)

    # Parallel Fan-In (Convergence to aggregate_response)
    draw_arrow((205, 118), (180, 58), "Weather Data", C_PURPLE, lw=1.8, curve=0.10)
    draw_arrow((205, 90), (165, 58), "Image URLs", C_ROSE, lw=1.8, curve=-0.10)

    # Guardrail Rejected -> aggregate_response
    draw_arrow((123, 70), (132, 58), "Bypass Tools", C_ROSE, lw=1.8, curve=-0.15)

    # aggregate_response -> END
    draw_arrow((184, 37), (190, 37), "State", C_EMERALD, lw=2.2)

    # aggregate_response -> Streamlit UI
    draw_arrow((122, 37), (110, 37), "Pydantic JSON", C_CYAN, lw=2.4)

    # Time-Travel / MemorySaver Loop (Distinction 3) routed cleanly along left margin
    draw_arrow((8, 30), (41, 105), "Distinction 3: Time Travel State Loop (Active City + Date Delta)",
               C_GOLD, lw=2.2, curve=0.55, style="-|>")

    # ═════════════════════════════════════════════════════════════════
    # 4. FOOTER & ACADEMIC CITATION BADGES
    # ═════════════════════════════════════════════════════════════════
    footer_text = (
        "Architectural Citations: [1] Model Context Protocol (FastMCP) - arXiv:2510.19856v1  |  "
        "[2] Agentsway Collaborative Multi-Agent Framework - arXiv:2510.23664v1  |  "
        "[3] LangGraph StateGraph Execution Engine"
    )
    ax.text(130, 3.2, footer_text, ha="center", va="center", fontsize=8.5,
            fontweight="normal", color=C_TEXT_MUTED, family="sans-serif")

    # Distinction Badges Row at Bottom
    badges_info = [
        ("The Switch", "Intelligent Chroma/Web Dynamic Routing", C_AMBER),
        ("Distinction 1", "Manual Transmission Tool Calling", C_CYAN),
        ("Distinction 2", "Parallel Fan-Out Execution", C_PURPLE),
        ("Distinction 3", "Time-Travel Checkpointer Memory", C_GOLD),
        ("Enterprise Guardrail", "Zero-Hallucination Rejection Barrier", C_ROSE),
    ]

    bx_start = 12
    for title, desc, col in badges_info:
        badge_box = FancyBboxPatch((bx_start, 6.2), 44, 4.5, boxstyle="round,pad=0.3,rounding_size=1.0",
                                   facecolor="#0f172a", edgecolor=col, linewidth=1.2, zorder=2)
        ax.add_patch(badge_box)
        ax.text(bx_start + 22, 9.2, title, fontsize=8, fontweight="bold",
                color=col, ha="center", va="center", family="sans-serif", zorder=3)
        ax.text(bx_start + 22, 7.2, desc, fontsize=6.8, color=C_TEXT_MUTED,
                ha="center", va="center", family="sans-serif", zorder=3)
        bx_start += 47

    plt.savefig(output_path, dpi=300, facecolor="#080c14", edgecolor="none", bbox_inches="tight")
    plt.close()
    print(f"Publication-grade architectural diagram generated successfully: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
    create_research_grade_diagram(out)
