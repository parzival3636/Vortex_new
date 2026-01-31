"""
Database layer for verification system
Stores QR codes, verification events, and receiver data
"""
import chromadb
from chromadb.config import Settings
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Dict, List, Optional


class VerificationDatabase:
    """Database for QR verification system"""
    
    def __init__(self, persist_directory: str = "./verification_data"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Collections
        self.qr_codes = self._get_or_create_collection("qr_codes")
        self.verifications = self._get_or_create_collection("verifications")
        self.receivers = self._get_or_create_collection("receivers")
        self.notifications = self._get_or_create_collection("notifications")
    
    def _get_or_create_collection(self, name: str):
        """Get or create a collection"""
        try:
            return self.client.get_collection(name=name)
        except:
            return self.client.create_collection(name=name)
    
    # QR Code Operations
    def create_qr_code(
        self,
        qr_type: str,
        load_id: str,
        driver_id: str,
        vendor_id: str,
        location_lat: float,
        location_lng: float,
        receiver_id: str = None,
        expiry_hours: int = 24
    ) -> Dict:
        """Generate a new QR code"""
        qr_id = str(uuid4())
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=expiry_hours)
        
        qr_data = {
            "qr_id": qr_id,
            "qr_type": qr_type,
            "load_id": load_id,
            "driver_id": driver_id,
            "vendor_id": vendor_id,
            "receiver_id": receiver_id or "",
            "location_lat": location_lat,
            "location_lng": location_lng,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_used": False,
            "verification_radius_meters": 100.0
        }
        
        self.qr_codes.add(
            ids=[qr_id],
            metadatas=[qr_data],
            documents=[f"QR {qr_type} for load {load_id}"]
        )
        
        return qr_data
    
    def get_qr_code(self, qr_id: str) -> Optional[Dict]:
        """Get QR code by ID"""
        result = self.qr_codes.get(ids=[qr_id])
        if result['ids']:
            return result['metadatas'][0]
        return None
    
    def mark_qr_used(self, qr_id: str) -> bool:
        """Mark QR code as used"""
        qr_data = self.get_qr_code(qr_id)
        if not qr_data:
            return False
        
        qr_data["is_used"] = True
        qr_data["used_at"] = datetime.utcnow().isoformat()
        
        self.qr_codes.update(
            ids=[qr_id],
            metadatas=[qr_data]
        )
        return True
    
    def get_qr_codes_for_load(self, load_id: str) -> List[Dict]:
        """Get all QR codes for a load"""
        all_qrs = self.qr_codes.get()
        if not all_qrs['ids']:
            return []
        
        return [qr for qr in all_qrs['metadatas'] if qr['load_id'] == load_id]
    
    # Verification Operations
    def create_verification_event(
        self,
        qr_id: str,
        load_id: str,
        verification_type: str,
        scanned_by_id: str,
        scanned_by_type: str,
        success: bool,
        message: str,
        confidence_score: float = 0.0,
        anomalies: List[str] = None,
        scan_location_lat: float = 0.0,
        scan_location_lng: float = 0.0
    ) -> Dict:
        """Record a verification event"""
        verification_id = str(uuid4())
        
        verification_data = {
            "verification_id": verification_id,
            "qr_id": qr_id,
            "load_id": load_id,
            "verification_type": verification_type,
            "scanned_by_id": scanned_by_id,
            "scanned_by_type": scanned_by_type,
            "success": success,
            "message": message,
            "confidence_score": confidence_score,
            "anomalies": ",".join(anomalies) if anomalies else "",
            "scan_location_lat": scan_location_lat,
            "scan_location_lng": scan_location_lng,
            "verified_at": datetime.utcnow().isoformat()
        }
        
        self.verifications.add(
            ids=[verification_id],
            metadatas=[verification_data],
            documents=[f"Verification {verification_type} for load {load_id}"]
        )
        
        return verification_data
    
    def get_verifications_for_load(self, load_id: str) -> List[Dict]:
        """Get all verification events for a load"""
        all_verifications = self.verifications.get()
        if not all_verifications['ids']:
            return []
        
        return [v for v in all_verifications['metadatas'] if v['load_id'] == load_id]
    
    # Receiver Operations
    def create_receiver(
        self,
        name: str,
        email: str,
        phone: str,
        location_lat: float,
        location_lng: float,
        location_address: str,
        company_name: str = None
    ) -> Dict:
        """Create a new receiver"""
        receiver_id = str(uuid4())
        
        receiver_data = {
            "receiver_id": receiver_id,
            "name": name,
            "email": email,
            "phone": phone,
            "location_lat": location_lat,
            "location_lng": location_lng,
            "location_address": location_address,
            "company_name": company_name or "",
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.receivers.add(
            ids=[receiver_id],
            metadatas=[receiver_data],
            documents=[f"Receiver {name} at {location_address}"]
        )
        
        return receiver_data
    
    def get_receiver(self, receiver_id: str) -> Optional[Dict]:
        """Get receiver by ID"""
        result = self.receivers.get(ids=[receiver_id])
        if result['ids']:
            return result['metadatas'][0]
        return None
    
    def get_all_receivers(self) -> List[Dict]:
        """Get all receivers"""
        result = self.receivers.get()
        return result['metadatas'] if result['ids'] else []
    
    # Notification Operations
    def create_notification(
        self,
        recipient_id: str,
        recipient_type: str,
        channel: str,
        priority: str,
        title: str,
        message: str,
        action_url: str = None,
        metadata: Dict = None
    ) -> Dict:
        """Create a notification record"""
        notification_id = str(uuid4())
        
        notification_data = {
            "notification_id": notification_id,
            "recipient_id": recipient_id,
            "recipient_type": recipient_type,
            "channel": channel,
            "priority": priority,
            "title": title,
            "message": message,
            "action_url": action_url or "",
            "metadata": str(metadata) if metadata else "",
            "created_at": datetime.utcnow().isoformat(),
            "read": False
        }
        
        self.notifications.add(
            ids=[notification_id],
            metadatas=[notification_data],
            documents=[f"{title}: {message}"]
        )
        
        return notification_data
    
    def get_notifications_for_recipient(
        self,
        recipient_id: str,
        unread_only: bool = False
    ) -> List[Dict]:
        """Get notifications for a recipient"""
        all_notifications = self.notifications.get()
        if not all_notifications['ids']:
            return []
        
        notifications = [n for n in all_notifications['metadatas'] 
                        if n['recipient_id'] == recipient_id]
        
        if unread_only:
            notifications = [n for n in notifications if not n.get('read', False)]
        
        # Sort by created_at descending
        notifications.sort(key=lambda x: x['created_at'], reverse=True)
        return notifications
    
    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        notification = self.notifications.get(ids=[notification_id])
        if not notification['ids']:
            return False
        
        notification_data = notification['metadatas'][0]
        notification_data['read'] = True
        
        self.notifications.update(
            ids=[notification_id],
            metadatas=[notification_data]
        )
        return True


# Global instance
verification_db = VerificationDatabase()
