"""
Web Search & Encyclopedic Intelligence Tool.

Provides verified destination intelligence from Wikipedia API and curated encyclopedia.
Strictly returns verified data or empty on unverified destinations (No generic hallucinations).
"""

import json
import urllib.parse
import urllib.request
from typing import Optional

from langchain_core.tools import tool

# Curated high-fidelity knowledge for key destinations
CURATED_DESTINATIONS = {
    "kyoto": (
        "Kyoto, Japan — Kyoto served as Japan's imperial capital from 794 until 1868. "
        "It houses over 2,000 Buddhist temples and Shinto shrines, including 17 UNESCO World Heritage Sites "
        "such as Kinkaku-ji (the Golden Pavilion), Fushimi Inari-taisha with its iconic torii gates, and the serene "
        "Arashiyama Bamboo Forest. Kyoto is the cultural cradle of traditional Japanese tea ceremony (chado), "
        "geisha arts in Gion, kaiseki gastronomy, and historic wooden machiya townhouses."
    ),
    "snohomish": (
        "Snohomish, Washington — Snohomish is known as the 'Antique Capital of the Northwest,' situated in "
        "Snohomish County along the Snohomish River. Founded in the mid-19th century, the city features a charming "
        "Historic Downtown district listed on the National Register of Historic Places, filled with vintage shops, "
        "artisan bakeries, and historic Victorian architecture. It is also famous for hot-air ballooning, river kayaking, "
        "and farm-to-table culinary experiences across the Snohomish River Valley."
    ),
    "london": (
        "London, United Kingdom — London is the capital of England and the UK, standing on the River Thames. "
        "With a two-millennium Roman heritage (Londinium), it boasts world-renowned landmarks including the Tower of "
        "London, Buckingham Palace, the British Museum, the Tate Modern, and Westminster Abbey. London is a global "
        "hub for arts, finance, West End theater, and Michelin-starred culinary diversity."
    ),
    "sydney": (
        "Sydney, Australia — Built around one of the world's most spectacular natural harbors, Sydney is famed for "
        "the Sydney Opera House, Harbour Bridge, and Bondi Beach. The city offers coastal walks from Bondi to Coogee, "
        "the Royal Botanic Garden, and a thriving contemporary food scene blending Asian and Mediterranean influences."
    ),
    "dubai": (
        "Dubai, United Arab Emirates — Dubai is a global metropolis on the Persian Gulf, celebrated for ultra-modern "
        "architecture including the Burj Khalifa (828 m, tallest building in the world), luxury shopping malls, and "
        "the Palm Jumeirah archipelago. It combines historic souks with futuristic desert hospitality and fine dining."
    ),
    "rome": (
        "Rome, Italy — The Eternal City is home to nearly three millennia of history, art, and architecture. "
        "Major sites include the Colosseum, the Pantheon, the Roman Forum, and Vatican City with St. Peter's Basilica. "
        "Famous for classic Roman cuisine like carbonara and cacio e pepe, vibrant piazzas, and the Trevi Fountain."
    ),
}


def _fetch_live_wikipedia(query: str) -> Optional[str]:
    """Retrieve comprehensive encyclopedic intelligence from Wikipedia REST & Action APIs."""
    city_term = query.replace("travel", "").replace("explore", "").replace("visit", "").replace("info", "").replace("Guide for", "").replace("guide to", "").strip()
    encoded = urllib.parse.quote(city_term)
    
    sections = []
    
    # 1. Summary REST API (lead paragraph & description)
    try:
        url_summary = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        req1 = urllib.request.Request(url_summary, headers={"User-Agent": "ProductionTravelAssistant/2.0 (contact: admin@travel.ai)"})
        with urllib.request.urlopen(req1, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            page_type = data.get("type", "")
            extract = data.get("extract")
            description = data.get("description", "")
            title = data.get("title", "")
            
            if page_type != "disambiguation" and extract and len(extract) > 80:
                desc_str = f" ({description})" if description else ""
                sections.append(f"### Overview of {title}{desc_str}\n{extract}")
    except Exception:
        pass

    # 2. Detailed Extract API for richer cultural & geographical context
    try:
        url_extract = (
            f"https://en.wikipedia.org/w/api.php?"
            f"action=query&prop=extracts&exintro=1&explaintext=1&titles={encoded}&format=json"
        )
        req2 = urllib.request.Request(url_extract, headers={"User-Agent": "ProductionTravelAssistant/2.0 (contact: admin@travel.ai)"})
        with urllib.request.urlopen(req2, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, pinfo in pages.items():
                full_extract = pinfo.get("extract", "")
                if full_extract and len(full_extract) > 200:
                    # If this provides more depth than just the short summary
                    if not sections or len(full_extract) > len(sections[0]):
                        sections = [f"### Factual Destination Brief for {pinfo.get('title', city_term.title())}\n{full_extract}"]
                    break
    except Exception:
        pass

    if sections:
        return "\n\n".join(sections)
    return None


@tool
def search_web(query: str) -> str:
    """Search the web for verified encyclopedic destination intelligence.

    Args:
        query: Destination name or travel query.

    Returns:
        A detailed string containing factual intelligence about the destination.
    """
    # 1. Attempt live Wikipedia search
    try:
        live_res = _fetch_live_wikipedia(query)
        if live_res and len(live_res) > 80:
            return live_res
    except Exception:
        pass

    # 2. Check curated encyclopedia
    query_lower = query.lower()
    for city_key, result in CURATED_DESTINATIONS.items():
        if city_key in query_lower:
            return result

    # Return empty string if no factual information could be found
    return ""
