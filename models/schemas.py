"""
Pydantic schemas for the Multi-Modal Travel Assistant.

Enforces strict structured output contract as required by the challenge rubric
and enriched with patterns from enterprise travel planner agents (itinerary planning,
geocoordinates, weather telemetry, landmarks, and categorized image assets).
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class WeatherDataPoint(BaseModel):
    """A single day's meteorological forecast point."""

    date: str = Field(description="Date in YYYY-MM-DD format")
    temperature_high: float = Field(description="High temperature in Celsius")
    temperature_low: float = Field(description="Low temperature in Celsius")
    condition: str = Field(description="Weather condition (e.g. Sunny, Partly Cloudy, Rain)")
    humidity: int = Field(description="Humidity percentage (0-100)")
    wind_speed: float = Field(description="Wind speed in km/h")


class TravelImage(BaseModel):
    """An authentic photograph of the destination with category and attribution."""

    url: str = Field(description="High-resolution image URL")
    title: str = Field(description="Landmark or scene title")
    category: str = Field(description="Category: Landmark, Architecture, Culture, Gastronomy, Skyline, Scenic")
    attribution: Optional[str] = Field(default=None, description="Attribution or source")


class LandmarkPoint(BaseModel):
    """A specific verified landmark with coordinates for interactive mapping."""

    name: str = Field(description="Name of the landmark or attraction")
    lat: float = Field(description="Latitude coordinate")
    lon: float = Field(description="Longitude coordinate")
    desc: str = Field(description="Factual description")
    category: str = Field(description="Category: Historic, Museum, Landmark, Scenic, Nature")


class CuisineItem(BaseModel):
    """A verified local culinary specialty."""

    name: str = Field(description="Dish or food specialty name")
    desc: str = Field(description="Description and cultural significance")


class Activity(BaseModel):
    """A single curated travel activity."""

    time_of_day: str = Field(description="Time of day: Morning, Afternoon, Evening")
    title: str = Field(description="Activity or attraction title")
    description: str = Field(description="Concise description of the experience")
    location: Optional[str] = Field(default=None, description="Landmark name or area")


class ItineraryDay(BaseModel):
    """A single day's structured travel itinerary."""

    day: int = Field(description="Day number (e.g. 1, 2, 3)")
    theme: str = Field(description="Day theme or focus area")
    activities: List[Activity] = Field(description="Scheduled activities for morning, afternoon, evening")
    dining_recommendation: Optional[str] = Field(default=None, description="Recommended dining or culinary specialty")


class Coordinates(BaseModel):
    """Geographic coordinates for interactive map rendering."""

    latitude: float = Field(description="Latitude in decimal degrees")
    longitude: float = Field(description="Longitude in decimal degrees")


class TravelResponse(BaseModel):
    """
    Core Structured Output contract produced by GovernanceAgent and consumed by Streamlit.

    Must-Haves (Rubric Baseline):
      - city_name: str
      - city_summary: str
      - weather_forecast: List[WeatherDataPoint]
      - image_urls: List[str]
      - source: str ('vectorstore' | 'websearch')

    Enriched Enterprise Features:
      - images: Optional[List[TravelImage]]
      - itinerary: Optional[List[ItineraryDay]]
      - coordinates: Optional[Coordinates]
      - landmarks: Optional[List[LandmarkPoint]]
      - cuisine: Optional[List[CuisineItem]]
      - country: Optional[str]
      - currency: Optional[str]
      - language: Optional[str]
      - timezone: Optional[str]
      - best_season: Optional[str]
      - transit_info: Optional[str]
    """

    city_name: str = Field(description="Name of the destination city")
    city_summary: str = Field(description="Rich narrative summary of the destination")
    weather_forecast: List[WeatherDataPoint] = Field(description="5-7 day weather forecast")
    image_urls: List[str] = Field(description="High-resolution photography URLs")
    source: str = Field(description="Data source: 'vectorstore' or 'websearch'")
    images: Optional[List[TravelImage]] = Field(default=None, description="Categorized authentic photographs")
    itinerary: Optional[List[ItineraryDay]] = Field(default=None, description="Curated multi-day itinerary")
    coordinates: Optional[Coordinates] = Field(default=None, description="Geographic coordinates")
    landmarks: Optional[List[LandmarkPoint]] = Field(default=None, description="Key landmarks with coordinates")
    cuisine: Optional[List[CuisineItem]] = Field(default=None, description="Regional culinary highlights")
    country: Optional[str] = Field(default=None, description="Country name")
    currency: Optional[str] = Field(default=None, description="Local currency")
    language: Optional[str] = Field(default=None, description="Primary language")
    timezone: Optional[str] = Field(default=None, description="Timezone name")
    best_season: Optional[str] = Field(default=None, description="Recommended season to visit")
    transit_info: Optional[str] = Field(default=None, description="Transit & getting around details")
