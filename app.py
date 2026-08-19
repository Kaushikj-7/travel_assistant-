"""
Voyager AI — Enterprise Multi-Modal Travel Intelligence & Autonomous Agentic Workflow

Architectural Reference:
- LangGraph v1.2 StateGraph & MemorySaver Checkpointer
- Model Context Protocol (MCP - arXiv:2510.19856v1) Server & Client Bridge
- Agentsway Collaborative Multi-Agent Lifecycle (arXiv:2510.23664v1)
- Enterprise Input/Output Guardrails & Zero-Hallucination Policy
- Multi-Marker Interactive Spatial Mapping & Landmark Extraction
- 7-Day Meteorological Forecast Radar & Interactive Plotly Charts
- Verified Regional Gastronomy & 3-Day Curated Itinerary Engine
- Authentic Categorized Media & Lightbox Visual Gallery
"""

import os
import uuid
import json
import time
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

from mcp_server.client import mcp_client
from graph.builder import build_graph

load_dotenv()

# ── Page Configuration ───────────────────────────────────────────────
st.set_page_config(
    page_title="Voyager — AI Travel Concierge",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Luxury Styling & Modern Aesthetic Design System ──────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #4f46e5;
        --primary-light: #818cf8;
        --accent: #f43f5e;
        --emerald: #10b981;
        --amber: #f59e0b;
        --slate-900: #0f172a;
        --slate-800: #1e293b;
        --slate-700: #334155;
        --slate-600: #475569;
        --slate-500: #64748b;
        --slate-100: #f1f5f9;
        --slate-50: #f8fafc;
        --card-border: rgba(226, 232, 240, 0.85);
        --glass-bg: rgba(255, 255, 255, 0.85);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1e293b;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 4rem;
        max-width: 1260px;
    }

    /* ── Cinematic Destination Hero Cover ── */
    .dest-hero-canvas {
        position: relative;
        border-radius: 26px;
        overflow: hidden;
        margin-bottom: 2rem;
        min-height: 280px;
        background-size: cover;
        background-position: center;
        box-shadow: 0 20px 45px -12px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .dest-hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.25) 0%, rgba(15, 23, 42, 0.82) 65%, rgba(15, 23, 42, 0.96) 100%);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 2.5rem 2.8rem;
    }
    .dest-hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        margin: 0;
        line-height: 1.1;
        text-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .dest-hero-sub {
        font-size: 1.15rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.85);
        margin-top: 0.4rem;
        margin-bottom: 1.2rem;
    }
    .hero-pills-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        align-items: center;
    }
    .hero-glass-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #ffffff;
        padding: 0.4rem 0.95rem;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 600;
    }
    .hero-glass-pill-highlight {
        background: rgba(79, 70, 229, 0.35);
        border-color: rgba(129, 140, 248, 0.45);
        color: #e0e7ff;
    }

    /* ── App Top Header ── */
    .app-brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0 1.4rem;
    }
    .app-brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #1e293b 0%, #4f46e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .app-brand-tag {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
    }

    /* ── Search Bar Styling ── */
    .stTextInput > div > div > input {
        border-radius: 16px !important;
        padding: 0.85rem 1.25rem !important;
        font-size: 1.05rem !important;
        border: 1.5px solid #cbd5e1 !important;
        background: #ffffff !important;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05) !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.12) !important;
    }

    /* ── Cards & Glass Panels ── */
    .luxury-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.8rem 2rem;
        border: 1px solid var(--card-border);
        box-shadow: 0 10px 30px -8px rgba(15, 23, 42, 0.05);
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .luxury-card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Telemetry Grid ── */
    .vitals-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 0.85rem;
        margin: 1.2rem 0 1.8rem;
    }
    .vital-card {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        border: 1px solid #e2e8f0;
        transition: transform 0.15s ease;
    }
    .vital-card:hover {
        transform: translateY(-2px);
        background: #ffffff;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
    }
    .vital-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .vital-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 0.25rem;
    }

    /* ── Weather Glass Grid ── */
    .forecast-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.75rem;
        margin-bottom: 1.4rem;
    }
    .forecast-card {
        background: linear-gradient(160deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 18px;
        padding: 1.2rem 0.6rem;
        text-align: center;
        border: 1.5px solid #e2e8f0;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }
    .forecast-card:hover {
        transform: translateY(-4px);
        border-color: #818cf8;
        box-shadow: 0 12px 24px -6px rgba(79, 70, 229, 0.15);
    }
    .fc-day { font-size: 0.78rem; font-weight: 700; color: #64748b; text-transform: uppercase; }
    .fc-icon { font-size: 2.2rem; margin: 0.4rem 0; }
    .fc-high { font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 800; color: #0f172a; }
    .fc-low { font-size: 0.85rem; font-weight: 600; color: #64748b; }
    .fc-cond { font-size: 0.75rem; color: #475569; margin-top: 0.35rem; font-weight: 500; }

    /* ── Landmark & Food Cards ── */
    .sight-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.85rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.02);
    }
    .sight-card:hover {
        transform: translateX(4px);
        border-color: #cbd5e1;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }
    .sight-title { font-size: 1rem; font-weight: 700; color: #0f172a; }
    .sight-desc { font-size: 0.88rem; color: #475569; margin-top: 0.3rem; line-height: 1.5; }

    /* ── Itinerary Timeline ── */
    .timeline-step {
        position: relative;
        padding-left: 1.5rem;
        margin-bottom: 1.2rem;
        border-left: 2px solid #e2e8f0;
    }
    .timeline-badge {
        position: absolute;
        left: -9px;
        top: 0;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #4f46e5;
        border: 3px solid #ffffff;
        box-shadow: 0 0 0 2px #c7d2fe;
    }
    .act-tag-morning { background: #fef3c7; color: #b45309; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.72rem; }
    .act-tag-afternoon { background: #e0f2fe; color: #0369a1; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.72rem; }
    .act-tag-evening { background: #f3e8ff; color: #7e22ce; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.72rem; }

    /* ── Modern Photography Grid ── */
    .photo-frame {
        border-radius: 18px;
        overflow: hidden;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.2rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .photo-frame:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 32px -8px rgba(15, 23, 42, 0.12);
    }
    .photo-frame img {
        width: 100%;
        aspect-ratio: 16 / 10;
        object-fit: cover;
        display: block;
    }
    .photo-caption-bar {
        padding: 0.9rem 1.1rem;
    }
    .photo-caption-title { font-size: 0.92rem; font-weight: 700; color: #0f172a; }
    .photo-caption-meta { font-size: 0.76rem; color: #64748b; display: flex; justify-content: space-between; margin-top: 0.3rem; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Initialize State & Compiled Graph ─────────────────────────────────
@st.cache_resource
def get_compiled_workflow():
    return build_graph()

graph = get_compiled_workflow()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ── Sidebar Configuration ────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧭 Experience Mode")
    view_mode = st.radio(
        "Interface Mode",
        ["👤 Traveler Experience", "🛠️ Developer Inspector"],
        index=0,
        label_visibility="collapsed",
        help="Switch between consumer travel deck and developer diagnostic inspector."
    )
    is_dev_mode = (view_mode == "🛠️ Developer Inspector")
    st.divider()

    if is_dev_mode:
        st.markdown("### ⚙️ Multi-Agent Settings")
        default_key = os.getenv("OPENAI_API_KEY", "")
        user_api_key = st.text_input(
            "API Key (OpenAI / Claude)",
            value="" if default_key.startswith("sk-your") else default_key,
            type="password",
            help="Optional: Live LLM inference key. Local fallback executes deterministically.",
        )

        model_choice = st.selectbox(
            "Reasoning Engine",
            ["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet"],
            index=0,
        )

        st.divider()
        st.markdown("### 🏛️ Architecture Specs")
        st.caption("• **Orchestration**: LangGraph v1.2 StateGraph")
        st.caption("• **Tool Protocol**: FastMCP (arXiv:2510.19856v1)")
        st.caption("• **Multi-Agent Methodology**: Agentsway (2510.23664v1)")
        st.caption("• **Vector Store**: Chroma Cloud / In-Memory")
        st.caption("• **Weather**: Open-Meteo Meteorological API")
        st.caption("• **Guardrails**: Zero-Hallucination Location Filter")
        st.divider()
    else:
        user_api_key = os.getenv("OPENAI_API_KEY", "")
        model_choice = "gpt-4o-mini"
        st.markdown("### 🌟 About Voyager")
        st.caption("Voyager is your AI travel concierge, delivering curated destination guides, live 7-day meteorological forecasts, interactive maps, and authentic photography for destinations worldwide.")
        st.divider()

    st.caption(f"Session: `{st.session_state.thread_id[:8]}...`")
    if st.button("🔄 New Destination / Reset", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.history = []
        st.session_state.chat_messages = []
        st.session_state.pending_query = None
        st.rerun()


# ── Top App Brand Bar ────────────────────────────────────────────────
col_b1, col_b2 = st.columns([3, 1])
with col_b1:
    st.markdown("""
    <div class="app-brand-bar">
        <div>
            <div class="app-brand-title">✈️ Voyager AI</div>
            <div class="app-brand-tag">Intelligent Multi-Modal Travel Concierge & Agentic Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Quick Destination Recommendation Carousel ────────────────────────
st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #64748b; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.05em;'>POPULAR DESTINATIONS:</p>", unsafe_allow_html=True)
col_q1, col_q2, col_q3, col_q4, col_q5, col_q6 = st.columns(6)

quick_query = None
with col_q1:
    if st.button("🗼 Paris", use_container_width=True): quick_query = "Tell me about Paris"
with col_q2:
    if st.button("⛩️ Kyoto", use_container_width=True): quick_query = "Explore Kyoto"
with col_q3:
    if st.button("🗽 New York", use_container_width=True): quick_query = "Tell me about New York"
with col_q4:
    if st.button("🏯 Tokyo", use_container_width=True): quick_query = "Explore Tokyo"
with col_q5:
    if st.button("🌲 Snohomish", use_container_width=True): quick_query = "Guide for Snohomish"
with col_q6:
    if st.button("🏰 London", use_container_width=True): quick_query = "Tell me about London"


# ── Search Input Form ────────────────────────────────────────────────
with st.form("voyager_search_form", clear_on_submit=False):
    col_input, col_submit = st.columns([5, 1.2])
    with col_input:
        user_input = st.text_input(
            "Destination Search",
            placeholder="Search any destination worldwide (e.g. 'Explore Paris', 'Tell me about Kyoto', 'Guide for Rome', or follow-up 'What about next week?')",
            label_visibility="collapsed",
        )
    with col_submit:
        submitted = st.form_submit_button("Explore ➔", use_container_width=True)

# Resolve active query from all potential triggers (form, quick button, pending follow-up)
active_query = quick_query or (user_input if submitted else None) or st.session_state.pending_query
st.session_state.pending_query = None


# ── LangGraph Workflow Execution ─────────────────────────────────────
if active_query and active_query.strip():
    query_text = active_query.strip()
    status_label = f"🤖 **Agentsway Team** executing multi-modal workflow for: **{query_text}**" if is_dev_mode else f"✨ Planning travel guide for **{query_text}**..."
    status_card = st.status(status_label, expanded=is_dev_mode)
    
    step_traces = []
    final_output = None

    try:
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        initial_state = {
            "query": query_text,
            "messages": [],
            "weather_forecast": [],
            "image_urls": [],
            "execution_trace": [],
            "api_key": user_api_key.strip() if user_api_key else None,
            "model_name": model_choice,
        }

        if is_dev_mode:
            status_card.write("🔍 **Input Guardrail**: Evaluating destination entity with global geographic authority...")
        else:
            status_card.write("🔍 Verifying geographical coordinates & destination authority...")

        api_url = os.getenv("API_URL")
        use_backend = os.getenv("USE_API_BACKEND", "false").lower() in ("true", "1", "yes") or bool(api_url)
        event_generator = None

        if use_backend:
            target_url = api_url or "http://localhost:8000"
            try:
                import requests
                import sseclient
                response = requests.post(
                    f"{target_url}/chat/stream",
                    json={"thread_id": st.session_state.thread_id, "message": query_text},
                    stream=True,
                    timeout=2
                )
                response.raise_for_status()
                client = sseclient.SSEClient(response)
                event_generator = (json.loads(event.data) for event in client.events())
            except Exception:
                status_card.write("⚠️ **API Backend Unreachable**: Falling back to local execution engine...")
                event_generator = graph.stream(initial_state, config=config, stream_mode="updates")
        else:
            event_generator = graph.stream(initial_state, config=config, stream_mode="updates")

        for event in event_generator:
            for node_name, node_update in event.items():
                if node_name == "parse_input":
                    extracted = node_update.get("city", "")
                    is_valid = node_update.get("is_valid_destination", True)
                    is_fu = node_update.get("is_weather_followup", False)
                    fu_str = " *(Preserved Context: Time Travel)*" if is_fu else ""

                    if is_dev_mode:
                        if is_valid:
                            status_card.write(f"🧠 **PlanningAgent & Guardrail**: Verified destination → `{extracted}`{fu_str}")
                        else:
                            status_card.write(f"🛡️ **Guardrail Alert**: `{extracted}` is not a recognized real-world destination. Short-circuiting execution.")
                    else:
                        if is_valid:
                            status_card.write(f"📍 Destination verified: **{extracted}**")
                        else:
                            status_card.write(f"⚠️ Destination could not be verified: **{extracted}**")

                elif node_name == "check_knowledge":
                    route = node_update.get("source", "")
                    if is_dev_mode:
                        if route == "vectorstore":
                            status_card.write("🗄️ **RetrievalAgent** (Chroma Cloud): Local knowledge verified → **Vector Store Path**")
                        elif route == "guardrail_rejected":
                            status_card.write("🛡️ **RetrievalAgent**: Guardrail active → Bypassing external tools.")
                        else:
                            status_card.write("🌐 **RetrievalAgent**: Not in vector store → **The Switch** activated → **Live Web Research Path**")
                    else:
                        status_card.write("🔍 Exploring destination highlights & insights...")

                elif node_name == "vectorstore_retrieve":
                    if is_dev_mode:
                        status_card.write("📚 **RetrievalAgent**: Synthesized guide from verified Chroma Cloud chunks.")
                    else:
                        status_card.write("📚 Compiling curated travel highlights...")

                elif node_name == "web_search":
                    if is_dev_mode:
                        status_card.write("🌐 **WebResearchAgent** (🏆 Distinction 1: Manual Transmission): Executed `search_web` over MCP & appended ToolMessage.")
                    else:
                        status_card.write("🌐 Discovering top landmarks, culture & local dining...")

                elif node_name == "fetch_weather":
                    count = len(node_update.get("weather_forecast", []))
                    if is_dev_mode:
                        status_card.write(f"🌤️ **EnvironmentAgent** (🏆 Distinction 2: Parallel Fan-Out): Ingested {count}-day Open-Meteo forecast.")
                    else:
                        status_card.write(f"🌤️ Ingesting 7-day meteorological forecast...")

                elif node_name == "fetch_images":
                    count = len(node_update.get("image_urls", []))
                    if is_dev_mode:
                        status_card.write(f"📸 **VisualAssetAgent** (🏆 Distinction 2: Parallel Fan-Out): Ingested {count} categorized photos.")
                    else:
                        status_card.write(f"📸 Curating high-resolution photography...")

                elif node_name == "aggregate_response":
                    if is_dev_mode:
                        status_card.write("🛡️ **GovernanceAgent**: Validated structured Pydantic `TravelResponse` contract & itinerary.")
                    else:
                        status_card.write("✨ Finalizing travel guide...")
                    final_output = node_update.get("final_response")

                if "execution_trace" in node_update:
                    step_traces.extend(node_update["execution_trace"])

        done_label = "✅ Agentsway Multi-Agent Workflow Completed!" if is_dev_mode else "✅ Travel Guide Ready!"
        status_card.update(label=done_label, state="complete", expanded=is_dev_mode)

        if final_output:
            st.session_state.history.append({
                "query": query_text,
                "response": final_output,
                "traces": step_traces,
            })
            st.session_state.chat_messages.append({"role": "user", "content": query_text})
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": final_output.get("city_summary", ""),
                "response": final_output
            })

    except Exception as e:
        status_card.update(label=f"❌ Error during agent execution: {e}", state="error", expanded=True)
        st.exception(e)


# ── Render Latest Destination Deck ───────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[-1]
    response = latest["response"]
    traces = latest.get("traces", [])

    city_name = response.get("city_name", "Destination")
    city_summary = response.get("city_summary", "")
    weather_forecast = response.get("weather_forecast", [])
    image_urls = response.get("image_urls", [])
    structured_images = response.get("images", [])
    source = response.get("source", "websearch")
    itinerary = response.get("itinerary", [])
    coords = response.get("coordinates")
    landmarks = response.get("landmarks", [])
    cuisine = response.get("cuisine", [])
    country = response.get("country", "")
    currency = response.get("currency", "")
    language = response.get("language", "")
    timezone = response.get("timezone", "")
    best_season = response.get("best_season", "")
    transit_info = response.get("transit_info", "")

    # ═════════════════════════════════════════════════════════════════
    # VIEW 1: GUARDRAIL REJECTION
    # ═════════════════════════════════════════════════════════════════
    if source == "guardrail_rejected":
        with st.container(border=True):
            st.markdown(f"""
            <div style="background: #fef2f2; border: 1.5px solid #fecaca; border-radius: 16px; padding: 1.8rem 2rem; margin-bottom: 1rem;">
                <h3 style="color: #991b1b; font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 800; margin-top: 0; margin-bottom: 0.6rem;">
                    🛡️ Security & Verification Guardrail Alert
                </h3>
                <p style="font-size: 1.02rem; color: #7f1d1d; margin-bottom: 0.8rem; line-height: 1.6;">{city_summary}</p>
                <hr style="border: 0; border-top: 1px solid rgba(153, 27, 27, 0.2); margin: 0.8rem 0;">
                <p style="font-size: 0.85rem; color: #991b1b; margin: 0; font-weight: 600;">
                    <b>Zero-Hallucination Policy</b>: Non-existent, fictional, or unverified locations are strictly blocked from generating synthetic coordinates, weather, or maps.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.info("💡 **Looking for inspiration?** Try exploring verified destinations like **Paris**, **Tokyo**, **Kyoto**, **New York**, **Snohomish**, **London**, **Rome**, or **Dubai**.")

    # ═════════════════════════════════════════════════════════════════
    # VIEW 2: CINEMATIC DESTINATION EXPERIENCE
    # ═════════════════════════════════════════════════════════════════
    else:
        # Hero Cover Background Image
        hero_img = image_urls[0] if image_urls else "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1600&auto=format&fit=crop&q=80"
        
        # Weather pill for hero
        hero_weather_str = ""
        if weather_forecast:
            first_day = weather_forecast[0]
            hero_weather_str = f"🌤️ {first_day.get('temperature_high', 0)}°C {first_day.get('condition', '')}"

        # ── 1. Destination Hero Banner ──
        st.markdown(f"""
        <div class="dest-hero-canvas" style="background-image: url('{hero_img}');">
            <div class="dest-hero-overlay">
                <div class="dest-hero-title">{city_name}</div>
                <div class="dest-hero-sub">{f'Destination in {country}' if country else 'Global Destination'}</div>
                <div class="hero-pills-row">
                    {f'<span class="hero-glass-pill hero-glass-pill-highlight">{hero_weather_str}</span>' if hero_weather_str else ''}
                    {f'<span class="hero-glass-pill">📍 {coords["latitude"]:.2f}°, {coords["longitude"]:.2f}°</span>' if coords and isinstance(coords, dict) else ''}
                    {f'<span class="hero-glass-pill">💰 {currency}</span>' if currency else ''}
                    {f'<span class="hero-glass-pill">🗣️ {language}</span>' if language else ''}
                    {f'<span class="hero-glass-pill">🗓️ {best_season}</span>' if best_season else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 2. Destination Story & Vitals Table ──
        with st.container(border=True):
            st.markdown("### 📖 Destination Overview & Travel Vitals")
            col_ov, col_vit = st.columns([1.5, 1])
            with col_ov:
                st.markdown(city_summary)
                if transit_info:
                    st.markdown(f"**🚇 Public Transit & Getting Around**: {transit_info}")
            with col_vit:
                st.markdown("**📊 Destination Fast Facts**")
                vitals_df = pd.DataFrame([
                    {"Attribute": "Country", "Value": country or "Global"},
                    {"Attribute": "Coordinates", "Value": f"{coords['latitude']:.4f}° N, {coords['longitude']:.4f}° E" if coords and isinstance(coords, dict) else "Verified"},
                    {"Attribute": "Currency", "Value": currency or "Local Currency"},
                    {"Attribute": "Language", "Value": language or "Official Language"},
                    {"Attribute": "Timezone", "Value": timezone or "Local Timezone"},
                    {"Attribute": "Best Season", "Value": best_season or "Spring / Autumn"},
                ])
                st.dataframe(vitals_df, use_container_width=True, hide_index=True)

        # ── 3. 7-Day Meteorological Radar & Forecast Table ──
        if weather_forecast:
            with st.container(border=True):
                st.markdown("### 🌤️ 7-Day Meteorological Radar (Open-Meteo Live API)")
                
                # Visual KPI Cards Row
                condition_emojis = {
                    "sunny": "☀️", "clear": "☀️", "clear sky": "☀️", "mainly clear": "🌤️",
                    "partly cloudy": "⛅", "cloudy": "☁️", "overcast": "☁️", "light rain": "🌦️",
                    "rainy": "🌧️", "rain showers": "🌧️", "scattered showers": "🌦️",
                    "slight rain": "🌦️", "moderate rain": "🌧️", "heavy rain": "🌧️",
                    "drizzle": "🌧️", "thunderstorm": "⛈️", "humid": "💧",
                    "hot & humid": "🌡️", "hot": "🔥", "breezy": "🍃", "warm": "🌤️", "hazy": "🌫️",
                }

                fc_cols = st.columns(len(weather_forecast))
                for col, day in zip(fc_cols, weather_forecast):
                    emoji = condition_emojis.get(day.get("condition", "").lower(), "🌡️")
                    date_str = day.get("date", "")[-5:]
                    with col:
                        st.markdown(f"""
                        <div class="forecast-card">
                            <div class="fc-day">{date_str}</div>
                            <div class="fc-icon">{emoji}</div>
                            <div class="fc-high">{day.get('temperature_high', 0)}°C</div>
                            <div class="fc-low">Low {day.get('temperature_low', 0)}°C</div>
                            <div class="fc-cond">{day.get('condition', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col_w_chart, col_w_table = st.columns([1.3, 1])
                with col_w_chart:
                    # Plotly Spline Chart
                    dates = [d.get("date", "") for d in weather_forecast]
                    highs = [d.get("temperature_high", 0) for d in weather_forecast]
                    lows = [d.get("temperature_low", 0) for d in weather_forecast]

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=dates, y=highs,
                        name="Day High (°C)",
                        mode="lines+markers",
                        line=dict(color="#f43f5e", width=3.5, shape="spline"),
                        marker=dict(size=8, color="#f43f5e"),
                        hovertemplate="<b>%{x}</b><br>High: %{y}°C<extra></extra>",
                    ))
                    fig.add_trace(go.Scatter(
                        x=dates, y=lows,
                        name="Night Low (°C)",
                        mode="lines+markers",
                        line=dict(color="#6366f1", width=3.5, shape="spline"),
                        marker=dict(size=8, color="#6366f1"),
                        fill="tonexty",
                        fillcolor="rgba(244, 63, 94, 0.08)",
                        hovertemplate="<b>%{x}</b><br>Low: %{y}°C<extra></extra>",
                    ))
                    fig.update_layout(
                        height=280,
                        margin=dict(l=15, r=15, t=15, b=15),
                        yaxis_title="Temperature (°C)",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        hovermode="x unified",
                    )
                    fig.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
                    fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
                    st.plotly_chart(fig, use_container_width=True)

                with col_w_table:
                    st.markdown("**📋 7-Day Meteorological Data Table**")
                    weather_table_rows = [
                        {
                            "Date": d.get("date", ""),
                            "Condition": d.get("condition", ""),
                            "High": f"{d.get('temperature_high', 0)}°C",
                            "Low": f"{d.get('temperature_low', 0)}°C",
                            "Precipitation": f"{d.get('precipitation_sum', 0)} mm",
                            "Est. Humidity": f"{d.get('humidity', 0)}%",
                        }
                        for d in weather_forecast
                    ]
                    st.dataframe(pd.DataFrame(weather_table_rows), use_container_width=True, hide_index=True)

        # ── 4. Spatial Map & Landmark Attractions Table ──
        with st.container(border=True):
            st.markdown("### 📍 Spatial Geolocation & Iconic Sights")
            col_map_view, col_lm_table = st.columns([1.2, 1.2])

            with col_map_view:
                st.markdown("**🗺️ Interactive Landmark Map**")
                map_points = []
                if coords and isinstance(coords, dict):
                    map_points.append({"lat": coords["latitude"], "lon": coords["longitude"], "name": f"{city_name} Center"})
                if landmarks:
                    for lm in landmarks:
                        if isinstance(lm, dict) and "lat" in lm and "lon" in lm:
                            map_points.append({"lat": lm["lat"], "lon": lm["lon"], "name": lm.get("name", "Landmark")})

                if map_points:
                    map_df = pd.DataFrame(map_points)
                    st.map(map_df, zoom=11, use_container_width=True)

            with col_lm_table:
                st.markdown("**🏛️ Landmarks & Attractions Directory**")
                if landmarks:
                    lm_rows = [
                        {
                            "Landmark": lm.get("name", "") if isinstance(lm, dict) else str(lm),
                            "Category": lm.get("category", "Landmark") if isinstance(lm, dict) else "Landmark",
                            "Description": lm.get("desc", "") if isinstance(lm, dict) else "",
                        }
                        for lm in landmarks
                    ]
                    st.dataframe(pd.DataFrame(lm_rows), use_container_width=True, hide_index=True)
                else:
                    st.caption("General city attractions are highlighted in the overview. Search specific sights for detail.")

        # ── 5. Gastronomy & Regional Cuisine Table ──
        if cuisine:
            with st.container(border=True):
                st.markdown("### 🍽️ Authentic Gastronomy & Regional Cuisine")
                food_rows = [
                    {
                        "Dish / Specialty": dish.get("name", "") if isinstance(dish, dict) else str(dish),
                        "Description": dish.get("desc", "") if isinstance(dish, dict) else "Local culinary specialty.",
                    }
                    for dish in cuisine
                ]
                st.dataframe(pd.DataFrame(food_rows), use_container_width=True, hide_index=True)

        # ── 6. Multi-Day Curated Itinerary Schedule ──
        if itinerary:
            with st.container(border=True):
                st.markdown("### 📅 Curated Multi-Day Travel Itinerary")
                itin_rows = []
                for day_info in itinerary:
                    day_num = day_info.get("day", 1)
                    day_theme = day_info.get("theme", "")
                    dining = day_info.get("dining_recommendation", "")
                    activities = day_info.get("activities", [])

                    with st.expander(f"📌 **Day {day_num}: {day_theme}**", expanded=True):
                        for act in activities:
                            tod = act.get("time_of_day", "Activity")
                            tag_cls = f"act-tag-{tod.lower()}" if tod.lower() in ["morning", "afternoon", "evening"] else "act-tag-morning"
                            loc_str = f"📍 <i>{act.get('location')}</i> — " if act.get("location") else ""
                            st.markdown(f"""
                            <div class="timeline-step">
                                <div class="timeline-badge"></div>
                                <span class="{tag_cls}">{tod}</span> <b>{act.get('title')}</b><br>
                                <span style="color: #475569; font-size: 0.9rem;">{loc_str}{act.get('description')}</span>
                            </div>
                            """, unsafe_allow_html=True)
                            itin_rows.append({
                                "Day": f"Day {day_num}",
                                "Theme": day_theme,
                                "Time": tod,
                                "Activity": act.get("title", ""),
                                "Location": act.get("location", ""),
                                "Description": act.get("description", ""),
                                "Dining Recommendation": dining or "Local Eatery"
                            })
                        if dining:
                            st.markdown(f"🍽️ **Dining Pick:** {dining}")

                if itin_rows:
                    st.markdown("**📋 Complete Itinerary Schedule Table**")
                    st.dataframe(pd.DataFrame(itin_rows), use_container_width=True, hide_index=True)

        # ── 7. Verified Photography Gallery ──
        if structured_images or image_urls:
            with st.container(border=True):
                st.markdown("### 📸 Verified Destination Photography")
                photo_cols = st.columns(3)
                display_list = structured_images if structured_images else [{"url": u, "title": f"{city_name} Landmark", "category": "Photography", "attribution": "Verified Media"} for u in image_urls]

                for i, img_item in enumerate(display_list):
                    u = img_item.get("url") if isinstance(img_item, dict) else img_item
                    t = img_item.get("title", f"{city_name} View") if isinstance(img_item, dict) else f"{city_name} View"
                    c = img_item.get("category", "General") if isinstance(img_item, dict) else "General"
                    a = img_item.get("attribution", "") if isinstance(img_item, dict) else ""

                    with photo_cols[i % 3]:
                        st.markdown(f"""
                        <div class="photo-frame">
                            <img src="{u}" alt="{t}">
                            <div class="photo-caption-bar">
                                <div class="photo-caption-title">{t}</div>
                                <div class="photo-caption-meta">
                                    <span style="font-weight: 700; color: #4f46e5;">{c}</span>
                                    <span>{a}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        # ── 8. Interactive Follow-Up Assistant (Time Travel / Distinction 3) ──
        with st.container(border=True):
            st.markdown("### 💬 Ask a Follow-Up Question")
            st.caption("Ask questions about this destination. Multi-turn context memory is preserved across turns.")
            
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                if st.button("🌦️ What about next week?", use_container_width=True):
                    st.session_state.pending_query = "What about next week?"
                    st.rerun()
            with col_f2:
                if st.button(f"🍜 Best food in {city_name}?", use_container_width=True):
                    st.session_state.pending_query = f"What are the best places to eat in {city_name}?"
                    st.rerun()
            with col_f3:
                if st.button(f"🚇 Transit tips for {city_name}?", use_container_width=True):
                    st.session_state.pending_query = f"How do I use public transit in {city_name}?"
                    st.rerun()
            with col_f4:
                if st.button(f"🏛️ Top museums in {city_name}?", use_container_width=True):
                    st.session_state.pending_query = f"What are the top museums in {city_name}?"
                    st.rerun()

    # ═════════════════════════════════════════════════════════════════
    # DEVELOPER, MCP & ARCHITECTURAL INSPECTOR PANEL (ONLY IN DEV MODE)
    # ═════════════════════════════════════════════════════════════════
    if is_dev_mode:
        with st.expander("🛠️ **Developer & Protocol Inspector (FastMCP, LangGraph & Schema)**", expanded=True):
            dev_tab1, dev_tab2, dev_tab3, dev_tab4, dev_tab5 = st.tabs([
                "🔌 FastMCP Tools & Wire Logs",
                "👥 Agentsway Team",
                "🧠 Node Execution Trace",
                "📄 Pydantic JSON Contract",
                "🕸️ LangGraph Topology",
            ])

            with dev_tab1:
                st.markdown("#### Model Context Protocol (FastMCP - arXiv:2510.19856v1)")
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.markdown("**Discovered Tools (`tools/list`):**")
                    for t in mcp_client.get_available_tools():
                        st.caption(f"• **{t['name']}**: {t['description']}")
                with col_m2:
                    st.markdown("**Recent Wire Calls (`tools/call`):**")
                    for h in reversed(mcp_client.get_call_history()[-4:]):
                        st.caption(f"• `[{h['timestamp']}]` **{h['tool']}** ({h['duration']}s)")

            with dev_tab2:
                st.markdown("""
| Role | Agent Class | Function |
| :--- | :--- | :--- |
| **🧠 Planning** | `PlanningAgent` | LLM intent extraction, conversation memory & time-travel parameter updates |
| **🛡️ Guardrails** | `GuardrailAgent` | Authoritative geocoding verification & fictional entity detection |
| **🗄️ Retrieval** | `RetrievalAgent` | Chroma Cloud semantic vector query & The Switch routing |
| **🌐 Web Intelligence** | `WebResearchAgent` | Raw MCP tool calling protocol (Distinction 1: Manual Transmission) |
| **🌤️ Environment** | `EnvironmentAndMediaAgent` | Open-Meteo weather & Wikimedia photo ingestion (Distinction 2: Fan-Out) |
| **🛡️ Governance** | `GovernanceAndTestingAgent` | Pydantic schema validation & hallucination prevention |
                """)

            with dev_tab3:
                st.markdown("**Step-by-Step Node Execution Events:**")
                for t in traces:
                    st.caption(f"• `[{t.get('timestamp')}]` **{t.get('node')}**: {t.get('action')}")

            with dev_tab4:
                st.json(response)

            with dev_tab5:
                if os.path.exists("graph.png"):
                    st.image("graph.png", caption="LangGraph StateGraph Topology Visualization", use_container_width=True)

else:
    # ── Clean Luxury Empty State ─────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2.5, 1])
    with c2:
        with st.container(border=True):
            st.markdown("""
            <div style="text-align: center; padding: 2.5rem 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.6rem;">✨</div>
                <h2 style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.8rem; color: #0f172a; margin-bottom: 0.4rem; letter-spacing: -0.02em;">
                    Where will your journey take you?
                </h2>
                <p style="color: #64748b; font-size: 1rem; max-width: 500px; margin: 0 auto 1.5rem; line-height: 1.6;">
                    Experience verified travel intelligence with live 7-day meteorological forecasts, interactive landmark maps, curated culinary guides, and authentic photography.
                </p>
                <div style="display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="hero-glass-pill" style="background: #f1f5f9; color: #334155; border-color: #cbd5e1;">✨ Curated Highlights</span>
                    <span class="hero-glass-pill" style="background: #f1f5f9; color: #334155; border-color: #cbd5e1;">🌤️ Live 7-Day Forecast</span>
                    <span class="hero-glass-pill" style="background: #f1f5f9; color: #334155; border-color: #cbd5e1;">📍 Spatial Landmark Maps</span>
                    <span class="hero-glass-pill" style="background: #f1f5f9; color: #334155; border-color: #cbd5e1;">📸 Verified Photography</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

