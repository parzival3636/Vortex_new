"""
API endpoints for QR code generation and verification
"""
from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from datetime import datetime

try:
    from verification_backend.db_verification import verification_db
    from verification_backend.agents.verification_agent import verification_agent
    from verification_backend.agents.notification_agent import notification_agent
    from verification_backend.models.verification_models import (
        QRVerificationRequest,
        QRVerificationResponse
    )
except ImportError:
    try:
        from verification_backend.db_verification_simple import verification_db
        from verification_backend.agents.verification_agent import verification_agent
        from verification_backend.agents.notification_agent import notification_agent
        from verification_backend.models.verification_models import (
            QRVerificationRequest,
            QRVerificationResponse
        )
    except ImportError:
        from db_verification_simple import verification_db
        from agents.verification_agent import verification_agent
        from agents.notification_agent import notification_agent
        from models.verification_models import (
            QRVerificationRequest,
            QRVerificationResponse
        )

router = APIRouter(prefix="/api/v1/qr", tags=["qr-verification"])


@router.post("/generate/pickup/{load_id}")
def generate_pickup_qr(
    load_id: UUID,
    driver_id: UUID,
    vendor_id: UUID,
    pickup_lat: float,
    pickup_lng: float
):
    """
    Generate QR code for pickup verification
    Called when driver is assigned to load
    """
    # Create QR code
    qr_data = verification_db.create_qr_code(
        qr_type="pickup",
        load_id=str(load_id),
        driver_id=str(driver_id),
        vendor_id=str(vendor_id),
        location_lat=pickup_lat,
        location_lng=pickup_lng,
        expiry_hours=24
    )
    
    # Send notifications via AI agent
    notification_agent.notify_qr_generated(
        load_id=str(load_id),
        qr_type="pickup",
        vendor_id=str(vendor_id),
        driver_id=str(driver_id)
    )
    
    return {
        "qr_id": qr_data["qr_id"],
        "qr_type": "pickup",
        "load_id": str(load_id),
        "expires_at": qr_data["expires_at"],
        "message": "Pickup QR code generated. Driver must scan at pickup location."
    }


@router.post("/generate/delivery/{load_id}")
def generate_delivery_qr(
    load_id: UUID,
    driver_id: UUID,
    vendor_id: UUID,
    receiver_id: UUID,
    delivery_lat: float,
    delivery_lng: float
):
    """
    Generate QR code for delivery verification
    Called after pickup is verified
    """
    # Verify pickup was completed first
    verifications = verification_db.get_verifications_for_load(str(load_id))
    pickup_verified = any(v['verification_type'] == 'pickup' and v['success'] 
                         for v in verifications)
    
    if not pickup_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot generate delivery QR before pickup verification"
        )
    
    # Create QR code
    qr_data = verification_db.create_qr_code(
        qr_type="delivery",
        load_id=str(load_id),
        driver_id=str(driver_id),
        vendor_id=str(vendor_id),
        receiver_id=str(receiver_id),
        location_lat=delivery_lat,
        location_lng=delivery_lng,
        expiry_hours=48
    )
    
    # Send notifications via AI agent
    notification_agent.notify_qr_generated(
        load_id=str(load_id),
        qr_type="delivery",
        vendor_id=str(vendor_id),
        driver_id=str(driver_id),
        receiver_id=str(receiver_id)
    )
    
    return {
        "qr_id": qr_data["qr_id"],
        "qr_type": "delivery",
        "load_id": str(load_id),
        "expires_at": qr_data["expires_at"],
        "message": "Delivery QR code generated. Receiver must scan upon delivery."
    }


@router.post("/verify/pickup", response_model=QRVerificationResponse)
def verify_pickup(request: QRVerificationRequest):
    """
    Verify driver scanning QR at pickup location
    """
    # Get QR code data
    qr_data = verification_db.get_qr_code(str(request.qr_id))
    if not qr_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR code not found"
        )
    
    if qr_data["qr_type"] != "pickup":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This QR code is not for pickup verification"
        )
    
    # Get load assignment from main database (would integrate with main system)
    load_assignment = {
        "assigned_driver_id": qr_data["driver_id"],
        "vendor_id": qr_data["vendor_id"]
    }
    
    # Use AI agent to verify
    scan_location = (request.scan_location_lat, request.scan_location_lng)
    verification_result = verification_agent.verify_pickup_scan(
        qr_data=qr_data,
        scanned_by_id=str(request.scanned_by_id),
        scan_location=scan_location,
        load_assignment=load_assignment
    )
    
    # Record verification event
    verification_db.create_verification_event(
        qr_id=str(request.qr_id),
        load_id=qr_data["load_id"],
        verification_type="pickup",
        scanned_by_id=str(request.scanned_by_id),
        scanned_by_type=request.scanned_by_type,
        success=verification_result["success"],
        message=verification_result["message"],
        confidence_score=verification_result.get("confidence_score", 0.0),
        anomalies=verification_result.get("anomalies", []),
        scan_location_lat=request.scan_location_lat,
        scan_location_lng=request.scan_location_lng
    )
    
    if verification_result["success"]:
        # Mark QR as used
        verification_db.mark_qr_used(str(request.qr_id))
        
        # Send success notifications
        notification_agent.notify_pickup_verified(
            load_id=qr_data["load_id"],
            vendor_id=qr_data["vendor_id"],
            driver_id=qr_data["driver_id"],
            verification_details=verification_result
        )
        
        return QRVerificationResponse(
            success=True,
            message=verification_result["message"],
            qr_id=request.qr_id,
            load_id=UUID(qr_data["load_id"]),
            verification_type="pickup",
            verified_at=datetime.fromisoformat(verification_result["verified_at"]),
            next_step="Proceed to delivery location. Delivery QR will be generated."
        )
    else:
        # Send anomaly alert
        notification_agent.notify_anomaly_detected(
            load_id=qr_data["load_id"],
            vendor_id=qr_data["vendor_id"],
            anomaly_type="pickup_verification_failed",
            details=verification_result
        )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=verification_result["message"]
        )


