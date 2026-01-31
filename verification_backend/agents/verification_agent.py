"""
AI Agent for QR Code Verification and Identity Matching
Handles driver identity verification at pickup and delivery points
"""
import math
from datetime import datetime, timedelta
from typing import Dict, Optional
from uuid import UUID


class VerificationAgent:
    """
    AI Agent responsible for:
    - Validating QR code authenticity
    - Verifying driver identity matches assignment
    - Checking location proximity
    - Detecting anomalies and fraud attempts
    """
    
    def __init__(self):
        self.verification_radius_meters = 100.0  # Default 100m radius
        self.qr_expiry_hours = 24  # QR codes expire after 24 hours
    
    def verify_pickup_scan(
        self,
        qr_data: Dict,
        scanned_by_id: str,
        scan_location: tuple[float, float],
        load_assignment: Dict
    ) -> Dict:
        """
        Verify driver scanning QR at pickup location
        
        Args:
            qr_data: QR code data from database
            scanned_by_id: ID of person scanning
            scan_location: (lat, lng) of scan location
            load_assignment: Load assignment details
            
        Returns:
            Verification result with success status and details
        """
        verification_result = {
            "success": False,
            "message": "",
            "anomalies": [],
            "confidence_score": 0.0
        }
        
        # Check 1: QR code not expired
        if self._is_qr_expired(qr_data):
            verification_result["message"] = "QR code has expired"
            verification_result["anomalies"].append("expired_qr")
            return verification_result
        
        # Check 2: QR code not already used
        if qr_data.get("is_used", False):
            verification_result["message"] = "QR code already used"
            verification_result["anomalies"].append("reused_qr")
            return verification_result
        
        # Check 3: Driver ID matches assignment
        if str(scanned_by_id) != str(load_assignment.get("assigned_driver_id")):
            verification_result["message"] = "Driver ID does not match assignment"
            verification_result["anomalies"].append("driver_mismatch")
            return verification_result
        
        # Check 4: Location proximity
        qr_location = (qr_data["location_lat"], qr_data["location_lng"])
        distance = self._calculate_distance(scan_location, qr_location)
        
        if distance > self.verification_radius_meters:
            verification_result["message"] = f"Scan location too far from pickup point ({distance:.0f}m away)"
            verification_result["anomalies"].append("location_mismatch")
            verification_result["distance_meters"] = distance
            return verification_result
        
        # Check 5: Time-based anomaly detection
        time_anomaly = self._check_time_anomaly(qr_data, load_assignment)
        if time_anomaly:
            verification_result["anomalies"].append(time_anomaly)
        
        # All checks passed
        confidence_score = self._calculate_confidence_score(
            distance, 
            len(verification_result["anomalies"])
        )
        
        verification_result.update({
            "success": True,
            "message": "Driver identity verified successfully at pickup",
            "confidence_score": confidence_score,
            "distance_meters": distance,
            "verified_at": datetime.utcnow().isoformat()
        })
        
        return verification_result
    
    def verify_delivery_scan(
        self,
        qr_data: Dict,
        scanned_by_receiver_id: str,
        scan_location: tuple[float, float],
        load_assignment: Dict,
        driver_id: str
    ) -> Dict:
        """
        Verify receiver scanning QR at delivery location
        
        Args:
            qr_data: QR code data from database
            scanned_by_receiver_id: ID of receiver scanning
            scan_location: (lat, lng) of scan location
            load_assignment: Load assignment details
            driver_id: ID of driver delivering
            
        Returns:
            Verification result with success status and details
        """
        verification_result = {
            "success": False,
            "message": "",
            "anomalies": [],
            "confidence_score": 0.0
        }
        
        # Check 1: QR code not expired
        if self._is_qr_expired(qr_data):
            verification_result["message"] = "QR code has expired"
            verification_result["anomalies"].append("expired_qr")
            return verification_result
        
        # Check 2: QR code not already used
        if qr_data.get("is_used", False):
            verification_result["message"] = "QR code already used"
            verification_result["anomalies"].append("reused_qr")
            return verification_result
        
        # Check 3: Receiver ID matches expected receiver
        expected_receiver = load_assignment.get("receiver_id")
        if expected_receiver and str(scanned_by_receiver_id) != str(expected_receiver):
            verification_result["message"] = "Receiver ID does not match expected recipient"
            verification_result["anomalies"].append("receiver_mismatch")
            return verification_result
        
        # Check 4: Driver ID matches the one who picked up
        if str(driver_id) != str(load_assignment.get("assigned_driver_id")):
            verification_result["message"] = "Driver delivering does not match assigned driver"
            verification_result["anomalies"].append("driver_mismatch")
            return verification_result
        
        # Check 5: Location proximity
        qr_location = (qr_data["location_lat"], qr_data["location_lng"])
        distance = self._calculate_distance(scan_location, qr_location)
        
        if distance > self.verification_radius_meters:
            verification_result["message"] = f"Scan location too far from delivery point ({distance:.0f}m away)"
            verification_result["anomalies"].append("location_mismatch")
            verification_result["distance_meters"] = distance
            return verification_result
        
        # Check 6: Pickup must have been verified first
        if not load_assignment.get("pickup_verified_at"):
            verification_result["message"] = "Cannot verify delivery before pickup verification"
            verification_result["anomalies"].append("sequence_violation")
            return verification_result
        
        # All checks passed
        confidence_score = self._calculate_confidence_score(
            distance, 
            len(verification_result["anomalies"])
        )
        
        verification_result.update({
            "success": True,
            "message": "Delivery verified successfully. Load received by correct recipient.",
            "confidence_score": confidence_score,
            "distance_meters": distance,
            "verified_at": datetime.utcnow().isoformat()
        })
        
        return verification_result
    
    def _is_qr_expired(self, qr_data: Dict) -> bool:
        """Check if QR code has expired"""
        expires_at = datetime.fromisoformat(qr_data["expires_at"])
        return datetime.utcnow() > expires_at
    
    def _calculate_distance(
        self, 
        point1: tuple[float, float], 
        point2: tuple[float, float]
    ) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula
        Returns distance in meters
        """
        lat1, lng1 = point1
        lat2, lng2 = point2
        
        R = 6371000  # Earth's radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_phi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _check_time_anomaly(self, qr_data: Dict, load_assignment: Dict) -> Optional[str]:
        """Check for time-based anomalies"""
        created_at = datetime.fromisoformat(qr_data["created_at"])
        now = datetime.utcnow()
        
        # If scanned within 1 minute of creation, might be suspicious
        if (now - created_at).total_seconds() < 60:
            return "suspicious_timing"
        
        return None
    
    def _calculate_confidence_score(self, distance: float, anomaly_count: int) -> float:
        """
        Calculate confidence score for verification
        100% = perfect match, 0% = complete failure
        """
        # Base score
        score = 100.0
        
        # Deduct for distance (max 20 points)
        distance_penalty = min(20, (distance / self.verification_radius_meters) * 20)
        score -= distance_penalty
        
        # Deduct for anomalies (10 points each)
        score -= (anomaly_count * 10)
        
        return max(0.0, min(100.0, score))


# Global instance
verification_agent = VerificationAgent()
