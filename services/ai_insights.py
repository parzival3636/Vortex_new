"""
AI Insights Generator for Daily Financial Report feature
"""

from typing import Dict, List
from datetime import datetime


class AIInsightGenerator:
    """Generator for AI-powered expense insights"""
    
    def generate_insights(
        self,
        driver_id: str,
        date: str,
        trips: List[Dict],
        total_earnings: float,
        total_expenses: float,
        expense_breakdown: Dict[str, float]
    ) -> Dict:
        """
        Generate AI insights about daily expenses and performance
        
        Requirements: 4.7, 8.1, 8.3, 8.5
        """
        
        # Generate summary
        summary = self._generate_summary(
            total_earnings, total_expenses, len(trips), expense_breakdown
        )
        
        # Identify anomalies
        anomalies = self._identify_anomalies(
            total_earnings, total_expenses, expense_breakdown
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            total_earnings, total_expenses, expense_breakdown, len(trips)
        )
        
        return {
            "summary": summary,
            "anomalies": anomalies,
            "recommendations": recommendations
        }
    
    def _generate_summary(
        self,
        total_earnings: float,
        total_expenses: float,
        trips_count: int,
        expense_breakdown: Dict[str, float]
    ) -> str:
        """Generate summary narrative"""
        
        net_profit = total_earnings - total_expenses
        expense_ratio = (total_expenses / total_earnings * 100) if total_earnings > 0 else 0
        
        # Find highest expense category
        highest_category = max(expense_breakdown.items(), key=lambda x: x[1])[0] if expense_breakdown else "unknown"
        highest_amount = max(expense_breakdown.values()) if expense_breakdown else 0
        
        summary = f"Daily Report Summary: Completed {trips_count} trip(s) with total earnings of ₹{total_earnings:.2f}. "
        summary += f"Total expenses were ₹{total_expenses:.2f}, resulting in a net profit of ₹{net_profit:.2f}. "
        summary += f"Expenses represent {expense_ratio:.1f}% of earnings. "
        summary += f"The highest expense category was {highest_category} at ₹{highest_amount:.2f}."
        
        return summary
    
    def _identify_anomalies(
        self,
        total_earnings: float,
        total_expenses: float,
        expense_breakdown: Dict[str, float]
    ) -> List[str]:
        """Identify unusual spending patterns"""
        
        anomalies = []
        
        # Check if expenses exceed earnings
        if total_expenses > total_earnings:
            anomalies.append(
                f"⚠️ Expenses (₹{total_expenses:.2f}) exceed earnings (₹{total_earnings:.2f}). "
                f"Net loss of ₹{total_expenses - total_earnings:.2f}."
            )
        
        # Check expense ratio
        expense_ratio = (total_expenses / total_earnings * 100) if total_earnings > 0 else 0
        if expense_ratio > 50:
            anomalies.append(
                f"⚠️ High expense ratio: {expense_ratio:.1f}% of earnings spent on expenses. "
                f"Consider cost optimization strategies."
            )
        
        # Check for unusually high fuel expenses
        fuel_expenses = expense_breakdown.get("fuel", 0)
        if fuel_expenses > total_earnings * 0.3:
            anomalies.append(
                f"⚠️ Fuel expenses are high at ₹{fuel_expenses:.2f}. "
                f"Consider route optimization or fuel efficiency improvements."
            )
        
        # Check for maintenance expenses
        maintenance_expenses = expense_breakdown.get("maintenance", 0)
        if maintenance_expenses > total_earnings * 0.2:
            anomalies.append(
                f"⚠️ Maintenance expenses are significant at ₹{maintenance_expenses:.2f}. "
                f"Schedule preventive maintenance to avoid future issues."
            )
        
        return anomalies if anomalies else ["No significant anomalies detected."]
    
    def _generate_recommendations(
        self,
        total_earnings: float,
        total_expenses: float,
        expense_breakdown: Dict[str, float],
        trips_count: int
    ) -> List[str]:
        """Generate cost optimization recommendations"""
        
        recommendations = []
        
        # Recommendation based on expense ratio
        expense_ratio = (total_expenses / total_earnings * 100) if total_earnings > 0 else 0
        if expense_ratio > 40:
            recommendations.append(
                "💡 Focus on reducing operational costs. Target a 30-35% expense ratio for better profitability."
            )
        
        # Recommendation for fuel optimization
        fuel_expenses = expense_breakdown.get("fuel", 0)
        if fuel_expenses > 0:
            recommendations.append(
                "💡 Optimize fuel consumption by maintaining steady speeds and reducing idle time."
            )
        
        # Recommendation for maintenance
        maintenance_expenses = expense_breakdown.get("maintenance", 0)
        if maintenance_expenses == 0:
            recommendations.append(
                "💡 Schedule regular preventive maintenance to avoid costly emergency repairs."
            )
        
        # Recommendation for trip efficiency
        if trips_count > 0:
            avg_earnings = total_earnings / trips_count
            if avg_earnings < 500:
                recommendations.append(
                    f"💡 Average earnings per trip is ₹{avg_earnings:.2f}. "
                    f"Consider accepting higher-paying loads to improve profitability."
                )
        
        # Recommendation for food expenses
        food_expenses = expense_breakdown.get("food", 0)
        if food_expenses > total_earnings * 0.1:
            recommendations.append(
                "💡 Food expenses are high. Consider meal planning and bringing food from home."
            )
        
        # Recommendation for toll optimization
        toll_expenses = expense_breakdown.get("toll", 0)
        if toll_expenses > total_earnings * 0.15:
            recommendations.append(
                "💡 Toll expenses are significant. Explore alternative routes when possible."
            )
        
        return recommendations if recommendations else [
            "💡 Great job maintaining low expenses! Continue monitoring your spending patterns."
        ]
