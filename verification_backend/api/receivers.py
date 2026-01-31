"""
API endpoints for receiver management
"""
from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List

try:
    from verification_backend.db_verification import verification_db
    from verification_backend.models.verification_models import ReceiverCreate, ReceiverResponse
except ImportError:
    try:
        from verification_backend.db_verification_simple import verification_db
        from verification_backend.models.verification_models import ReceiverCreate, ReceiverResponse
    except ImportError:
        from db_verification_simple import verification_db
        from models.verification_models import ReceiverCreate, ReceiverResponse

router = APIRouter(prefix="/api/v1/receivers", tags=["receivers"])


@router.post("/", response_model=ReceiverResponse, status_code=status.HTTP_201_CREATED)
def create_receiver(receiver_data: ReceiverCreate):
    """Create a new receiver"""
    receiver = verification_db.create_receiver(
        name=receiver_data.name,
        email=receiver_data.email,
        phone=receiver_data.phone,
        location_lat=receiver_data.location_lat,
        location_lng=receiver_data.location_lng,
        location_address=receiver_data.location_address,
        company_name=receiver_data.company_name
    )
    
    return ReceiverResponse(
        receiver_id=UUID(receiver["receiver_id"]),
        name=receiver["name"],
        email=receiver["email"],
        phone=receiver["phone"],
        location_lat=receiver["location_lat"],
        location_lng=receiver["location_lng"],
        location_address=receiver["location_address"],
        company_name=receiver["company_name"] if receiver["company_name"] else None,
        created_at=receiver["created_at"]
    )


@router.get("/", response_model=List[ReceiverResponse])
def get_all_receivers():
    """Get all receivers"""
    receivers = verification_db.get_all_receivers()
    
    return [
        ReceiverResponse(
            receiver_id=UUID(r["receiver_id"]),
            name=r["name"],
            email=r["email"],
            phone=r["phone"],
            location_lat=r["location_lat"],
            location_lng=r["location_lng"],
            location_address=r["location_address"],
            company_name=r["company_name"] if r["company_name"] else None,
            created_at=r["created_at"]
        )
        for r in receivers
    ]


@router.get("/{receiver_id}", response_model=ReceiverResponse)
def get_receiver(receiver_id: UUID):
    """Get receiver by ID"""
    receiver = verification_db.get_receiver(str(receiver_id))
    
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver with ID {receiver_id} not found"
        )
    
    return ReceiverResponse(
        receiver_id=UUID(receiver["receiver_id"]),
        name=receiver["name"],
        email=receiver["email"],
        phone=receiver["phone"],
        location_lat=receiver["location_lat"],
        location_lng=receiver["location_lng"],
        location_address=receiver["location_address"],
        company_name=receiver["company_name"] if receiver["company_name"] else None,
        created_at=receiver["created_at"]
    )


@router.get("/{receiver_id}/notifications")
def get_receiver_notifications(receiver_id: UUID, unread_only: bool = False):
    """Get notifications for a receiver"""
    notifications = verification_db.get_notifications_for_recipient(
        recipient_id=str(receiver_id),
        unread_only=unread_only
    )
    
    return {
        "receiver_id": str(receiver_id),
        "total_notifications": len(notifications),
        "notifications": notifications
    }


@router.patch("/{receiver_id}/notifications/{notification_id}/read")
def mark_notification_read(receiver_id: UUID, notification_id: UUID):
    """Mark notification as read"""
    success = verification_db.mark_notification_read(str(notification_id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return {"message": "Notification marked as read"}
