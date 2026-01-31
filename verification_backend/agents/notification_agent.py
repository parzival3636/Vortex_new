"""
AI Agent for Automated Notifications
Sends real-time notifications to vendors, drivers, and receivers
"""
from datetime import datetime
from typing import Dict, List
from uuid import UUID


class NotificationAgent:
    """
    AI Agent responsible for:
    - Sending automated notifications
    - Managing notification priorities
    - Tracking notification delivery
    - Escalating critical events
    """
    
    def __init__(self):
        self.notification_channels = ["email", "sms", "push", "in_app"]
        self.notification_history = []
    
    def notify_qr_generated(
        self,
        load_id: str,
        qr_type: str,
        vendor_id: str,
        driver_id: str,
        receiver_id: str = None
    ) -> Dict:
        """
        Notify relevant parties when QR code is generated
        
        Args:
            load_id: Load identifier
            qr_type: "pickup" or "delivery"
            vendor_id: Vendor identifier
            driver_id: Driver identifier
            receiver_id: Receiver identifier (for delivery QR)
        """
        notifications = []
        
        if qr_type == "pickup":
            # Notify vendor
            notifications.append({
                "recipient_id": vendor_id,
                "recipient_type": "vendor",
                "channel": "in_app",
                "priority": "high",
                "title": "Pickup QR Code Generated",
                "message": f"Driver is assigned to load {load_id}. QR code ready for verification.",
                "action_url": f"/vendor/loads/{load_id}",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Notify driver
            notifications.append({
                "recipient_id": driver_id,
                "recipient_type": "driver",
                "channel": "push",
                "priority": "high",
                "title": "Load Assignment Confirmed",
                "message": f"Scan QR code at pickup location to verify your identity.",
                "action_url": f"/driver/scan-qr/{load_id}",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        elif qr_type == "delivery":
            # Notify receiver
            if receiver_id:
                notifications.append({
                    "recipient_id": receiver_id,
                    "recipient_type": "receiver",
                    "channel": "in_app",
                    "priority": "high",
                    "title": "Delivery QR Code Ready",
                    "message": f"Driver is en route. Scan QR code upon delivery to verify.",
                    "action_url": f"/receiver/loads/{load_id}",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Notify vendor
            notifications.append({
                "recipient_id": vendor_id,
                "recipient_type": "vendor",
                "channel": "in_app",
                "priority": "normal",
                "title": "Load In Transit",
                "message": f"Load {load_id} picked up and in transit to delivery location.",
                "action_url": f"/vendor/loads/{load_id}",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        self._send_notifications(notifications)
        return {"sent": len(notifications), "notifications": notifications}
    
    def notify_pickup_verified(
        self,
        load_id: str,
        vendor_id: str,
        driver_id: str,
        verification_details: Dict
    ) -> Dict:
        """Notify when pickup is verified"""
        notifications = []
        
        # Notify vendor
        notifications.append({
            "recipient_id": vendor_id,
            "recipient_type": "vendor",
            "channel": "in_app",
            "priority": "high",
            "title": "✓ Pickup Verified",
            "message": f"Driver identity confirmed. Load {load_id} picked up successfully.",
            "metadata": {
                "confidence_score": verification_details.get("confidence_score"),
                "verified_at": verification_details.get("verified_at")
            },
            "action_url": f"/vendor/loads/{load_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Notify driver
        notifications.append({
            "recipient_id": driver_id,
            "recipient_type": "driver",
            "channel": "push",
            "priority": "normal",
            "title": "Pickup Confirmed",
            "message": "Identity verified. Proceed to delivery location.",
            "action_url": f"/driver/loads/{load_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self._send_notifications(notifications)
        return {"sent": len(notifications), "notifications": notifications}
    
    def notify_delivery_verified(
        self,
        load_id: str,
        vendor_id: str,
        driver_id: str,
        receiver_id: str,
        verification_details: Dict
    ) -> Dict:
        """Notify when delivery is verified"""
        notifications = []
        
        # Notify vendor - CRITICAL notification
        notifications.append({
            "recipient_id": vendor_id,
            "recipient_type": "vendor",
            "channel": "email",
            "priority": "critical",
            "title": "✓ Delivery Completed",
            "message": f"Load {load_id} delivered and verified. Receiver confirmed receipt.",
            "metadata": {
                "confidence_score": verification_details.get("confidence_score"),
                "verified_at": verification_details.get("verified_at")
            },
            "action_url": f"/vendor/loads/{load_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Notify driver
        notifications.append({
            "recipient_id": driver_id,
            "recipient_type": "driver",
            "channel": "push",
            "priority": "normal",
            "title": "Delivery Confirmed",
            "message": "Load delivered successfully. Payment processing initiated.",
            "action_url": f"/driver/loads/{load_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Notify receiver
        notifications.append({
            "recipient_id": receiver_id,
            "recipient_type": "receiver",
            "channel": "in_app",
            "priority": "normal",
            "title": "Receipt Confirmed",
            "message": f"Load {load_id} received and verified in system.",
            "action_url": f"/receiver/loads/{load_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self._send_notifications(notifications)
        return {"sent": len(notifications), "notifications": notifications}
    
    def notify_anomaly_detected(
        self,
        load_id: str,
        vendor_id: str,
        anomaly_type: str,
        details: Dict
    ) -> Dict:
        """Send critical alert when anomaly is detected"""
        notifications = []
        
        # Critical alert to vendor
        notifications.append({
            "recipient_id": vendor_id,
            "recipient_type": "vendor",
            "channel": "sms",
            "priority": "critical",
            "title": "⚠️ Security Alert",
            "message": f"Anomaly detected for load {load_id}: {anomaly_type}",
            "metadata": details,
            "action_url": f"/vendor/alerts/{load_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Also send in-app notification
        notifications.append({
            "recipient_id": vendor_id,
            "recipient_type": "vendor",
            "channel": "in_app",
            "priority": "critical",
            "title": "⚠️ Verification Failed",
            "message": f"Load {load_id}: {details.get('message', 'Unknown error')}",
            "metadata": details,
            "action_url": f"/vendor/alerts/{load_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self._send_notifications(notifications)
        return {"sent": len(notifications), "notifications": notifications}
    
    def _send_notifications(self, notifications: List[Dict]) -> None:
        """
        Send notifications through appropriate channels
        In production, this would integrate with email/SMS/push services
        """
        for notification in notifications:
            # Store in history
            self.notification_history.append(notification)
            
            # Log notification (in production, send via actual channels)
            print(f"[{notification['priority'].upper()}] {notification['channel']} -> "
                  f"{notification['recipient_type']}:{notification['recipient_id']}")
            print(f"  {notification['title']}: {notification['message']}")
    
    def get_notification_history(
        self,
        recipient_id: str = None,
        limit: int = 50
    ) -> List[Dict]:
        """Get notification history for a recipient"""
        if recipient_id:
            filtered = [n for n in self.notification_history 
                       if n["recipient_id"] == recipient_id]
            return filtered[-limit:]
        return self.notification_history[-limit:]


# Global instance
notification_agent = NotificationAgent()
