from typing import List, Dict

from agents.load_matcher import load_matcher_agent
from agents.route_optimizer import route_optimizer_agent
from agents.financial_analyzer import financial_analyzer_agent
from models.domain import Coordinate


class CoordinatorAgent:
    """
    Orchestrates the workflow between specialized agents to provide 
    optimal load recommendations for deadheading drivers
    """
    
    def __init__(self):
        self.load_matcher = load_matcher_agent
        self.route_optimizer = route_optimizer_agent
        self.financial_analyzer = financial_analyzer_agent
    
    def get_load_recommendations(
        self,
        driver_current: Coordinate,
        driver_destination: Coordinate,
        available_loads: List[Dict]
    ) -> List[Dict]:
        """
        Orchestrate all agents to get ranked load recommendations
        
        Args:
            driver_current: Driver's current location
            driver_destination: Driver's intended destination
            available_loads: List of available loads from ChromaDB
            
        Returns:
            List of load opportunities ranked by profitability
        """
        try:
            # Step 1: Load Matcher - Find compatible loads
            matched_loads = self.load_matcher.match_loads(
                driver_current, driver_destination, available_loads
            )
            
            if not matched_loads:
                return []
            
            # Step 2: Route Optimizer - Calculate route metrics for each load
            route_metrics = {}
            for load in matched_loads:
                vendor_pickup = Coordinate(**load["pickup_location"])
                vendor_destination = Coordinate(**load["destination"])
                
                metrics = self.route_optimizer.calculate_route_metrics(
                    driver_current,
                    driver_destination,
                    vendor_pickup,
                    vendor_destination
                )
                
                route_metrics[load["load_id"]] = metrics
            
            # Step 3: Financial Analyzer - Analyze profitability and rank
            ranked_opportunities = self.financial_analyzer.analyze_profitability(
                matched_loads, route_metrics
            )
            
            return ranked_opportunities
            
        except Exception as e:
            # Fallback: simple distance-based matching
            print(f"Agent coordination failed: {e}. Using fallback matching.")
            return self._fallback_matching(driver_current, driver_destination, available_loads)
    
    def _fallback_matching(
        self,
        driver_current: Coordinate,
        driver_destination: Coordinate,
        available_loads: List[Dict]
    ) -> List[Dict]:
        """
        Fallback to simple distance-based matching if agent coordination fails
        """
        # Use load matcher without AI agents
        matched_loads = self.load_matcher.match_loads(
            driver_current, driver_destination, available_loads
        )
        
        # Sort by deviation (closest first)
        matched_loads.sort(key=lambda x: x.get("deviation_km", float('inf')))
        
        return matched_loads[:5]  # Return top 5


# Global instance
coordinator_agent = CoordinatorAgent()
