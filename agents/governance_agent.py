"""
Governance & Testing Agent — Agentsway Methodology (2510.23664v1) & OpenAI Agents Guardrails.

Role:
- Validates data integrity and enforces Pydantic schema contract (TravelResponse)
- Enforces Guardrail Rejections on unverified / non-existent destinations (NEVER hallucinates fake coordinates)
- Uses verified real-world geocoordinates from Open-Meteo Geocoding / ChromaDB
- Integrates authentic destination intelligence, landmarks, cuisine, and multi-day itinerary
"""

from datetime import datetime
from typing import Any, Dict

from langchain_core.messages import AIMessage

from models.schemas import (
    Coordinates,
    CuisineItem,
    LandmarkPoint,
    TravelImage,
    TravelResponse,
    WeatherDataPoint,
)
from tools.destination_intel import get_destination_intelligence
from utils.logger import logger


class GovernanceAndTestingAgent:
    """Agent responsible for output aggregation, quality validation, guardrails, and schema conformance."""

    @staticmethod
    def aggregate_and_validate(state: Dict[str, Any]) -> Dict[str, Any]:
        city = state.get("city", "").strip()
        is_valid = state.get("is_valid_destination", True)
        guardrail_error = state.get("guardrail_error")
        geo_meta = state.get("geo_metadata") or {}

        # ── 1. Guardrail Rejection Handler ───────────────────────────
        if not is_valid or state.get("source") == "guardrail_rejected":
            reject_msg = (
                f"⚠️ **Guardrail Alert**: The location **'{city}'** could not be found or verified in any global "
                f"geographic database.\n\n"
                f"**Reason**: {guardrail_error or 'Non-existent destination or invalid input.'}\n\n"
                f"Please verify your destination spelling (e.g. *Paris, Tokyo, New York, Kyoto, London, Snohomish, Dubai, Rome*)."
            )

            travel_response = TravelResponse(
                city_name=city.title() if city else "Unknown Destination",
                city_summary=reject_msg,
                weather_forecast=[],
                image_urls=[],
                images=[],
                source="guardrail_rejected",
                itinerary=None,
                coordinates=None,
                landmarks=None,
                cuisine=None,
            )

            trace_entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
                "node": "GovernanceAgent",
                "agent_role": "Testing, Governance & Output Guardrail",
                "action": f"⚠️ Output Guardrail: Rejected unverified destination '{city}'. Blocked coordinate hallucination.",
                "details": {
                    "pydantic_schema": "TravelResponse",
                    "guardrail_status": "REJECTED",
                    "guardrail_error": guardrail_error,
                    "coordinates": None,
                    "weather_points_count": 0,
                    "images_count": 0,
                }
            }

            return {
                "final_response": travel_response.model_dump(),
                "execution_trace": [trace_entry],
                "messages": [AIMessage(content=f"Guardrail rejected unverified destination '{city}'.")],
            }

        # ── 2. Verified Destination Deep Intelligence ────────────────
        intel = get_destination_intelligence(city, geo_meta)
        
        # Summary resolution
        state_summary = state.get("city_summary", "").strip()
        summary = state_summary if state_summary else intel.get("overview", f"Travel guide for {city.title()}.")
        
        forecast_raw = state.get("weather_forecast", [])
        images = state.get("image_urls", [])
        media_items_raw = state.get("media_items", [])
        source = state.get("source", "websearch")

        # Weather forecast deduplication & validation
        weather_points = []
        seen_dates = set()
        for item in forecast_raw:
            if isinstance(item, dict):
                d = item.get("date")
                if d and d not in seen_dates:
                    seen_dates.add(d)
                    try:
                        weather_points.append(WeatherDataPoint(**item))
                    except Exception as e:
                        logger.warning(f"Failed to parse weather point: {e}")
                        continue

        # Image URLs and TravelImage deduplication
        seen_imgs = set()
        clean_images = []
        structured_images = []

        if media_items_raw:
            for m in media_items_raw:
                if isinstance(m, dict):
                    u = m.get("url")
                    if u and u not in seen_imgs:
                        seen_imgs.add(u)
                        clean_images.append(u)
                        try:
                            structured_images.append(TravelImage(**m))
                        except Exception as e:
                            logger.warning(f"Failed to parse travel image: {e}")
                            pass

        for img in images:
            if isinstance(img, str) and img not in seen_imgs:
                seen_imgs.add(img)
                clean_images.append(img)
                structured_images.append(TravelImage(
                    url=img,
                    title=f"{city.title()} Landmark",
                    category="Photography",
                    attribution="Verified Media"
                ))

        # Real-world Geocoordinates resolution
        coords = None
        if "latitude" in geo_meta and "longitude" in geo_meta:
            coords = Coordinates(
                latitude=float(geo_meta["latitude"]),
                longitude=float(geo_meta["longitude"])
            )

        # Landmarks conversion
        landmarks_list = []
        for lm in intel.get("landmarks", []):
            try:
                landmarks_list.append(LandmarkPoint(**lm))
            except Exception as e:
                logger.warning(f"Failed to parse landmark point: {e}")
                pass

        # Cuisine conversion
        cuisine_list = []
        for c in intel.get("cuisine", []):
            try:
                cuisine_list.append(CuisineItem(**c))
            except Exception as e:
                logger.warning(f"Failed to parse cuisine item: {e}")
                pass

        # Multi-day Itinerary
        itinerary = intel.get("itinerary")

        # Enforce Pydantic TravelResponse contract
        travel_response = TravelResponse(
            city_name=city.title() if city else "Destination",
            city_summary=summary,
            weather_forecast=weather_points,
            image_urls=clean_images[:6],
            images=structured_images[:6],
            source=source,
            itinerary=itinerary,
            coordinates=coords,
            landmarks=landmarks_list,
            cuisine=cuisine_list,
            country=intel.get("country"),
            currency=intel.get("currency"),
            language=intel.get("language"),
            timezone=intel.get("timezone"),
            best_season=intel.get("best_season"),
            transit_info=intel.get("transit_info"),
        )

        trace_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "node": "GovernanceAgent",
            "agent_role": "Testing, Governance & Schema Contract",
            "action": f"Validated output against Pydantic TravelResponse contract (Forecast: {len(weather_points)}, Images: {len(clean_images)}, Itinerary: {len(itinerary) if itinerary else 0} days, Landmarks: {len(landmarks_list)}).",
            "details": {
                "pydantic_schema": "TravelResponse",
                "guardrail_status": "PASSED",
                "weather_points_count": len(weather_points),
                "images_count": len(clean_images),
                "itinerary_days": len(itinerary) if itinerary else 0,
                "landmarks_count": len(landmarks_list),
                "coordinates": coords.model_dump() if coords else None,
                "source": source,
            }
        }

        return {
            "final_response": travel_response.model_dump(),
            "execution_trace": [trace_entry],
            "messages": [AIMessage(content=f"Governance validation passed for {city.title()}.")],
        }
