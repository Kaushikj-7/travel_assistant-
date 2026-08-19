"""
Pre-populated city knowledge base.

Detailed factual text chunks for Paris, Tokyo, and New York.
Each city has multiple thematic chunks to enable granular
semantic retrieval from the vector store.
"""

CITY_KNOWLEDGE = {
    "paris": [
        {
            "id": "paris_overview",
            "text": (
                "Paris, France — Paris is the capital and most populous city of France, with a population of "
                "approximately 2.1 million in the city proper and over 12 million in the metropolitan area. "
                "Known as the 'City of Light' (La Ville Lumière), Paris has been a global centre for art, "
                "fashion, gastronomy, and culture since the 17th century. The city is built along the Seine "
                "River and is divided into 20 arrondissements (districts) arranged in a clockwise spiral."
            ),
        },
        {
            "id": "paris_landmarks",
            "text": (
                "Major landmarks in Paris include the Eiffel Tower (completed 1889, 330 m tall), the Louvre "
                "Museum (world's most-visited museum, home to the Mona Lisa), Notre-Dame Cathedral (Gothic "
                "masterpiece, currently under restoration after the 2019 fire), the Arc de Triomphe at the "
                "western end of the Champs-Élysées, Sacré-Cœur Basilica atop Montmartre hill, and the "
                "Musée d'Orsay housed in a former railway station."
            ),
        },
        {
            "id": "paris_cuisine",
            "text": (
                "Parisian cuisine is renowned worldwide. Classic dishes include croissants, coq au vin, "
                "croque monsieur, escargot, duck confit, and French onion soup. The city has the highest "
                "concentration of Michelin-starred restaurants in the world. The café culture is legendary — "
                "establishments like Café de Flore and Les Deux Magots were meeting places for existentialist "
                "philosophers. French patisserie art reaches its pinnacle in Paris with macarons, éclairs, "
                "mille-feuille, and tarte Tatin."
            ),
        },
        {
            "id": "paris_culture",
            "text": (
                "Paris is a world capital of art, fashion, and intellectual life. The Louvre, Musée d'Orsay, "
                "Centre Pompidou, and Palais de Tokyo house extraordinary collections spanning millennia. "
                "The city hosts Paris Fashion Week twice a year, anchoring the global luxury fashion industry. "
                "Literary history runs deep: Hemingway, Fitzgerald, Stein, and Wilde all lived and wrote here. "
                "The city is also home to UNESCO's headquarters."
            ),
        },
        {
            "id": "paris_transport",
            "text": (
                "Paris has an extensive public transport network. The Paris Métro has 16 lines and over 300 "
                "stations, making it one of the densest metro systems in the world. The RER suburban rail "
                "connects the city centre to outlying areas including both airports (Charles de Gaulle and "
                "Orly). A public bike-sharing system (Vélib') offers thousands of bicycles across the city. "
                "The TGV high-speed rail connects Paris to other European cities."
            ),
        },
        {
            "id": "paris_practical",
            "text": (
                "Best time to visit Paris: April–June and September–October for mild weather and fewer crowds. "
                "Currency: Euro (EUR). Language: French, though English is widely spoken in tourist areas. "
                "Time zone: CET (UTC+1) / CEST (UTC+2) in summer. Paris has a temperate oceanic climate "
                "with warm summers (avg 25°C) and cool winters (avg 5°C). Tipping is not mandatory as "
                "service is included, but rounding up is appreciated."
            ),
        },
    ],
    "tokyo": [
        {
            "id": "tokyo_overview",
            "text": (
                "Tokyo, Japan — Tokyo is the capital of Japan and the most populous metropolitan area in the "
                "world, with approximately 14 million people in the city proper and 37 million in the greater "
                "metropolitan area. Originally a small fishing village named Edo, it became the political "
                "centre of Japan when Tokugawa Ieyasu established his shogunate here in 1603. It was officially "
                "renamed Tokyo ('Eastern Capital') in 1868 when it became the imperial capital."
            ),
        },
        {
            "id": "tokyo_landmarks",
            "text": (
                "Key landmarks in Tokyo include the Meiji Shrine (a Shinto shrine dedicated to Emperor Meiji), "
                "Senso-ji (Tokyo's oldest temple in Asakusa), the Imperial Palace surrounded by moats and "
                "gardens, Tokyo Skytree (634 m, tallest tower in the world), Shibuya Crossing (the world's "
                "busiest pedestrian intersection), and Tsukiji Outer Market for fresh seafood and street food."
            ),
        },
        {
            "id": "tokyo_cuisine",
            "text": (
                "Tokyo has the most Michelin-starred restaurants of any city in the world. The cuisine ranges "
                "from exquisite sushi at Tsukiji and Toyosu markets to rich tonkotsu ramen in neighbourhood "
                "shops. Tempura, yakitori, okonomiyaki, and wagyu beef are staples. The city is also famous "
                "for its depachika (department store basement food halls) and konbini (convenience store) "
                "culture, where onigiri and bento boxes are elevated to an art form."
            ),
        },
        {
            "id": "tokyo_culture",
            "text": (
                "Tokyo uniquely blends ultra-modern technology with deep traditional culture. Akihabara is the "
                "global epicentre of anime, manga, and electronics culture. Harajuku's Takeshita Street "
                "showcases avant-garde youth fashion. Meanwhile, traditional arts like tea ceremony, calligraphy, "
                "and sumo wrestling thrive. The Ghibli Museum in Mitaka celebrates Studio Ghibli's animation. "
                "Tokyo's pop culture exports — from J-Pop to video games — have shaped global entertainment."
            ),
        },
        {
            "id": "tokyo_transport",
            "text": (
                "Tokyo's public transport is famously efficient and punctual. The Tokyo Metro and Toei Subway "
                "systems, combined with JR lines (including the Yamanote loop line), form a comprehensive "
                "network. The Shinkansen (bullet train) connects Tokyo to Osaka in 2.5 hours at speeds up "
                "to 320 km/h. Narita and Haneda airports serve international and domestic flights. Suica and "
                "Pasmo IC cards make payment seamless across all transport modes."
            ),
        },
        {
            "id": "tokyo_practical",
            "text": (
                "Best time to visit Tokyo: March–May (cherry blossom season) and October–November (autumn "
                "foliage). Currency: Japanese Yen (JPY). Language: Japanese, with limited English outside "
                "tourist areas. Time zone: JST (UTC+9). Tokyo has a humid subtropical climate with hot, "
                "humid summers (avg 30°C) and mild winters (avg 6°C). The rainy season (tsuyu) runs from "
                "early June to mid-July. Japan Rail Pass is recommended for visitors planning bullet train travel."
            ),
        },
    ],
    "new york": [
        {
            "id": "newyork_overview",
            "text": (
                "New York City, USA — New York City (NYC) is the most populous city in the United States, with "
                "approximately 8.3 million residents across five boroughs: Manhattan, Brooklyn, Queens, the Bronx, "
                "and Staten Island. Often called 'The Big Apple' or 'The City That Never Sleeps,' NYC is a "
                "global powerhouse in finance (Wall Street), media, art, fashion, technology, and entertainment. "
                "The city was founded as New Amsterdam by Dutch colonists in 1626."
            ),
        },
        {
            "id": "newyork_landmarks",
            "text": (
                "Iconic NYC landmarks include the Statue of Liberty (a gift from France in 1886), the Empire "
                "State Building (443 m), Central Park (843 acres of green space in Manhattan), Times Square, "
                "the Brooklyn Bridge (opened 1883), One World Trade Center (541 m, tallest building in the "
                "Western Hemisphere), and the High Line — an elevated linear park built on a former rail line. "
                "The Metropolitan Museum of Art is one of the largest art museums in the world."
            ),
        },
        {
            "id": "newyork_cuisine",
            "text": (
                "NYC's food scene reflects its incredible diversity. The city is famous for New York-style "
                "pizza (thin crust, foldable slices), bagels, cheesecake, and hot dogs from street vendors. "
                "Chinatown and Little Italy offer authentic ethnic cuisines, while the five boroughs harbour "
                "food from virtually every country on Earth. Fine dining thrives in Manhattan with restaurants "
                "like Le Bernardin and Eleven Madison Park. The food truck and street food culture is legendary."
            ),
        },
        {
            "id": "newyork_culture",
            "text": (
                "NYC is a global arts and culture capital. Broadway in the Theatre District hosts world-renowned "
                "musicals and plays. The Metropolitan Museum, MoMA, the Guggenheim, and the Whitney Museum "
                "house extraordinary art collections. Music history runs deep — from Carnegie Hall to the "
                "birthplace of hip-hop in the Bronx and the jazz clubs of Harlem and Greenwich Village. "
                "The city's literary tradition includes the New York Public Library and countless independent "
                "bookshops."
            ),
        },
        {
            "id": "newyork_transport",
            "text": (
                "The NYC Subway is one of the world's oldest and most extensive rapid transit systems, operating "
                "24/7 with 472 stations. Yellow taxis and ride-sharing services cover the five boroughs. "
                "Three major airports serve the metro area: JFK, LaGuardia, and Newark Liberty. The Staten "
                "Island Ferry provides free service across New York Harbor with views of the Statue of Liberty. "
                "Citi Bike bike-sharing offers thousands of docking stations across Manhattan and Brooklyn."
            ),
        },
        {
            "id": "newyork_practical",
            "text": (
                "Best time to visit NYC: April–June and September–November for pleasant weather. Currency: "
                "US Dollar (USD). Language: English, with hundreds of other languages spoken. Time zone: "
                "EST (UTC-5) / EDT (UTC-4) in summer. NYC has a humid subtropical climate with hot summers "
                "(avg 30°C) and cold winters (avg 0°C, with snowfall). Standard tipping is 18-20%% for "
                "restaurant service. The city's grid plan in Manhattan makes navigation straightforward."
            ),
        },
    ],
}

# Flat list of all supported city names for quick lookup
SUPPORTED_CITIES = list(CITY_KNOWLEDGE.keys())
