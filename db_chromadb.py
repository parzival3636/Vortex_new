"""
ChromaDB Database - Embedded, no setup required!
Stores all data locally in ./chroma_data directory
"""

import chromadb
from chromadb.config import Settings
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import json


class ChromaDatabase:
    """Embedded ChromaDB for storing all application data"""
    
    def __init__(self, persist_directory="./chroma_data"):
        """Initialize ChromaDB client"""
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create collections for each entity type
        self.owners = self._get_or_create_collection("owners")
        self.drivers = self._get_or_create_collection("drivers")
        self.vendors = self._get_or_create_collection("vendors")
        self.trucks = self._get_or_create_collection("trucks")
        self.trips = self._get_or_create_collection("trips")
        self.loads = self._get_or_create_collection("loads")
        self.load_assignments = self._get_or_create_collection("load_assignments")
        
    def _get_or_create_collection(self, name: str):
        """Get or create a collection"""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(name)
    
    # ==================== OWNERS ====================
    
    def create_owner(self, name: str, email: str) -> Dict:
        """Create a new owner"""
        owner_id = str(uuid.uuid4())
        owner = {
            "owner_id": owner_id,
            "name": name,
            "email": email,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.owners.add(
            ids=[owner_id],
            documents=[name],  # For search
            metadatas=[owner]
        )
        return owner
    
    def get_owner(self, owner_id: str) -> Optional[Dict]:
        """Get owner by ID"""
        try:
            result = self.owners.get(ids=[owner_id])
            if result['ids']:
                return result['metadatas'][0]
        except:
            pass
        return None
    
    # ==================== DRIVERS ====================
    
    def create_driver(self, name: str, phone: str, truck_id: str, hourly_rate: float = 25.0) -> Dict:
        """Create a new driver"""
        driver_id = str(uuid.uuid4())
        driver = {
            "driver_id": driver_id,
            "name": name,
            "phone": phone,
            "truck_id": truck_id,
            "hourly_rate": hourly_rate,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.drivers.add(
            ids=[driver_id],
            documents=[name],
            metadatas=[driver]
        )
        return driver
    
    def get_driver(self, driver_id: str) -> Optional[Dict]:
        """Get driver by ID"""
        try:
            result = self.drivers.get(ids=[driver_id])
            if result['ids']:
                return result['metadatas'][0]
        except:
            pass
        return None
    
    # ==================== VENDORS ====================
    
    def create_vendor(self, name: str, email: str, phone: str, location_lat: float, location_lng: float) -> Dict:
        """Create a new vendor"""
        vendor_id = str(uuid.uuid4())
        vendor = {
            "vendor_id": vendor_id,
            "name": name,
            "email": email,
            "phone": phone,
            "location_lat": location_lat,
            "location_lng": location_lng,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.vendors.add(
            ids=[vendor_id],
            documents=[name],
            metadatas=[vendor]
        )
        return vendor
    
    def get_vendor(self, vendor_id: str) -> Optional[Dict]:
        """Get vendor by ID"""
        try:
            result = self.vendors.get(ids=[vendor_id])
            if result['ids']:
                return result['metadatas'][0]
        except:
            pass
        return None
    
    # ==================== TRUCKS ====================
    
    def create_truck(self, owner_id: str, license_plate: str, fuel_consumption_rate: float = 0.35) -> Dict:
        """Create a new truck"""
        truck_id = str(uuid.uuid4())
        truck = {
            "truck_id": truck_id,
            "owner_id": owner_id,
            "license_plate": license_plate,
            "fuel_consumption_rate": fuel_consumption_rate,
            "status": "idle",
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.trucks.add(
            ids=[truck_id],
            documents=[license_plate],
            metadatas=[truck]
        )
        return truck
    
    def get_truck(self, truck_id: str) -> Optional[Dict]:
        """Get truck by ID"""
        try:
            result = self.trucks.get(ids=[truck_id])
            if result['ids']:
                return result['metadatas'][0]
        except:
            pass
        return None
    
    # ==================== TRIPS ====================
    
    def create_trip(self, driver_id: str, truck_id: str, origin_lat: float, origin_lng: float,
                   origin_address: str, destination_lat: float, destination_lng: float,
                   destination_address: str, outbound_load: str) -> Dict:
        """Create a new trip"""
        trip_id = str(uuid.uuid4())
        trip = {
            "trip_id": trip_id,
            "driver_id": driver_id,
            "truck_id": truck_id,
            "origin_lat": origin_lat,
            "origin_lng": origin_lng,
            "origin_address": origin_address,
            "destination_lat": destination_lat,
            "destination_lng": destination_lng,
            "destination_address": destination_address,
            "outbound_load": outbound_load,
            "is_deadheading": False,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": ""  # Empty string instead of None
        }
        
        self.trips.add(
            ids=[trip_id],
            documents=[f"{origin_address} to {destination_address}"],
            metadatas=[trip]
        )
        return trip
    
    def get_trip(self, trip_id: str) -> Optional[Dict]:
        """Get trip by ID"""
        try:
            result = self.trips.get(ids=[trip_id])
            if result['ids']:
                return result['metadatas'][0]
        except:
            pass
        return None
    
    def update_trip(self, trip_id: str, updates: Dict) -> Optional[Dict]:
        """Update trip"""
        trip = self.get_trip(trip_id)
        if trip:
            trip.update(updates)
            self.trips.update(
                ids=[trip_id],
                documents=[f"{trip['origin_address']} to {trip['destination_address']}"],
                metadatas=[trip]
            )
            return trip
        return None
    
    def mark_deadheading(self, trip_id: str) -> Optional[Dict]:
        """Mark trip as deadheading"""
        return self.update_trip(trip_id, {"is_deadheading": True})
    
    # ==================== LOADS ====================
    
    def create_load(self, vendor_id: str, weight_kg: float, pickup_lat: float, pickup_lng: float,
                   pickup_address: str, destination_lat: float, destination_lng: float,
                   destination_address: str, price_offered: float, currency: str = "INR") -> Dict:
        """Create a new load"""
        load_id = str(uuid.uuid4())
        load = {
            "load_id": load_id,
            "vendor_id": vendor_id,
            "weight_kg": weight_kg,
            "pickup_lat": pickup_lat,
            "pickup_lng": pickup_lng,
            "pickup_address": pickup_address,
            "destination_lat": destination_lat,
            "destination_lng": destination_lng,
            "destination_address": destination_address,
            "price_offered": price_offered,
            "currency": currency,
            "status": "available",
            "assigned_driver_id": "",  # Empty string instead of None
            "assigned_trip_id": "",  # Empty string instead of None
            "created_at": datetime.utcnow().isoformat(),
            "assigned_at": "",
            "picked_up_at": "",
            "delivered_at": ""
        }
        
        self.loads.add(
            ids=[load_id],
            documents=[f"{pickup_address} to {destination_address}"],
            metadatas=[load]
        )
        return load
    
    def get_load(self, load_id: str) -> Optional[Dict]:
        """Get load by ID"""
        try:
            result = self.loads.get(ids=[load_id])
            if result['ids']:
                return result['metadatas'][0]
        except:
            pass
        return None
    
    def get_available_loads(self) -> List[Dict]:
        """Get all available loads"""
        try:
            result = self.loads.get()
            if result['ids']:
                return [meta for meta in result['metadatas'] if meta.get('status') == 'available']
        except:
            pass
        return []
    
    def update_load(self, load_id: str, updates: Dict) -> Optional[Dict]:
        """Update load"""
        load = self.get_load(load_id)
        if load:
            load.update(updates)
            self.loads.update(
                ids=[load_id],
                documents=[f"{load['pickup_address']} to {load['destination_address']}"],
                metadatas=[load]
            )
            return load
        return None
    
    def accept_load(self, load_id: str, trip_id: str, driver_id: str) -> Optional[Dict]:
        """Accept a load"""
        return self.update_load(load_id, {
            "status": "assigned",
            "assigned_trip_id": trip_id,
            "assigned_driver_id": driver_id,
            "assigned_at": datetime.utcnow().isoformat()
        })
    
    # ==================== UTILITY ====================
    
    def clear_all_data(self):
        """Clear all data (for testing)"""
        collections = [self.owners, self.drivers, self.vendors, self.trucks, 
                      self.trips, self.loads, self.load_assignments]
        for collection in collections:
            try:
                self.client.delete_collection(collection.name)
            except:
                pass
        
        # Recreate collections
        self.__init__()


# Global database instance
db = ChromaDatabase()
