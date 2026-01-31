"""
AI-Powered Auto-Scheduler
Automatically matches optimal loads to drivers every 2 minutes
Uses Math Engine and AI Agents for intelligent decision making
"""

import time
import threading
from datetime import datetime
from typing import List, Dict, Optional
from db_chromadb import db
from services.math_engine import math_engine
from agents.coordinator import coordinator_agent
from models.domain import Coordinate


class AutoScheduler:
    """
    Intelligent auto-scheduler that runs every 2 minutes to:
    1. Find all active trips (deadheading drivers)
    2. Get available loads
    3. Use Math Engine to calculate profitability
    4. Use AI Agents to find optimal matches
    5. Auto-assign best load to each driver
    """
    
    def __init__(self, interval_seconds: int = 120):
        self.interval_seconds = interval_seconds
        self.running = False
        self.thread = None
        self.last_run = None
        self.stats = {
            "total_runs": 0,
            "total_matches": 0,
            "total_assignments": 0,
            "last_run_time": None,
            "last_run_matches": 0
        }
    
    def start(self):
        """Start the auto-scheduler background thread"""
        if self.running:
            print("⚠️  Auto-scheduler already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"✅ Auto-scheduler started (runs every {self.interval_seconds}s)")
    
    def stop(self):
        """Stop the auto-scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("🛑 Auto-scheduler stopped")
    
    def _run_loop(self):
        """Main loop that runs every interval"""
        while self.running:
            try:
                self._run_scheduling_cycle()
            except Exception as e:
                print(f"❌ Auto-scheduler error: {e}")
                import traceback
                traceback.print_exc()
            
            # Sleep for interval
            time.sleep(self.interval_seconds)
    
    def _run_scheduling_cycle(self):
        """Run one scheduling cycle"""
        print(f"\n{'='*60}")
        print(f"🤖 AUTO-SCHEDULER CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        self.stats["total_runs"] += 1
        self.stats["last_run_time"] = datetime.now().isoformat()
        
        # Step 1: Find active trips (deadheading drivers)
        active_trips = self._get_active_trips()
        print(f"\n📍 Found {len(active_trips)} active trips")
        
        if not active_trips:
            print("   No active trips to schedule")
            return
        
        # Step 2: Get available loads
        available_loads = db.get_available_loads()
        print(f"📦 Found {len(available_loads)} available loads")
        
        if not available_loads:
            print("   No available loads to assign")
            return
        
        # Step 3: For each trip, find optimal load
        matches_found = 0
        assignments_made = 0
        
        for trip in active_trips:
            print(f"\n🚛 Processing Trip: {trip['trip_id'][:8]}...")
            print(f"   Driver: {trip['driver_id'][:8]}")
            print(f"   Route: {trip['origin_address'][:30]} → {trip['destination_address'][:30]}")
            
            # Find optimal load for this driver
            optimal_load = self._find_optimal_load(trip, available_loads)
            
            if optimal_load:
                matches_found += 1
                print(f"   ✅ Optimal load found: {optimal_load['load_id'][:8]}")
                print(f"      Profit: ₹{optimal_load['profitability']['net_profit']:.2f}")
                print(f"      Score: {optimal_load['profitability']['profitability_score']:.2f}")
                
                # Auto-assign load to driver
                success = self._auto_assign_load(trip, optimal_load)
                if success:
                    assignments_made += 1
                    print(f"      ✅ Auto-assigned to driver")
                    
                    # Remove assigned load from available list
                    available_loads = [l for l in available_loads if l['load_id'] != optimal_load['load_id']]
                else:
                    print(f"      ❌ Assignment failed")
            else:
                print(f"   ℹ️  No profitable load found")
        
        # Update stats
        self.stats["last_run_matches"] = matches_found
        self.stats["total_matches"] += matches_found
        self.stats["total_assignments"] += assignments_made
        
        print(f"\n{'='*60}")
        print(f"📊 CYCLE SUMMARY")
        print(f"{'='*60}")
        print(f"Matches Found: {matches_found}")
        print(f"Assignments Made: {assignments_made}")
        print(f"Total Runs: {self.stats['total_runs']}")
        print(f"Total Assignments: {self.stats['total_assignments']}")
        print(f"{'='*60}\n")
    
    def _get_active_trips(self) -> List[Dict]:
        """Get all active trips that need load matching"""
        try:
            all_trips = db.trips.get()
            
            if not all_trips['ids']:
                return []
            
            # Filter for active trips without assigned loads
            active_trips = []
            for trip_meta in all_trips['metadatas']:
                # Check if trip is active and not completed
                if trip_meta.get('status') == 'active':
                    # Check if trip doesn't have a load assigned yet
                    trip_id = trip_meta['trip_id']
                    
                    # Check if any load is assigned to this trip
                    all_loads = db.loads.get()
                    has_load = False
                    
                    if all_loads['ids']:
                        for load_meta in all_loads['metadatas']:
                            if load_meta.get('assigned_trip_id') == trip_id:
                                has_load = True
                                break
                    
                    if not has_load:
                        active_trips.append(trip_meta)
            
            return active_trips
        except Exception as e:
            print(f"Error getting active trips: {e}")
            return []
    
    def _find_optimal_load(self, trip: Dict, available_loads: List[Dict]) -> Optional[Dict]:
        """
        Find the most optimal load for a trip using Math Engine and AI Agents
        
        Args:
            trip: Trip dictionary
            available_loads: List of available loads
            
        Returns:
            Optimal load with profitability data, or None
        """
        try:
            # Create coordinates
            driver_current = Coordinate(
                lat=trip['origin_lat'],
                lng=trip['origin_lng'],
                address=trip['origin_address']
            )
            driver_destination = Coordinate(
                lat=trip['destination_lat'],
                lng=trip['destination_lng'],
                address=trip['destination_address']
            )
            
            # Use AI Coordinator to get ranked recommendations
            print(f"   🤖 Using AI Agents for load matching...")
            recommendations = coordinator_agent.get_load_recommendations(
                driver_current,
                driver_destination,
                available_loads
            )
            
            if not recommendations:
                print(f"   ℹ️  No compatible loads found by AI")
                return None
            
            # Calculate profitability for each recommendation using Math Engine
            print(f"   🧮 Calculating profitability with Math Engine...")
            loads_with_profit = []
            
            for load in recommendations[:5]:  # Top 5 recommendations
                vendor_pickup = Coordinate(
                    lat=load['pickup_location']['lat'],
                    lng=load['pickup_location']['lng'],
                    address=load['pickup_location']['address']
                )
                vendor_destination = Coordinate(
                    lat=load['destination']['lat'],
                    lng=load['destination']['lng'],
                    address=load['destination']['address']
                )
                
                # Use Math Engine for precise calculations
                profitability = math_engine.calculate_full_profitability(
                    driver_current=driver_current,
                    driver_destination=driver_destination,
                    vendor_pickup=vendor_pickup,
                    vendor_destination=vendor_destination,
                    vendor_offering=load['price_offered']
                )
                
                # Only consider profitable loads
                if profitability['net_profit'] > 0:
                    load['profitability'] = profitability
                    loads_with_profit.append(load)
            
            if not loads_with_profit:
                print(f"   ℹ️  No profitable loads found")
                return None
            
            # Sort by profitability score (profit per hour)
            loads_with_profit.sort(
                key=lambda x: x['profitability']['profitability_score'],
                reverse=True
            )
            
            # Return the most profitable load
            return loads_with_profit[0]
            
        except Exception as e:
            print(f"   ❌ Error finding optimal load: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _auto_assign_load(self, trip: Dict, load: Dict) -> bool:
        """
        Auto-assign a load to a trip
        
        Args:
            trip: Trip dictionary
            load: Load dictionary with profitability data
            
        Returns:
            True if assignment successful
        """
        try:
            # Assign load to trip
            db.accept_load(
                load_id=load['load_id'],
                trip_id=trip['trip_id'],
                driver_id=trip['driver_id']
            )
            
            return True
        except Exception as e:
            print(f"   ❌ Error assigning load: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get scheduler statistics"""
        return {
            **self.stats,
            "running": self.running,
            "interval_seconds": self.interval_seconds
        }
    
    def force_run(self):
        """Force an immediate scheduling cycle (for testing)"""
        print("🔄 Forcing immediate scheduling cycle...")
        self._run_scheduling_cycle()


# Global instance
auto_scheduler = AutoScheduler(interval_seconds=120)  # 2 minutes


if __name__ == "__main__":
    # Test the auto-scheduler
    print("Testing Auto-Scheduler...")
    auto_scheduler.force_run()