@router.post("/verify/delivery", response_model=QRVerificationResponse)
def verify_delivery(request: QRVerificationRequest):
    """
    Verify receiver scanning QR at delivery location
    """
    # Get QR code data
    qr_data = verification_db.get_qr_code(str(request.qr_id))
    if not qr_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR code not found"
        )
    
    if qr_data["qr_type"] != "delivery":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This QR code is not for delivery verification"
        )
    
    # Get load assignment and pickup verification
    verifications = verification_db.get_verifications_for_load(qr_data["load_id"])
    pickup_verification = next((v for v in verifications 
                               if v['verification_type'] == 'pickup' and v['success']), None)
    
    if not pickup_verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pickup must be verified before delivery"
        )
    
    load_assignment = {
        "assigned_driver_id": qr_data["driver_id"],
        "vendor_id": qr_data["vendor_id"],
        "receiver_id": qr_data["receiver_id"],
        "pickup_verified_at": pickup_verification["verified_at"]
    }
    
    # Use AI agent to verify
    scan_location = (request.scan_location_lat, request.scan_location_lng)
    verification_result = verification_agent.verify_delivery_scan(
        qr_data=qr_data,
        scanned_by_receiver_id=str(request.scanned_by_id),
        scan_location=scan_location,
        load_assignment=load_assignment,
        driver_id=qr_data["driver_id"]
    )
    
    # Record verification event
    verification_db.create_verification_event(
        qr_id=str(request.qr_id),
        load_id=qr_data["load_id"],
        verification_type="delivery",
        scanned_by_id=str(request.scanned_by_id),
        scanned_by_type=request.scanned_by_type,
        success=verification_result["success"],
        message=verification_result["message"],
        confidence_score=verification_result.get("confidence_score", 0.0),
        anomalies=verification_result.get("anomalies", []),
        scan_location_lat=request.scan_location_lat,
        scan_location_lng=request.scan_location_lng
    )
    
    if verification_result["success"]:
        # Mark QR as used
        verification_db.mark_qr_used(str(request.qr_id))
        
        # Send success notifications to all parties
        notification_agent.notify_delivery_verified(
            load_id=qr_data["load_id"],
            vendor_id=qr_data["vendor_id"],
            driver_id=qr_data["driver_id"],
            receiver_id=qr_data["receiver_id"],
            verification_details=verification_result
        )
        
        return QRVerificationResponse(
            success=True,
            message=verification_result["message"],
            qr_id=request.qr_id,
            load_id=UUID(qr_data["load_id"]),
            verification_type="delivery",
            verified_at=datetime.fromisoformat(verification_result["verified_at"]),
            next_step="Load delivery complete. Payment processing initiated."
        )
    else:
        # Send anomaly alert
        notification_agent.notify_anomaly_detected(
            load_id=qr_data["load_id"],
            vendor_id=qr_data["vendor_id"],
            anomaly_type="delivery_verification_failed",
            details=verification_result
        )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=verification_result["message"]
        )


@router.get("/load/{load_id}/status")
def get_load_verification_status(load_id: UUID):
    """Get complete verification status for a load"""
    qr_codes = verification_db.get_qr_codes_for_load(str(load_id))
    verifications = verification_db.get_verifications_for_load(str(load_id))
    
    pickup_qr = next((qr for qr in qr_codes if qr['qr_type'] == 'pickup'), None)
    delivery_qr = next((qr for qr in qr_codes if qr['qr_type'] == 'delivery'), None)
    
    pickup_verified = any(v['verification_type'] == 'pickup' and v['success'] 
                         for v in verifications)
    delivery_verified = any(v['verification_type'] == 'delivery' and v['success'] 
                           for v in verifications)
    
    # Determine status
    if delivery_verified:
        status = "delivered"
    elif pickup_verified:
        status = "in_transit"
    elif pickup_qr:
        status = "awaiting_pickup"
    else:
        status = "assigned"
    
    return {
        "load_id": str(load_id),
        "status": status,
        "pickup_qr_generated": pickup_qr is not None,
        "pickup_verified": pickup_verified,
        "delivery_qr_generated": delivery_qr is not None,
        "delivery_verified": delivery_verified,
        "qr_codes": qr_codes,
        "verifications": verifications
    }
