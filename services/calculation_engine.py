"""
Financial Calculation Engine for Daily Financial Report feature
"""

from datetime import datetime, date
from typing import Dict, List, Optional
from db_chromadb import db


class CalculationEngine:
    """Engine for calculating financial metrics"""
    
    # Classification rules for expenses
    FUEL_KEYWORDS = {"gas", "fuel", "petrol", "diesel", "gasoline", "pump"}
    MAINTENANCE_KEYWORDS = {"repair", "maintenance", "service", "oil", "mechanic", "spare", "parts"}
    TOLL_KEYWORDS = {"toll", "highway", "fee", "tax", "road"}
    FOOD_KEYWORDS = {"food", "meal", "restaurant", "lunch", "dinner", "breakfast", "snack", "eat"}
    
    @staticmethod
    def classify_expense(description: str, amount: float = None) -> str:
        """
        Classify expense into one of five categories using rule-based approach
        
        Requirements: 3.5, 8.2
        """
        description_lower = description.lower()
        
        # Check fuel keywords
        if any(keyword in description_lower for keyword in CalculationEngine.FUEL_KEYWORDS):
            return "fuel"
        
        # Check maintenance keywords
        if any(keyword in description_lower for keyword in CalculationEngine.MAINTENANCE_KEYWORDS):
            return "maintenance"
        
        # Check toll keywords
        if any(keyword in description_lower for keyword in CalculationEngine.TOLL_KEYWORDS):
            return "toll"
        
        # Check food keywords
        if any(keyword in description_lower for keyword in CalculationEngine.FOOD_KEYWORDS):
            return "food"
        
        # Default to other
        return "other"
    
    @staticmethod
    def calculate_daily_earnings(driver_id: str, date_str: str) -> float:
        """
        Calculate total earnings from completed trips for a specific day
        
        Requirements: 3.1, 3.6
        """
        try:
            result = db.trips.get()
            
            if not result['ids']:
                return 0.0
            
            total_earnings = 0.0
            
            for metadata in result['metadatas']:
                # Check if trip belongs to driver
                if metadata.get('driver_id') != driver_id:
                    continue
                
                # Check if trip is completed
                if metadata.get('status') != 'completed':
                    continue
                
                # Check if trip was completed on the specified date
                completed_at = metadata.get('completed_at', '')
                if completed_at and completed_at.startswith(date_str):
                    # Get earnings from trip or associated load
                    earnings = metadata.get('earnings', 0.0)
                    if earnings:
                        total_earnings += float(earnings)
            
            return total_earnings
        
        except Exception as e:
            print(f"Error calculating daily earnings: {e}")
            return 0.0
    
    @staticmethod
    def calculate_daily_expenses(driver_id: str, date_str: str) -> float:
        """
        Calculate total expenses for a specific day
        
        Requirements: 3.2
        """
        try:
            result = db.expenses.get()
            
            if not result['ids']:
                return 0.0
            
            total_expenses = 0.0
            
            for metadata in result['metadatas']:
                # Check if expense belongs to driver
                if metadata.get('driver_id') != driver_id:
                    continue
                
                # Check if expense was recorded on the specified date
                timestamp = metadata.get('timestamp', '')
                if timestamp and timestamp.startswith(date_str):
                    amount = metadata.get('amount', 0.0)
                    total_expenses += float(amount)
            
            return total_expenses
        
        except Exception as e:
            print(f"Error calculating daily expenses: {e}")
            return 0.0
    
    @staticmethod
    def calculate_net_profit(driver_id: str, date_str: str) -> float:
        """
        Calculate net profit (earnings - expenses) for a specific day
        
        Requirements: 3.3
        """
        earnings = CalculationEngine.calculate_daily_earnings(driver_id, date_str)
        expenses = CalculationEngine.calculate_daily_expenses(driver_id, date_str)
        return earnings - expenses
    
    @staticmethod
    def get_expense_breakdown(driver_id: str, date_str: str) -> Dict[str, float]:
        """
        Get breakdown of expenses by category for a specific day
        
        Requirements: 3.4
        """
        breakdown = {
            "fuel": 0.0,
            "maintenance": 0.0,
            "toll": 0.0,
            "food": 0.0,
            "other": 0.0
        }
        
        try:
            result = db.expenses.get()
            
            if not result['ids']:
                return breakdown
            
            for metadata in result['metadatas']:
                # Check if expense belongs to driver
                if metadata.get('driver_id') != driver_id:
                    continue
                
                # Check if expense was recorded on the specified date
                timestamp = metadata.get('timestamp', '')
                if timestamp and timestamp.startswith(date_str):
                    category = metadata.get('category', 'other')
                    amount = metadata.get('amount', 0.0)
                    
                    if category in breakdown:
                        breakdown[category] += float(amount)
                    else:
                        breakdown['other'] += float(amount)
            
            return breakdown
        
        except Exception as e:
            print(f"Error calculating expense breakdown: {e}")
            return breakdown
    
    @staticmethod
    def get_daily_trips(driver_id: str, date_str: str) -> List[Dict]:
        """
        Get all completed trips for a specific day
        
        Requirements: 4.2
        """
        try:
            result = db.trips.get()
            
            if not result['ids']:
                return []
            
            trips = []
            
            for metadata in result['metadatas']:
                # Check if trip belongs to driver
                if metadata.get('driver_id') != driver_id:
                    continue
                
                # Check if trip is completed
                if metadata.get('status') != 'completed':
                    continue
                
                # Check if trip was completed on the specified date
                completed_at = metadata.get('completed_at', '')
                if completed_at and completed_at.startswith(date_str):
                    trips.append({
                        "trip_id": metadata.get('trip_id', ''),
                        "origin": metadata.get('origin_address', ''),
                        "destination": metadata.get('destination_address', ''),
                        "load_details": metadata.get('outbound_load', ''),
                        "earnings": float(metadata.get('earnings', 0.0))
                    })
            
            return trips
        
        except Exception as e:
            print(f"Error retrieving daily trips: {e}")
            return []
    
    @staticmethod
    def calculate_performance_metrics(driver_id: str, date_str: str) -> Dict:
        """
        Calculate driver performance metrics for a specific day
        
        Requirements: 4.6
        """
        trips = CalculationEngine.get_daily_trips(driver_id, date_str)
        earnings = CalculationEngine.calculate_daily_earnings(driver_id, date_str)
        expenses = CalculationEngine.calculate_daily_expenses(driver_id, date_str)
        
        trips_completed = len(trips)
        average_earnings_per_trip = earnings / trips_completed if trips_completed > 0 else 0.0
        expense_ratio = expenses / earnings if earnings > 0 else 0.0
        
        return {
            "trips_completed": trips_completed,
            "average_earnings_per_trip": round(average_earnings_per_trip, 2),
            "expense_ratio": round(expense_ratio, 4)
        }
