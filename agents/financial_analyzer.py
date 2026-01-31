from crewai import Agent, Task
from crewai.tools import tool
from typing import Dict, List

from agents.base import create_agent
from services.math_engine import math_engine


@tool("calculate_profitability")
def calculate_profitability_tool(
    extra_distance_km: float,
    extra_time_hours: float,
    vendor_offering: float
) -> Dict:
    """Calculate profitability metrics for a load opportunity"""
    fuel_cost = math_engine.calculate_fuel_cost(extra_distance_km)
    time_cost = math_engine.calculate_time_cost(extra_time_hours)
    net_profit = math_engine.calculate_net_profit(vendor_offering, fuel_cost, time_cost)
    profitability_score = math_engine.calculate_profitability_score(net_profit, extra_time_hours)
    
    return {
        "fuel_cost": fuel_cost,
        "time_cost": time_cost,
        "net_profit": net_profit,
        "profitability_score": profitability_score
    }


class FinancialAnalyzerAgent:
    """Agent responsible for evaluating profitability of load opportunities"""
    
    def __init__(self):
        self.agent = create_agent(
            role="Financial Analysis Specialist",
            goal="Evaluate profitability and rank load opportunities to maximize driver earnings while considering all costs",
            backstory="""You are a financial expert specializing in transportation economics. 
            You understand the true costs of trucking operations including fuel, time, and 
            opportunity costs. You help drivers make financially sound decisions by providing 
            clear profitability analysis and ranking opportunities by their earning potential.""",
            tools=[calculate_profitability_tool],
            verbose=True
        )
    
    def analyze_profitability(
        self,
        load_opportunities: List[Dict],
        route_metrics: Dict
    ) -> List[Dict]:
        """
        Analyze profitability for all load opportunities and rank them
        
        Args:
            load_opportunities: List of matched loads
            route_metrics: Route metrics for each load
            
        Returns:
            List of load opportunities with profitability analysis, ranked by score
        """
        analyzed_loads = []
        
        for load in load_opportunities:
            # Get route metrics for this load
            metrics = route_metrics.get(load["load_id"], {})
            
            if not metrics:
                continue
            
            # Calculate profitability
            profitability = calculate_profitability_tool(
                extra_distance_km=metrics["extra_distance_km"],
                extra_time_hours=metrics["extra_time_hours"],
                vendor_offering=load["price_offered"]
            )
            
            # Only include profitable loads
            if profitability["net_profit"] > 0:
                analyzed_loads.append({
                    **load,
                    "calculation": {
                        "extra_distance_km": metrics["extra_distance_km"],
                        "extra_time_hours": metrics["extra_time_hours"],
                        "fuel_cost": profitability["fuel_cost"],
                        "time_cost": profitability["time_cost"],
                        "net_profit": profitability["net_profit"],
                        "profitability_score": profitability["profitability_score"]
                    }
                })
        
        # Sort by profitability score (descending)
        analyzed_loads.sort(key=lambda x: x["calculation"]["profitability_score"], reverse=True)
        
        # Add rank
        for idx, load in enumerate(analyzed_loads, 1):
            load["rank"] = idx
        
        return analyzed_loads


# Global instance
financial_analyzer_agent = FinancialAnalyzerAgent()
