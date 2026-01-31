"""
Real-world data generator
Generates realistic vendor locations, market yards, and load data
Based on actual Indian cities and logistics hubs
"""

from typing import List, Dict
from models.domain import Coordinate
import random


class RealWorldDataGenerator:
    """Generate realistic logistics data based on real locations"""
    
    def __init__(self):
        # Real market yards and logistics hubs in India
        self.market_yards = {
            "Delhi": [
                {"name": "Azadpur Mandi", "lat": 28.7041, "lng": 77.1734},
                {"name": "Ghazipur Mandi", "lat": 28.6517, "lng": 77.3167},
                {"name": "Okhla Mandi", "lat": 28.5355, "lng": 77.2750},
                {"name": "Narela Mandi", "lat": 28.8534, "lng": 77.0934},
            ],
            "Mumbai": [
                {"name": "Vashi APMC", "lat": 19.0728, "lng": 73.0050},
                {"name": "Turbhe APMC", "lat": 19.0728, "lng": 73.0167},
                {"name": "Kalamboli Market", "lat": 19.0333, "lng": 73.1167},
            ],
            "Bangalore": [
                {"name": "Yeshwanthpur Market", "lat": 13.0280, "lng": 77.5376},
                {"name": "KR Market", "lat": 12.9634, "lng": 77.5855},
            ],
            "Pune": [
                {"name": "Market Yard", "lat": 18.4977, "lng": 73.8536},
                {"name": "Gultekdi Market", "lat": 18.5018, "lng": 73.8636},
            ]
        }
        
        # Common cargo types and typical weights
        self.cargo_types = [
            {"type": "Electronics", "weight_range": (1000, 5000), "price_per_kg": 2.5},
            {"type": "Textiles", "weight_range": (2000, 8000), "price_per_kg": 1.5},
            {"type": "Food Grains", "weight_range": (5000, 15000), "price_per_kg": 0.8},
            {"type": "Vegetables", "weight_range": (3000, 10000), "price_per_kg": 1.2},
            {"type": "Furniture", "weight_range": (2000, 7000), "price_per_kg": 2.0},
            {"type": "Construction Materials", "weight_range": (8000, 20000), "price_per_kg": 0.5},
            {"type": "Pharmaceuticals", "weight_range": (500, 3000), "price_per_kg": 5.0},
            {"type": "Auto Parts", "weight_range": (1000, 6000), "price_per_kg": 3.0},
        ]
        
        # Major Indian cities with coordinates
        self.cities = {
            "Delhi": {"lat": 28.6139, "lng": 77.2090},
            "Mumbai": {"lat": 19.0760, "lng": 72.8777},
            "Bangalore": {"lat": 12.9716, "lng": 77.5946},
            "Chennai": {"lat": 13.0827, "lng": 80.2707},
            "Kolkata": {"lat": 22.5726, "lng": 88.3639},
            "Hyderabad": {"lat": 17.3850, "lng": 78.4867},
            "Pune": {"lat": 18.5204, "lng": 73.8567},
            "Ahmedabad": {"lat": 23.0225, "lng": 72.5714},
            "Jaipur": {"lat": 26.9124, "lng": 75.7873},
            "Lucknow": {"lat": 26.8467, "lng": 80.9462},
        }
    
    def get_random_market_yard(self, city: str = None) -> Dict:
        """Get a random market yard location"""
        if city and city in self.market_yards:
            yards = self.market_yards[city]
        else:
            # Random city
            city = random.choice(list(self.market_yards.keys()))
            yards = self.market_yards[city]
        
        yard = random.choice(yards)
        return {
            "name": yard["name"],
            "city": city,
            "coordinate": Coordinate(
                lat=yard["lat"],
                lng=yard["lng"],
                address=f"{yard['name']}, {city}"
            )
        }
    
    def generate_realistic_load(self) -> Dict:
        """Generate a realistic load with cargo type, weight, and pricing"""
        cargo = random.choice(self.cargo_types)
        weight_kg = random.randint(cargo["weight_range"][0], cargo["weight_range"][1])
        
        # Calculate price based on weight and type
        base_price = weight_kg * cargo["price_per_kg"]
        
        # Add distance factor (longer distance = higher price)
        distance_factor = random.uniform(1.0, 2.0)
        price_offered = base_price * distance_factor
        
        # Get pickup and delivery locations
        pickup_yard = self.get_random_market_yard()
        
        # Delivery to a different city
        delivery_city = random.choice([c for c in self.cities.keys() if c != pickup_yard["city"]])
        delivery_coords = self.cities[delivery_city]
        
        return {
            "cargo_type": cargo["type"],
            "weight_kg": weight_kg,
            "pickup_location": pickup_yard["coordinate"],
            "pickup_name": pickup_yard["name"],
            "destination": Coordinate(
                lat=delivery_coords["lat"],
                lng=delivery_coords["lng"],
                address=delivery_city
            ),
            "price_offered": round(price_offered, 2),
            "currency": "INR"
        }
    
    def generate_multiple_loads(self, count: int = 10) -> List[Dict]:
        """Generate multiple realistic loads"""
        return [self.generate_realistic_load() for _ in range(count)]
    
    def get_city_coordinate(self, city_name: str) -> Coordinate:
        """Get coordinates for a major city"""
        if city_name in self.cities:
            coords = self.cities[city_name]
            return Coordinate(
                lat=coords["lat"],
                lng=coords["lng"],
                address=city_name
            )
        return None
    
    def get_route_between_cities(self, city1: str, city2: str) -> Dict:
        """Get a realistic route between two cities"""
        if city1 in self.cities and city2 in self.cities:
            return {
                "origin": self.get_city_coordinate(city1),
                "destination": self.get_city_coordinate(city2),
                "route_name": f"{city1} to {city2}"
            }
        return None


# Global instance
real_world_data = RealWorldDataGenerator()
