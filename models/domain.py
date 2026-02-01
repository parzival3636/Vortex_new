from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class Coordinate(BaseModel):
    """Geographic coordinate with address"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    address: Optional[str] = Field(None, description="Human-readable address")


class TripCreate(BaseModel):
    """Request model for creating a trip"""
    driver_id: UUID
    truck_id: UUID
    origin: Coordinate
    destination: Coordinate
    outbound_load: str


class TripResponse(BaseModel):
    """Response model for trip data"""
    trip_id: UUID
    driver_id: UUID
    truck_id: UUID
    origin: Coordinate
    destination: Coordinate
    outbound_load: str
    is_deadheading: bool
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None


class LoadCreate(BaseModel):
    """Request model for creating a load posting"""
    vendor_id: UUID
    weight_kg: float = Field(..., gt=0, description="Load weight in kilograms")
    pickup_location: Coordinate
    destination: Coordinate
    price_offered: float = Field(..., gt=0, description="Price offered for transport")
    currency: str = Field(default="USD", description="Currency code")


class LoadResponse(BaseModel):
    """Response model for load data"""
    load_id: UUID
    vendor_id: UUID
    weight_kg: float
    pickup_location: Coordinate
    destination: Coordinate
    price_offered: float
    currency: str
    status: str
    assigned_driver_id: Optional[UUID] = None
    assigned_trip_id: Optional[UUID] = None
    created_at: datetime
    assigned_at: Optional[datetime] = None
    picked_up_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


class ProfitabilityCalculation(BaseModel):
    """Profitability calculation breakdown"""
    extra_distance_km: float
    fuel_cost: float
    time_cost: float
    net_profit: float
    profitability_score: float
    estimated_time_hours: float


class LoadOpportunity(BaseModel):
    """Load opportunity with profitability calculation"""
    load: LoadResponse
    calculation: ProfitabilityCalculation
    vendor_name: str
    rank: int


class FleetStatistics(BaseModel):
    """Fleet statistics for owner dashboard"""
    total_trucks: int
    trucks_loaded: int
    trucks_deadheading: int
    trucks_idle: int
    total_revenue: float
    total_fuel_savings: float
    deadheading_reduction_percent: float


class DriverRatingCreate(BaseModel):
    """Request model for creating a driver rating"""
    vendor_id: UUID
    driver_id: UUID
    load_id: UUID
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: Optional[str] = None


class DriverRatingResponse(BaseModel):
    """Response model for driver rating"""
    rating_id: UUID
    vendor_id: UUID
    driver_id: UUID
    load_id: UUID
    rating: int
    comment: Optional[str]
    created_at: datetime


# ==================== MANUAL ALLOCATION MODELS ====================

class OwnerStatistics(BaseModel):
    """Owner dashboard statistics"""
    totalActiveVehicles: int
    totalPendingLoads: int
    totalAllocatedLoads: int
    totalCompletedLoads: int
    allocationRate: float
    averageVehicleUtilization: float
    lastUpdated: datetime


class VehicleLocation(BaseModel):
    """Vehicle location information"""
    latitude: float
    longitude: float
    address: str


class VehicleInfo(BaseModel):
    """Vehicle information for allocation"""
    id: str
    name: str
    currentLocation: VehicleLocation
    status: str
    distanceToNearestLoad: float


class LoadInfo(BaseModel):
    """Load information for allocation"""
    id: str
    pickupLocation: Coordinate
    destination: Coordinate
    status: str
    specialInstructions: Optional[str] = None


class AllocationRequest(BaseModel):
    """Request to create an allocation"""
    vehicleId: str
    loadId: str
    ownerId: str


class AllocationRecord(BaseModel):
    """Allocation record response"""
    id: str
    vehicleId: str
    loadId: str
    status: str
    allocatedAt: datetime
    completedAt: Optional[datetime] = None
    cancelledAt: Optional[datetime] = None


class DriverAllocatedLoad(BaseModel):
    """Allocated load for driver"""
    id: str
    loadId: str
    pickupLocation: Coordinate
    destination: Coordinate
    status: str
    estimatedDistanceToPickup: float
    estimatedTimeToPickup: float
    totalEstimatedDistance: float
    totalEstimatedTime: float
    specialInstructions: Optional[str] = None


class DriverAllocatedLoadsSummary(BaseModel):
    """Summary of all allocated loads for a driver"""
    totalLoads: int
    totalDistance: float
    totalTime: float
    loads: list[DriverAllocatedLoad]


class NavigationState(BaseModel):
    """Navigation state for live map"""
    currentLocation: Coordinate
    pickupPoint: Coordinate
    destination: Coordinate
    route: dict
    nextWaypoint: str
    distanceToNextWaypoint: float
    timeToNextWaypoint: float


class LocationUpdate(BaseModel):
    """Location update from driver"""
    vehicleId: str
    latitude: float
    longitude: float
    accuracy: float


class Notification(BaseModel):
    """Notification for driver"""
    id: str
    driverId: str
    type: str
    title: str
    message: str
    loadId: Optional[str] = None
    waypointType: Optional[str] = None
    isRead: bool
    createdAt: datetime
