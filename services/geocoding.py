"""
Geocoding Service using OpenStreetMap Nominatim API
Converts addresses to GPS coordinates and vice versa
"""

import requests
import time
from typing import Optional, Dict, List
from functools import lru_cache
from models.domain import Coordinate


class GeocodingService:
    """OpenStreetMap Nominatim geocoding service with caching and optimization"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {
            "User-Agent": "DeadheadingOptimization/1.0",
            "Accept-Language": "en"  # Get English results
        }
        self.rate_limit_delay = 0.5  # Reduced delay with caching
        self.last_request_time = 0
        self._cache = {}  # Simple in-memory cache
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def geocode(self, address: str, country: str = "India") -> Optional[Coordinate]:
        """
        Convert address to GPS coordinates
        
        Args:
            address: Address string (e.g., "Azadpur Mandi, Delhi")
            country: Country name for better results
            
        Returns:
            Coordinate object with lat, lng, and formatted address
        """
        self._rate_limit()
        
        try:
            # Try with country first
            params = {
                "q": f"{address}, {country}",
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                
                if results and len(results) > 0:
                    result = results[0]
                    return Coordinate(
                        lat=float(result['lat']),
                        lng=float(result['lon']),
                        address=result.get('display_name', address)
                    )
            
            # If first attempt failed, try without country
            print(f"⚠️  First geocoding attempt failed, retrying without country...")
            self._rate_limit()
            
            params = {
                "q": address,
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                
                if results and len(results) > 0:
                    result = results[0]
                    print(f"✓ Geocoding succeeded on retry: {result.get('display_name', address)}")
                    return Coordinate(
                        lat=float(result['lat']),
                        lng=float(result['lon']),
                        address=result.get('display_name', address)
                    )
            
            print(f"⚠️  Geocoding failed for: {address}")
            print(f"    Response status: {response.status_code}")
            print(f"    Response: {response.text[:200]}")
            return None
            
        except Exception as e:
            print(f"❌ Geocoding error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        """
        Convert GPS coordinates to address
        
        Args:
            lat: Latitude
            lng: Longitude
            
        Returns:
            Formatted address string
        """
        self._rate_limit()
        
        try:
            params = {
                "lat": lat,
                "lon": lng,
                "format": "json",
                "addressdetails": 1
            }
            
            response = requests.get(
                f"{self.base_url}/reverse",
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('display_name', f"{lat}, {lng}")
            
            return f"{lat}, {lng}"
            
        except Exception as e:
            print(f"❌ Reverse geocoding error: {e}")
            return f"{lat}, {lng}"
    
    def search_places(self, query: str, country: str = "India", limit: int = 10) -> List[Dict]:
        """
        Search for places matching query with enhanced accuracy
        
        Args:
            query: Search query (e.g., "market yard mumbai" or "MG Road, Bangalore")
            country: Country name
            limit: Maximum number of results
            
        Returns:
            List of dictionaries with location details
        """
        # Check cache first
        cache_key = f"{query}_{country}_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        self._rate_limit()
        
        try:
            # Enhanced search with structured query
            params = {
                "q": f"{query}, {country}",
                "format": "json",
                "limit": limit,
                "addressdetails": 1,
                "dedupe": 1,  # Remove duplicate results
                "extratags": 1,  # Get additional tags
                "namedetails": 1  # Get name variations
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                
                formatted_results = []
                for r in results:
                    # Extract detailed address components
                    address_parts = r.get('address', {})
                    
                    # Build a more readable address
                    display_parts = []
                    
                    # Add specific location details first
                    for key in ['building', 'house_number', 'road', 'neighbourhood', 
                               'suburb', 'village', 'town', 'city', 'state', 'country']:
                        if key in address_parts and address_parts[key]:
                            display_parts.append(address_parts[key])
                    
                    # Use display_name as fallback
                    readable_address = ', '.join(display_parts) if display_parts else r.get('display_name', query)
                    
                    formatted_results.append({
                        'lat': float(r['lat']),
                        'lng': float(r['lon']),
                        'address': readable_address,
                        'display_name': r.get('display_name', ''),
                        'type': r.get('type', ''),
                        'importance': r.get('importance', 0),
                        'address_components': address_parts
                    })
                
                # Sort by importance (relevance)
                formatted_results.sort(key=lambda x: x['importance'], reverse=True)
                
                # Cache results
                self._cache[cache_key] = formatted_results
                
                return formatted_results
            
            return []
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def autocomplete(self, query: str, country: str = "India", limit: int = 8) -> List[Dict]:
        """
        Fast autocomplete for address input with street-level precision
        
        Args:
            query: Partial address query
            country: Country name
            limit: Maximum number of suggestions
            
        Returns:
            List of autocomplete suggestions
        """
        if len(query) < 3:
            return []
        
        # Use search_places with optimized parameters
        return self.search_places(query, country, limit)
    
    def geocode_structured(self, street: str = None, city: str = None, 
                          state: str = None, country: str = "India") -> Optional[Coordinate]:
        """
        Geocode using structured address components for better accuracy
        
        Args:
            street: Street name with number
            city: City name
            state: State name
            country: Country name
            
        Returns:
            Coordinate object or None
        """
        self._rate_limit()
        
        try:
            params = {
                "format": "json",
                "addressdetails": 1,
                "limit": 1
            }
            
            # Add structured components
            if street:
                params['street'] = street
            if city:
                params['city'] = city
            if state:
                params['state'] = state
            if country:
                params['country'] = country
            
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                
                if results and len(results) > 0:
                    result = results[0]
                    return Coordinate(
                        lat=float(result['lat']),
                        lng=float(result['lon']),
                        address=result.get('display_name', f"{street}, {city}")
                    )
            
            return None
            
        except Exception as e:
            print(f"❌ Structured geocoding error: {e}")
            return None
    
    def get_route_points(self, start: Coordinate, end: Coordinate, num_points: int = 5) -> List[Coordinate]:
        """
        Get intermediate points along a route
        Note: This is a simple linear interpolation. For real routing, use OSRM or GraphHopper.
        
        Args:
            start: Starting coordinate
            end: Ending coordinate
            num_points: Number of intermediate points
            
        Returns:
            List of coordinates along the route
        """
        points = []
        
        for i in range(num_points + 1):
            ratio = i / num_points
            lat = start.lat + (end.lat - start.lat) * ratio
            lng = start.lng + (end.lng - start.lng) * ratio
            
            points.append(Coordinate(
                lat=lat,
                lng=lng,
                address=f"Point {i+1}"
            ))
        
        return points
    
    def calculate_distance_osrm(self, start: Coordinate, end: Coordinate) -> Optional[float]:
        """
        Calculate actual road distance using OSRM (Open Source Routing Machine)
        
        Args:
            start: Starting coordinate
            end: Ending coordinate
            
        Returns:
            Distance in kilometers, or None if failed
        """
        try:
            # Using public OSRM server
            url = f"http://router.project-osrm.org/route/v1/driving/{start.lng},{start.lat};{end.lng},{end.lat}"
            params = {
                "overview": "false",
                "steps": "false"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['code'] == 'Ok' and data['routes']:
                    # Distance is in meters, convert to km
                    distance_km = data['routes'][0]['distance'] / 1000
                    return round(distance_km, 2)
            
            return None
            
        except Exception as e:
            print(f"⚠️  OSRM routing failed: {e}")
            return None


# Global instance
geocoding_service = GeocodingService()
