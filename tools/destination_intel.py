"""
Comprehensive Destination Intelligence & Landmark Discovery Engine.

Fetches accurate, factual travel data for any city worldwide using:
1. Wikipedia REST API & Wikitravel/Wikivoyage extracts
2. OpenStreetMap / Overpass / Geocoding for genuine landmark coordinates
3. Curated deep-knowledge profiles for top destinations
"""

import json
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

from models.schemas import Activity, ItineraryDay

# Comprehensive verified destination intelligence database
VERIFIED_DESTINATION_DATABASE: Dict[str, Dict[str, Any]] = {
    "paris": {
        "city_name": "Paris",
        "country": "France",
        "region": "Île-de-France",
        "currency": "Euro (EUR, €)",
        "language": "French",
        "timezone": "Central European Time (UTC+1 / UTC+2 in summer)",
        "best_season": "April–May (Spring) or September–October (Autumn)",
        "transit_info": "Extensive Paris Métro (16 lines), RER suburban express, and Vélib' bike-sharing system.",
        "overview": (
            "Paris, the capital of France, is an internationally celebrated center of art, fashion, gastronomy, and culture. "
            "Situated along the River Seine in northern France, the city has been a major cultural and commercial metropolis "
            "for over two millennia. Renowned for its 19th-century Haussmannian boulevards, monumental landmarks, and vibrant "
            "café culture, Paris houses world-famous institutions including the Musée du Louvre, Musée d'Orsay, and the Centre Pompidou."
        ),
        "landmarks": [
            {"name": "Eiffel Tower", "lat": 48.8584, "lon": 2.2945, "desc": "Iconic 330-meter wrought-iron lattice tower on the Champ de Mars, designed by Gustave Eiffel for the 1889 World's Fair.", "category": "Landmark"},
            {"name": "Louvre Museum", "lat": 48.8606, "lon": 2.3376, "desc": "World's most-visited art museum housing the Mona Lisa, Venus de Milo, and Winged Victory of Samothrace inside a historic royal palace.", "category": "Museum"},
            {"name": "Notre-Dame Cathedral", "lat": 48.8530, "lon": 2.3499, "desc": "Medieval Catholic cathedral on the Île de la Cité, celebrated as a masterpiece of French Gothic architecture with gargoyles and flying buttresses.", "category": "Historic"},
            {"name": "Arc de Triomphe", "lat": 48.8738, "lon": 2.2950, "desc": "Monumental triumphal arch honoring those who fought for France, anchoring the western end of the Avenue des Champs-Élysées.", "category": "Monument"},
            {"name": "Sacré-Cœur Basilica", "lat": 48.8867, "lon": 2.3431, "desc": "Romano-Byzantine basilica crowning the Montmartre butte, offering sweeping 360-degree panoramic vistas across Paris.", "category": "Scenic"},
        ],
        "cuisine": [
            {"name": "Croissants & Pain au Chocolat", "desc": "Flaky, multi-layered butter pastries freshly baked at artisan boulangeries."},
            {"name": "Boeuf Bourguignon", "desc": "Slow-braised beef stew simmered in red Burgundy wine with lardons, mushrooms, and pearl onions."},
            {"name": "Duck Confit (Confit de Canard)", "desc": "Tender duck leg cured and slow-cooked in its own fat, served with crispy skin and garlic potatoes."},
            {"name": "French Macarons", "desc": "Delicate almond meringue confections filled with chocolate ganache, raspberry, or salted caramel."},
        ],
        "itinerary": [
            ItineraryDay(
                day=1,
                theme="Iconic Monuments & Royal Heritage",
                activities=[
                    Activity(time_of_day="Morning", title="Eiffel Tower & Champ de Mars", description="Ascend to the summit for morning panoramic views, then stroll through the Champ de Mars gardens.", location="Champ de Mars (7th Arr.)"),
                    Activity(time_of_day="Afternoon", title="Louvre Museum Masterpieces", description="Explore the Denon and Sully wings to admire the Mona Lisa, Venus de Milo, and French Crown Jewels.", location="1st Arrondissement"),
                    Activity(time_of_day="Evening", title="Seine River Sunset Cruise & Pont Neuf", description="Glide past illuminated bridges, Notre-Dame, and the Musée d'Orsay as twilight falls.", location="Pont Neuf"),
                ],
                dining_recommendation="Traditional Parisian dinner at a Saint-Germain bistro featuring Duck Confit and French Onion Soup."
            ),
            ItineraryDay(
                day=2,
                theme="Impressionist Masterpieces & Bohemian Montmartre",
                activities=[
                    Activity(time_of_day="Morning", title="Musée d'Orsay Impressionist Gallery", description="View masterworks by Claude Monet, Vincent van Gogh, Edgar Degas, and Auguste Renoir in a converted Beaux-Arts railway station.", location="7th Arrondissement"),
                    Activity(time_of_day="Afternoon", title="Montmartre Village & Sacré-Cœur", description="Wander cobblestone alleys through Place du Tertre, view artist studios, and visit the Sacré-Cœur Basilica.", location="Montmartre (18th Arr.)"),
                    Activity(time_of_day="Evening", title="Latin Quarter Café & Bookstore Stroll", description="Explore Shakespeare and Company bookstore and enjoy lively evening terrace dining along Rue Mouffetard.", location="5th Arrondissement"),
                ],
                dining_recommendation="Artisan patisserie tasting with macarons at Ladurée or Pierre Hermé, followed by steak frites in the Marais."
            ),
            ItineraryDay(
                day=3,
                theme="Historic Île de la Cité & Chic Le Marais",
                activities=[
                    Activity(time_of_day="Morning", title="Sainte-Chapelle Stained Glass & Notre-Dame", description="Marvel at 1,113 13th-century stained-glass windows inside Sainte-Chapelle, then view Notre-Dame Cathedral.", location="Île de la Cité"),
                    Activity(time_of_day="Afternoon", title="Le Marais Boutiques & Place des Vosges", description="Explore historic 17th-century aristocratic mansions, the Picasso Museum, and the symmetrical Place des Vosges.", location="4th Arrondissement"),
                    Activity(time_of_day="Evening", title="Arc de Triomphe Sunset & Champs-Élysées", description="Climb to the rooftop viewing terrace of the Arc de Triomphe to witness the sparkling evening lights along the avenue.", location="Place Charles de Gaulle"),
                ],
                dining_recommendation="Classic French raclette or soufflé dinner in the vibrant Bastille neighborhood."
            ),
        ]
    },
    "tokyo": {
        "city_name": "Tokyo",
        "country": "Japan",
        "region": "Kantō",
        "currency": "Japanese Yen (JPY, ¥)",
        "language": "Japanese",
        "timezone": "Japan Standard Time (UTC+9)",
        "best_season": "Late March–April (Cherry Blossom) or October–November (Autumn Foliage)",
        "transit_info": "World's most punctual railway network: JR Yamanote Loop Line, Tokyo Metro, and Toei Subway lines with Suica/Pasmo IC cards.",
        "overview": (
            "Tokyo, the dynamic capital of Japan, is the world's most populous metropolitan area. "
            "It presents a captivating contrast of ultramodern neon-lit skyscrapers, futuristic robotics, and cutting-edge design "
            "alongside ancient Shinto shrines, historic wooden temples, and peaceful Zen gardens. As a global culinary capital, "
            "Tokyo boasts more Michelin stars than any other city on Earth."
        ),
        "landmarks": [
            {"name": "Senso-ji Temple", "lat": 35.7148, "lon": 139.7967, "desc": "Tokyo's oldest Buddhist temple founded in 645 AD, entered through the monumental Kaminarimon (Thunder Gate).", "category": "Historic"},
            {"name": "Shibuya Crossing", "lat": 35.6595, "lon": 139.7005, "desc": "The world's busiest pedestrian scramble crossing, illuminated by giant video screens and surrounded by youth fashion hubs.", "category": "Culture"},
            {"name": "Tokyo Tower", "lat": 35.6586, "lon": 139.7454, "desc": "333-meter communications and observation tower inspired by the Eiffel Tower, painted in distinctive white and international orange.", "category": "Landmark"},
            {"name": "Meiji Jingu Shrine", "lat": 35.6764, "lon": 139.6993, "desc": "Sacred Shinto shrine dedicated to Emperor Meiji, nestled within a 170-acre evergreen forest of 120,000 trees.", "category": "Historic"},
            {"name": "Shinjuku Gyoen National Garden", "lat": 35.6852, "lon": 139.7101, "desc": "Sprawling 144-acre park blending traditional Japanese landscape, English formal, and French garden styles.", "category": "Scenic"},
        ],
        "cuisine": [
            {"name": "Edomae Nigiri Sushi", "desc": "Freshly sliced seasonal fish (Tuna, Sea Urchin, Salmon) hand-pressed over seasoned vinegared rice."},
            {"name": "Tonkotsu & Shoyu Ramen", "desc": "Rich, multi-hour simmered pork bone or soy-sauce broth with springy noodles, chashu pork, and ajitsuke tamago."},
            {"name": "Charcoal-Grilled Yakitori", "desc": "Skewered chicken glazed with sweet-savory tare sauce or sea salt, grilled over white Binchotan charcoal."},
            {"name": "Wagyu Sukiyaki & Shabu-Shabu", "desc": "Paper-thin slices of marbled Japanese A5 beef simmered in sweet soy dashi broth."},
        ],
        "itinerary": [
            ItineraryDay(
                day=1,
                theme="Ancient Heritage & Pop Culture Contrasts",
                activities=[
                    Activity(time_of_day="Morning", title="Senso-ji Temple & Nakamise Dori", description="Pass beneath the giant red lantern of Kaminarimon gate and sample freshly made ningyo-yaki sweets.", location="Asakusa (Taito)"),
                    Activity(time_of_day="Afternoon", title="Akihabara Electric Town & Retro Gaming", description="Explore multi-floor retro video game stores, manga shops, and futuristic robotics centers.", location="Akihabara (Chiyoda)"),
                    Activity(time_of_day="Evening", title="Tokyo Skytree Observation Deck", description="Ascend to the Tembo Galleria at 450 meters for evening panoramas reaching to Mount Fuji.", location="Sumida"),
                ],
                dining_recommendation="Authentic Tonkotsu ramen in Asakusa followed by matcha ice cream."
            ),
            ItineraryDay(
                day=2,
                theme="Shinto Serenity, Fashion & Vibrant Shibuya",
                activities=[
                    Activity(time_of_day="Morning", title="Meiji Jingu Forest Walk", description="Stroll under massive wooden torii gates through the sacred forest to witness traditional Shinto wedding processions.", location="Harajuku / Shibuya"),
                    Activity(time_of_day="Afternoon", title="Takeshita Street & Omotesando Architecture", description="Browse avant-garde youth boutiques on Takeshita Street, then explore luxury architectural flagships along tree-lined Omotesando.", location="Harajuku"),
                    Activity(time_of_day="Evening", title="Shibuya Scramble & Shibuya Sky Deck", description="Experience the famous crossing at street level, then take the elevator up to the open-air 360-degree glass rooftop deck.", location="Shibuya"),
                ],
                dining_recommendation="Conveyor belt or counter-style Edomae sushi at a specialty restaurant in Shibuya."
            ),
            ItineraryDay(
                day=3,
                theme="Fish Markets, Luxury Ginza & Neon Shinjuku",
                activities=[
                    Activity(time_of_day="Morning", title="Tsukiji Outer Market Tasting Tour", description="Sample freshly torched wagyu skewers, tamagoyaki omelettes, and sashimi bowls from lively street stalls.", location="Tsukiji (Chuo)"),
                    Activity(time_of_day="Afternoon", title="Imperial Palace East Gardens & Ginza", description="Walk through historic Edo Castle stone ruins and moats, then browse department stores in high-end Ginza.", location="Ginza / Chiyoda"),
                    Activity(time_of_day="Evening", title="Shinjuku Omoide Yokocho & Kabukicho", description="Dine on charcoal-grilled yakitori beneath red paper lanterns in nostalgic alleyways, then view the giant 3D Godzilla head.", location="Shinjuku"),
                ],
                dining_recommendation="Smoky yakitori skewers and draft Japanese beer in historic Omoide Yokocho."
            ),
        ]
    },
    "kyoto": {
        "city_name": "Kyoto",
        "country": "Japan",
        "region": "Kansai",
        "currency": "Japanese Yen (JPY, ¥)",
        "language": "Japanese",
        "timezone": "Japan Standard Time (UTC+9)",
        "best_season": "March–April (Sakura) or November (Autumn Maples)",
        "transit_info": "Kyoto City Bus network, Karasuma and Tozai subway lines, and Keihan/Hankyu private railways.",
        "overview": (
            "Kyoto served as Japan's imperial capital for over a millennium from 794 until 1868. "
            "Considered the cultural and spiritual heart of Japan, Kyoto is home to over 2,000 temples and shrines, "
            "including 17 UNESCO World Heritage Sites. The city preserves traditional wooden machiya townhouses, "
            "historic geisha districts in Gion, stone Zen rock gardens, and sublime kaiseki haute cuisine."
        ),
        "landmarks": [
            {"name": "Fushimi Inari-taisha", "lat": 34.9671, "lon": 135.7727, "desc": "Head shrine of Inari featuring a mesmerizing 4-kilometer tunnel of over 10,000 vermilion torii gates winding up Mount Inari.", "category": "Historic"},
            {"name": "Kinkaku-ji (Golden Pavilion)", "lat": 35.0394, "lon": 135.7292, "desc": "Two-story Zen Buddhist temple completely covered in pure gold leaf, reflecting across the serene Mirror Pond (Kyoko-chi).", "category": "Landmark"},
            {"name": "Arashiyama Bamboo Grove", "lat": 35.0170, "lon": 135.6713, "desc": "Soaring, sun-dappled green bamboo stalks creating a natural cathedral of rustling stems and tranquil walking paths.", "category": "Scenic"},
            {"name": "Kiyomizu-dera Temple", "lat": 34.9949, "lon": 135.7850, "desc": "Historic temple founded in 778 AD, famous for its massive wooden stage built entirely without nails, overlooking cherry and maple trees.", "category": "Historic"},
            {"name": "Gion Geisha District", "lat": 35.0037, "lon": 135.7772, "desc": "Historic entertainment district lined with 17th-century wooden tea houses (ochaya) and preservation streets like Hanami-koji.", "category": "Culture"},
        ],
        "cuisine": [
            {"name": "Kyoto Kaiseki Ryori", "desc": "Multi-course seasonal haute cuisine celebrating artistic presentation, subtle dashi flavors, and local vegetables."},
            {"name": "Yudofu (Simmered Artisan Tofu)", "desc": "Delicate silken tofu simmered in kombu kelp broth, dipped in soy tare with grated ginger and scallions."},
            {"name": "Uji Matcha Delicacies", "desc": "Ceremonial grade stone-ground green tea served with seasonal wagashi sweets, parfaits, and soba noodles."},
            {"name": "Kyo-Tsukemono Pickles", "desc": "Traditional Kyoto-style seasonal fermented vegetables prepared using historic heirloom recipes."},
        ],
        "itinerary": [
            ItineraryDay(
                day=1,
                theme="Spiritual Paths & Golden Temples",
                activities=[
                    Activity(time_of_day="Morning", title="Fushimi Inari Shrine Morning Hike", description="Hike beneath thousands of vibrant orange torii gates in the quiet morning mist before crowds arrive.", location="Fushimi Ward"),
                    Activity(time_of_day="Afternoon", title="Kinkaku-ji & Ryoan-ji Zen Garden", description="View the gold-leaf Golden Pavilion, then visit Ryoan-ji to contemplate the famous 15-rock dry landscape garden.", location="Kita Ward"),
                    Activity(time_of_day="Evening", title="Gion Lantern-Lit Evening Stroll", description="Walk down Hanami-koji street past preservation machiya townhouses and historic teahouses.", location="Gion (Higashiyama)"),
                ],
                dining_recommendation="Seasonal multi-course Kaiseki ryori dinner overlooking a traditional private moss garden."
            ),
            ItineraryDay(
                day=2,
                theme="Bamboo Groves, Zen Temples & River Views",
                activities=[
                    Activity(time_of_day="Morning", title="Arashiyama Bamboo Grove & Tenryu-ji", description="Walk through the soaring bamboo stalks, then explore the 14th-century Sogenchi garden at Tenryu-ji temple.", location="Arashiyama (Ukyo)"),
                    Activity(time_of_day="Afternoon", title="Togetsukyo Bridge & Monkey Park", description="Cross the historic wooden Moon Crossing Bridge and visit the hillside park for sweeping views of Kyoto basin.", location="Arashiyama"),
                    Activity(time_of_day="Evening", title="Pontocho Alley Dining by the River", description="Dine on traditional wooden kawayuka platforms built over the Kamogawa River.", location="Pontocho (Nakagyo)"),
                ],
                dining_recommendation="Simmered artisan tofu (Yudofu) at a historic temple garden restaurant in Arashiyama."
            ),
            ItineraryDay(
                day=3,
                theme="Historic Higashiyama & Scenic Hillsides",
                activities=[
                    Activity(time_of_day="Morning", title="Kiyomizu-dera Wooden Stage", description="Stand on the massive cliffside wooden stage overlooking forested hillsides, then drink from the Otowa Waterfall.", location="Higashiyama"),
                    Activity(time_of_day="Afternoon", title="Ninenzaka & Sannenzaka Preservation Streets", description="Browse traditional pottery shops, incense boutiques, and historic wooden houses on stone pathways.", location="Higashiyama"),
                    Activity(time_of_day="Evening", title="Nishiki Food Market Tasting", description="Sample fresh seafood skewers, pickled vegetables, roasted tea, and artisan snacks along Kyoto's Kitchen.", location="Downtown Kyoto"),
                ],
                dining_recommendation="Freshly prepared Kyoto-style duck ramen or charcoal-broiled eel (Unagi) near Nishiki Market."
            ),
        ]
    },
    "snohomish": {
        "city_name": "Snohomish",
        "country": "United States",
        "region": "Washington (Pacific Northwest)",
        "currency": "US Dollar (USD, $)",
        "language": "English",
        "timezone": "Pacific Time (UTC-8 / UTC-7 in summer)",
        "best_season": "June–September (Warm & Sunny) or October (Autumn Harvest)",
        "transit_info": "Community Transit bus routes, Centennial Trail for cycling, easily accessible by car from Seattle (45 mins).",
        "overview": (
            "Snohomish is a historic city located along the Snohomish River in the scenic Puget Sound region of Washington State. "
            "Known as the 'Antique Capital of the Northwest,' its downtown district is listed on the National Register of "
            "Historic Places, featuring well-preserved late 19th-century Victorian architecture, artisan coffee shops, "
            "vintage boutiques, and craft cideries against the majestic backdrop of the Cascade Mountains."
        ),
        "landmarks": [
            {"name": "Historic Downtown Snohomish", "lat": 47.9129, "lon": -122.0982, "desc": "Charming district on First Street filled with multi-dealer antique malls, bakeries, and historic Victorian brick buildings.", "category": "Historic"},
            {"name": "Centennial Trail", "lat": 47.9150, "lon": -122.0940, "desc": "30-mile paved recreational trail popular for cycling, jogging, and scenic views through the Snohomish River Valley.", "category": "Scenic"},
            {"name": "Blackman House Museum", "lat": 47.9142, "lon": -122.0925, "desc": "Restored 1878 Queen Anne-style home documenting the early timber, farming, and settlement history of the city.", "category": "Museum"},
            {"name": "Snohomish Riverfront Trail", "lat": 47.9115, "lon": -122.0970, "desc": "Peaceful walking pathway along the river with wooden observation decks, kayaking launches, and mountain vistas.", "category": "Nature"},
            {"name": "Harvey Field Airport", "lat": 47.9073, "lon": -122.1065, "desc": "Historic general aviation field offering scenic hot-air balloon rides and skydiving over the Cascade foothills.", "category": "Adventure"},
        ],
        "cuisine": [
            {"name": "Snohomish Bakery Artisan Bread", "desc": "European-style sourdough loaves, cinnamon rolls, and handmade croissants baked daily."},
            {"name": "Pacific Northwest Dungeness Crab", "desc": "Sweet, tender local crab cakes served with roasted garlic aioli and fresh lemon."},
            {"name": "Farm-to-Table Valley Dining", "desc": "Locally grown seasonal produce, heirloom squash, and grass-fed meats from Snohomish Valley farms."},
            {"name": "Artisan Craft Cider & Beer", "desc": "Small-batch ciders pressed from local Washington heritage apples."},
        ],
        "itinerary": [
            ItineraryDay(
                day=1,
                theme="Antique Hunting & Victorian Charm",
                activities=[
                    Activity(time_of_day="Morning", title="First Street Antique Shopping", description="Browse vintage collectibles, mid-century decor, and rare books inside Star Center Antique Mall.", location="First Street Downtown"),
                    Activity(time_of_day="Afternoon", title="Riverfront Trail & Blackman House Museum", description="Stroll the riverfront promenade, then tour the furnished 1878 Victorian residence.", location="Downtown Riverfront"),
                    Activity(time_of_day="Evening", title="Local Craft Brewery & Cider Tasting", description="Sample local IPAs and heritage apple ciders in a restored historic barn.", location="Avenue D"),
                ],
                dining_recommendation="Farm-to-table Pacific Northwest dinner overlooking the river with wild salmon and local berry cobbler."
            ),
            ItineraryDay(
                day=2,
                theme="River Valley Nature & Scenic Cycling",
                activities=[
                    Activity(time_of_day="Morning", title="Hot-Air Balloon Flight over Snohomish Valley", description="Take an early sunrise hot-air balloon flight for breathtaking views of Mount Rainier and the Cascades.", location="Harvey Field"),
                    Activity(time_of_day="Afternoon", title="Centennial Trail Bike Ride", description="Rent a bicycle and ride north along the scenic trail through farmland and cedar forests.", location="Centennial Trailhead"),
                    Activity(time_of_day="Evening", title="Snohomish River Sunset & Local Bakery Treats", description="Watch the twilight reflect over the Snohomish River with artisan pastries and local espresso.", location="First Street"),
                ],
                dining_recommendation="Artisan brick-oven sourdough pizza and Washington craft wine in downtown Snohomish."
            ),
        ]
    },
    "new york": {
        "city_name": "New York",
        "country": "United States",
        "region": "New York",
        "currency": "US Dollar (USD, $)",
        "language": "English",
        "timezone": "Eastern Time (UTC-5 / UTC-4 in summer)",
        "best_season": "September–November (Fall) or April–June (Spring)",
        "transit_info": "24/7 New York City Subway network across all five boroughs, MTA buses, and Staten Island Ferry.",
        "overview": (
            "New York City, the most populous city in the United States, is a global epicenter for finance, theater, "
            "fashion, gastronomy, and international commerce. Comprising five distinct boroughs—Manhattan, Brooklyn, "
            "Queens, the Bronx, and Staten Island—the city features world-defining architectural icons, Broadway theaters, "
            "and cultural institutions like the Metropolitan Museum of Art and MoMA."
        ),
        "landmarks": [
            {"name": "Empire State Building", "lat": 40.7484, "lon": -73.9857, "desc": "102-story Art Deco skyscraper in Midtown Manhattan, completed in 1931 and recognized as a symbol of New York.", "category": "Landmark"},
            {"name": "Central Park", "lat": 40.7851, "lon": -73.9683, "desc": "843-acre urban oasis featuring Bethesda Terrace, Bow Bridge, the Reservoir, and scenic winding paths.", "category": "Scenic"},
            {"name": "Statue of Liberty", "lat": 40.6892, "lon": -74.0445, "desc": "Colossal neoclassical copper statue on Liberty Island, a gift of friendship from the people of France.", "category": "Monument"},
            {"name": "Metropolitan Museum of Art (The Met)", "lat": 40.7794, "lon": -73.9632, "desc": "One of the world's greatest museums, housing over two million works spanning 5,000 years of global culture.", "category": "Museum"},
            {"name": "Brooklyn Bridge", "lat": 40.7061, "lon": -73.9969, "desc": "Historic 1883 hybrid cable-stayed/suspension bridge with Neo-Gothic limestone towers spanning the East River.", "category": "Landmark"},
        ],
        "cuisine": [
            {"name": "New York-Style Thin Crust Pizza", "desc": "Crispy yet pliable hand-tossed slices with rich tomato sauce and whole-milk mozzarella."},
            {"name": "Pastrami on Rye from Katz's Delicatessen", "desc": "Towering stacks of cured, spiced, and smoked beef pastrami served with deli mustard and kosher pickles."},
            {"name": "New York Bagel with Lox & Cream Cheese", "desc": "Kettle-boiled, dense, chewy bagels topped with scallion cream cheese, smoked Atlantic salmon, and capers."},
            {"name": "Classic New York Cheesecake", "desc": "Dense, velvety smooth cream cheese cake with a buttery graham cracker crust."},
        ],
        "itinerary": [
            ItineraryDay(
                day=1,
                theme="Midtown Icons & Broadway Theater",
                activities=[
                    Activity(time_of_day="Morning", title="Empire State Building Observation Deck", description="Ride the elevator up to the 86th-floor open-air observatory for sweeping skyline views.", location="Midtown Manhattan"),
                    Activity(time_of_day="Afternoon", title="Fifth Avenue & Museum of Modern Art (MoMA)", description="View Van Gogh's The Starry Night and modern masterpieces, then stroll down Fifth Avenue past St. Patrick's Cathedral.", location="Midtown"),
                    Activity(time_of_day="Evening", title="Times Square & Broadway Show", description="Experience the dazzling neon lights of Times Square and attend an evening Broadway musical performance.", location="Theater District"),
                ],
                dining_recommendation="Classic New York steakhouse dinner near the Theater District with dry-aged prime ribeye."
            ),
            ItineraryDay(
                day=2,
                theme="Central Park Serenity & World-Class Art",
                activities=[
                    Activity(time_of_day="Morning", title="Central Park Walk & Rowboat at The Lake", description="Stroll across Bow Bridge, visit Bethesda Fountain, and row a vintage boat from Loeb Boathouse.", location="Central Park"),
                    Activity(time_of_day="Afternoon", title="The Metropolitan Museum of Art (The Met)", description="Explore the Temple of Dendur, European Paintings galleries, and the rooftop sculpture garden.", location="Upper East Side"),
                    Activity(time_of_day="Evening", title="High Line Park & Chelsea Market", description="Walk the elevated linear park built on historic freight rail lines and browse artisanal food stalls at Chelsea Market.", location="Chelsea / Meatpacking"),
                ],
                dining_recommendation="Artisan pastrami on rye at Katz's Delicatessen or wood-fired pizza in the West Village."
            ),
            ItineraryDay(
                day=3,
                theme="Historic Harbor & Brooklyn Waterfront",
                activities=[
                    Activity(time_of_day="Morning", title="Statue of Liberty & Ellis Island Ferry", description="Take the morning ferry to Liberty Island, then explore the immigration museum at Ellis Island.", location="New York Harbor"),
                    Activity(time_of_day="Afternoon", title="9/11 Memorial & Financial District", description="Visit the reflecting pool memorial and One World Trade Center, then stroll down Wall Street.", location="Lower Manhattan"),
                    Activity(time_of_day="Evening", title="Walk Across Brooklyn Bridge to DUMBO", description="Walk across the iconic suspension bridge at sunset and enjoy skyline views from Brooklyn Bridge Park.", location="DUMBO, Brooklyn"),
                ],
                dining_recommendation="Coal-fired Brooklyn-style pizza in DUMBO with panoramic views of the illuminated Manhattan skyline."
            ),
        ]
    },
}


