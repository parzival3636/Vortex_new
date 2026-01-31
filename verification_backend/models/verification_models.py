from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class QRCodeData(BaseModel):
    """QR Code data structure"""
    qr_id: UUID
    qr_type: str  # "pickup" or "delivery"
    load_id: UUID
    driver_id: UUID
    vendor_id: UUID
    receiver_id: Optional[UUID] = None
    created_at: datetime
    expires_at: datetime
    is_used: bool = False
    location_lat: float
    location_lng: float
    verification_radius_meters: float = 100.0


class QRVerificationRequest(BaseModel):
    """Request to verify QR code scan"""
    qr_id: UUID
    scanned_by_id: UUID
    scanned_by_type: str  # "driver" or "receiver"
    scan_location_lat: float
    scan_location_lng: float
    timestamp: datetime


class QRVerificationResponse(BaseModel):
    """Response after QR verification"""
    success: bool
    message: str
    qr_id: UUID
    load_id: UUID
    verification_type: str
    verified_at: Optional[datetime] = None
    next_step: Optional[str] = None


class LoadTrackingStatus(BaseModel):
    """Complete tracking status of a load"""
    load_id: UUID
    vendor_id: UUID
    driver_id: UUID
    receiver_id: Optional[UUID] = None
    status: str  # "assigned", "pickup_qr_generated", "picked_up", "delivery_qr_generated", "delivered"
    pickup_qr_id: Optional[UUID] = None
    delivery_qr_id: Optional[UUID] = None
    pickup_verified_at: Optional[datetime] = None
    delivery_verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ReceiverCreate(BaseModel):
    """Create a new receiver"""
    name: str
    email: str
    phone: str
    location_lat: float
    location_lng: float
    location_address: str
    company_name: Optional[str] = None


class ReceiverResponse(BaseModel):
    """Receiver details"""
    receiver_id: UUID
    name: str
    email: str
    phone: str
    location_lat: float
    location_lng: float
    location_address: str
    company_name: Optional[str]
    created_at: datetime


class NotificationEvent(BaseModel):
    """Notification event for AI agent processing"""
    event_id: UUID
    event_type: str  # "qr_generated", "pickup_verified", "delivery_verified", "anomaly_detected"
    load_id: UUID
    vendor_id: UUID
    driver_id: UUID
    receiver_id: Optional[UUID] = None
    message: str
    priority: str = "normal"  # "low", "normal", "high", "critical"
    created_at: datetime
    processed: bool = False
