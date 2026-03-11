"""
Management command to seed the database with sample data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from listings.models import City, Agent, Property, PropertyEnlistRequest


CITIES = [
    ("Bengaluru", "Karnataka"),
    ("Mumbai",    "Maharashtra"),
    ("Hyderabad", "Telangana"),
    ("Pune",      "Maharashtra"),
    ("Chennai",   "Tamil Nadu"),
    ("Delhi",     "Delhi"),
    ("Gurugram",  "Haryana"),
    ("Kolkata",   "West Bengal"),
]

AGENTS = [
    {"name": "Priya Mehta",    "phone": "+91 98765 11001", "email": "priya@housesquare.in",  "bio": "10+ years in Bengaluru luxury residential market.", "verified": True, "listings_count": 28},
    {"name": "Arun Sharma",    "phone": "+91 98765 11002", "email": "arun@housesquare.in",   "bio": "Mumbai's top commercial property specialist.",     "verified": True, "listings_count": 42},
    {"name": "Divya Reddy",    "phone": "+91 98765 11003", "email": "divya@housesquare.in",  "bio": "Hyderabad plots and villa expert since 2014.",      "verified": True, "listings_count": 19},
    {"name": "Rahul Kapoor",   "phone": "+91 98765 11004", "email": "rahul@housesquare.in",  "bio": "Pune residential and commercial property advisor.",  "verified": False, "listings_count": 7},
]

PROPERTIES = [
    {
        "title": "Spacious 3 BHK with Rooftop Garden",
        "description": "A stunning 3-bedroom apartment with a private rooftop garden offering panoramic city views. Features modular kitchen, imported marble flooring, and two covered parking spots. Located in the heart of Indiranagar with easy access to metro and prime restaurants.",
        "property_type": "apartment",
        "purpose": "sale",
        "address": "12, 100 Feet Road, Indiranagar",
        "locality": "Indiranagar",
        "city_name": "Bengaluru",
        "price": 18500000,
        "bedrooms": 3, "bathrooms": 2, "balconies": 2, "parking_spots": 2,
        "built_up_area": 1840, "carpet_area": 1620,
        "furnishing": "fully_furnished",
        "floor_number": 8, "total_floors": 12,
        "has_gym": True, "has_security": True, "has_lift": True, "has_power_backup": True,
        "is_featured": True, "is_verified": True,
        "agent_index": 0,
    },
    {
        "title": "Modern Villa with Private Pool",
        "description": "An architectural masterpiece set across 3,200 sqft of living space. This 5-bedroom villa comes with a private temperature-controlled swimming pool, landscaped garden, home theatre, and a dedicated staff quarter. Premium Italian marble, automated lighting, and smart home integration.",
        "property_type": "villa",
        "purpose": "sale",
        "address": "Plot 7, Road No. 10, Jubilee Hills",
        "locality": "Jubilee Hills",
        "city_name": "Hyderabad",
        "price": 42000000,
        "bedrooms": 5, "bathrooms": 4, "balconies": 3, "parking_spots": 3,
        "built_up_area": 3200,
        "furnishing": "fully_furnished",
        "has_gym": True, "has_pool": True, "has_security": True, "has_garden": True,
        "has_lift": True, "has_clubhouse": True, "has_power_backup": True,
        "is_featured": True, "is_verified": True,
        "agent_index": 2,
    },
    {
        "title": "Sea-Facing Penthouse with Sky Lounge",
        "description": "Rare sea-facing penthouse offering 270° views of the Arabian Sea from the private sky lounge. 4 bedrooms, designer bathrooms with Italian fixtures, a chef's kitchen, and direct terrace access. Building amenities include concierge service, valet parking, and rooftop infinity pool.",
        "property_type": "penthouse",
        "purpose": "sale",
        "address": "The Grand, Carter Road, Bandra West",
        "locality": "Bandra West",
        "city_name": "Mumbai",
        "price": 75000000,
        "bedrooms": 4, "bathrooms": 3, "balconies": 2, "parking_spots": 2,
        "built_up_area": 2600,
        "furnishing": "fully_furnished",
        "floor_number": 32, "total_floors": 32,
        "has_gym": True, "has_pool": True, "has_security": True, "has_lift": True,
        "has_clubhouse": True, "has_power_backup": True, "pet_friendly": True,
        "is_featured": True, "is_verified": True,
        "agent_index": 1,
    },
    {
        "title": "Ready-to-Move 2 BHK Near Metro",
        "description": "Bright and airy 2-bedroom apartment in a gated community just 5 minutes from Koramangala metro. Semi-furnished with premium wardrobes, split ACs in all rooms, and modular kitchen. Society amenities include 24/7 security, gym, and children's play area.",
        "property_type": "apartment",
        "purpose": "sale",
        "address": "Prestige Gardens, 5th Block, Koramangala",
        "locality": "Koramangala",
        "city_name": "Bengaluru",
        "price": 9500000,
        "bedrooms": 2, "bathrooms": 2, "balconies": 1, "parking_spots": 1,
        "built_up_area": 1180, "carpet_area": 980,
        "furnishing": "semi_furnished",
        "floor_number": 3, "total_floors": 8,
        "has_gym": True, "has_security": True, "has_lift": True,
        "is_featured": False, "is_verified": True,
        "agent_index": 0,
    },
    {
        "title": "Premium Commercial Office Space",
        "description": "Grade A office space in the heart of Cyber City, ideal for IT & tech companies. Features raised floor, high-speed fibre, modular workstations for 50 seats, 2 conference rooms, a pantry area, and dedicated parking. LEED-certified green building.",
        "property_type": "office",
        "purpose": "lease",
        "address": "DLF Cyber Hub, Tower B, Sector 24",
        "locality": "Cyber City",
        "city_name": "Gurugram",
        "price": 21000000,
        "built_up_area": 3500,
        "parking_spots": 5,
        "furnishing": "fully_furnished",
        "has_security": True, "has_lift": True, "has_power_backup": True,
        "is_featured": True, "is_verified": True,
        "agent_index": 1,
    },
    {
        "title": "Residential Plot in Premium Layout",
        "description": "East-facing BDA-approved residential plot in a premium gated layout on Sarjapur Road. Fully developed with wide roads, underground cabling, parks, and clubhouse. BBMP-approved, clear title, RERA registered. Ideal for building your custom dream home.",
        "property_type": "plot",
        "purpose": "sale",
        "address": "Sunshine Enclave, Sarjapur Road",
        "locality": "Sarjapur Road",
        "city_name": "Bengaluru",
        "price": 12000000,
        "built_up_area": 2400,
        "plot_area": 2400,
        "is_featured": False, "is_verified": True,
        "facing": "east",
    },
    {
        "title": "Luxury 4 BHK Row House with Garden",
        "description": "Elegant row house in a premium township offering a private garden, home theatre, and designer interiors. 4 large bedrooms with attached baths, an open-plan kitchen, and a double-height living room. Located within a gated community with 24/7 security and clubhouse.",
        "property_type": "villa",
        "purpose": "sale",
        "address": "Greenfields Township, Viman Nagar",
        "locality": "Viman Nagar",
        "city_name": "Pune",
        "price": 29000000,
        "bedrooms": 4, "bathrooms": 4, "balconies": 2, "parking_spots": 2,
        "built_up_area": 2800,
        "furnishing": "semi_furnished",
        "has_gym": True, "has_pool": True, "has_security": True, "has_garden": True,
        "has_clubhouse": True, "has_power_backup": True,
        "is_featured": True, "is_verified": True,
        "agent_index": 3,
    },
    {
        "title": "Cozy Studio Apartment for Rent",
        "description": "A well-designed studio apartment perfect for working professionals. Fully furnished with a queen bed, work desk, smart TV, and a mini-kitchen. 24/7 security, high-speed WiFi included. Located 5 minutes from HSR Layout bus stand and multiple co-working spaces.",
        "property_type": "apartment",
        "purpose": "rent",
        "address": "Oaktree Residences, Sector 2, HSR Layout",
        "locality": "HSR Layout",
        "city_name": "Bengaluru",
        "price": 25000,
        "bedrooms": 1, "bathrooms": 1,
        "built_up_area": 480,
        "furnishing": "fully_furnished",
        "floor_number": 2, "total_floors": 5,
        "has_security": True, "has_lift": True, "pet_friendly": True,
        "is_featured": False, "is_verified": True,
        "agent_index": 0,
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with sample HouseSquare data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🏗️  Seeding HouseSquare database...\n')

        # Cities
        city_map = {}
        for name, state in CITIES:
            city, created = City.objects.get_or_create(name=name, defaults={"state": state})
            city_map[name] = city
            if created:
                self.stdout.write(f'  ✅ City: {name}')

        # Agents
        agent_list = []
        for a in AGENTS:
            agent, created = Agent.objects.get_or_create(
                email=a["email"],
                defaults={k: v for k, v in a.items() if k != "email"}
            )
            agent_list.append(agent)
            if created:
                self.stdout.write(f'  ✅ Agent: {agent.name}')

        # Properties
        for p in PROPERTIES:
            if Property.objects.filter(title=p["title"]).exists():
                self.stdout.write(f'  ⏭  Skip: {p["title"][:50]}')
                continue

            city = city_map.get(p.pop("city_name", None))
            agent_idx = p.pop("agent_index", None)
            agent = agent_list[agent_idx] if agent_idx is not None and agent_idx < len(agent_list) else None

            prop = Property.objects.create(
                city=city,
                agent=agent,
                **p
            )
            self.stdout.write(f'  ✅ Property: {prop.title[:60]}')

        # Sample enlist request
        if not PropertyEnlistRequest.objects.exists():
            PropertyEnlistRequest.objects.create(
                owner_name="Sanjay Patel",
                owner_phone="+91 99887 66554",
                owner_email="sanjay.patel@gmail.com",
                property_type="apartment",
                purpose="sale",
                city="Chennai",
                locality="Anna Nagar",
                price=8500000,
                built_up_area=1200,
                bedrooms=3,
                description="Well maintained 3 BHK in prime Anna Nagar location. 10 years old building, recently renovated. Close to schools and hospitals.",
            )
            self.stdout.write('  ✅ Enlist Request: Sanjay Patel')

        self.stdout.write(self.style.SUCCESS('\n🎉  Database seeded successfully! Run: python manage.py runserver'))