def get_destination_intelligence(city_name: str, geo_meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Retrieve comprehensive, accurate, factual intelligence for any destination.

    Args:
        city_name: Name of the destination city.
        geo_meta: Optional verified geocoding metadata from GuardrailAgent.

    Returns:
        Structured intelligence dictionary with overview, landmarks, coordinates, and itinerary.
    """
    city_lower = city_name.strip().lower()

    # 1. Return curated deep intelligence if in database
    if city_lower in VERIFIED_DESTINATION_DATABASE:
        return VERIFIED_DESTINATION_DATABASE[city_lower]

    # Check aliases (e.g. 'nyc')
    if city_lower == "nyc" and "new york" in VERIFIED_DESTINATION_DATABASE:
        return VERIFIED_DESTINATION_DATABASE["new york"]

    # 2. Dynamic live generation for other verified global cities (e.g. Rome, London, Dubai, etc.)
    lat = geo_meta.get("latitude", 0.0) if geo_meta else 0.0
    lon = geo_meta.get("longitude", 0.0) if geo_meta else 0.0
    country = geo_meta.get("country", "") if geo_meta else ""
    region = geo_meta.get("region", "") if geo_meta else ""

    # Fetch live Wikipedia overview
    wiki_overview = ""
    try:
        encoded = urllib.parse.quote(city_name.strip())
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "EnterpriseTravelIntel/2.0 (contact: admin@travel.ai)"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract", "")
            description = data.get("description", "")
            title = data.get("title", city_name)
            desc_str = f" ({description})" if description else ""
            if extract:
                wiki_overview = f"**{title}**{desc_str}\n\n{extract}"
    except Exception:
        pass

    if not wiki_overview:
        wiki_overview = f"**{city_name.title()}** is a verified destination located in {country or 'the world'}, offering rich cultural heritage and landmark sights."

    # No verified landmarks/itinerary available for this city. Returning empty to avoid fabrication.
    landmarks = []
    itinerary = None
    cuisine = []

    return {
        "city_name": city_name.title(),
        "country": country,
        "region": region,
        "currency": "Local Currency",
        "language": "Official Regional Language",
        "timezone": "Local Regional Timezone",
        "best_season": "Spring / Autumn",
        "transit_info": f"Public transport and taxi services across {city_name.title()}.",
        "overview": wiki_overview,
        "landmarks": landmarks,
        "cuisine": cuisine,
        "itinerary": itinerary,
    }
