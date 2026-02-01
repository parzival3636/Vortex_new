# Design Document: Manual Vehicle-Load Allocation

## Overview

The Manual Vehicle-Load Allocation feature provides owners with a manual allocation interface to assign vehicles to loads based on vehicle location, and gives drivers visibility into their allocated loads with live navigation capabilities. The system maintains compatibility with the existing deadheading feature by preventing conflicts between manual allocations and automatic assignments.

The architecture consists of four main components:
1. **Owner Dashboard Statistics** - Real-time metrics display
2. **Manual Allocation Interface** - Vehicle-load matching UI
3. **Driver Allocated Loads Section** - Driver-facing load management
4. **Live Navigation Map** - Real-time route tracking and navigation

## Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
├─────────────────────────────────────────────────────────────┤
│  Owner Dashboard    │  Manual Allocation UI  │  Driver UI   │
│  - Statistics       │  - Vehicle List       │  - Loads List│
│  - Metrics Display  │  - Load List          │  - Navigation│
│                     │  - Allocation Logic   │  - Map View  │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│                    API Layer                                 │
├─────────────────────────────────────────────────────────────┤
│  - Allocation Service API                                   │
│  - Statistics Calculation API                               │
│  - Location Tracking API                                    │
│  - Notification Service API                                 │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│                  Business Logic Layer                        │
├─────────────────────────────────────────────────────────────┤
│  - Allocation Manager                                       │
│  - Statistics Calculator                                    │
│  - Location Service                                         │
│  - Deadheading Compatibility Manager                        │
│  - Notification Manager                                     │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│                   Data Layer                                 │
├─────────────────────────────────────────────────────────────┤
│  - Allocations Table                                        │
│  - Vehicles Table (existing)                                │
│  - Loads Table (existing)                                   │
│  - Location History Table                                   │
│  - Notifications Table                                      │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
Owner Allocation Flow:
1. Owner views Manual Allocation UI
2. System fetches unallocated loads and available vehicles
3. Owner selects vehicle → System highlights compatible loads
4. Owner selects load → System validates allocation
5. System creates allocation record
6. System notifies driver
7. Driver sees load in Allocated Loads section

Driver Navigation Flow:
1. Driver views Allocated Loads
2. Driver selects a load
3. System displays Live Navigation Map
4. System tracks driver location in real-time
5. System updates route and distance/time
6. Driver receives notifications at waypoints
7. Driver marks load as completed
```

## Components and Interfaces

### 1. Owner Dashboard Statistics Component

**Purpose**: Display real-time business metrics on the owner dashboard.

**Data Model**:
```
OwnerStatistics {
  totalActiveVehicles: number
  totalPendingLoads: number
  totalAllocatedLoads: number
  totalCompletedLoads: number
  allocationRate: number (0-100, percentage)
  averageVehicleUtilization: number (0-100, percentage)
  lastUpdated: timestamp
}
```

**Interface**:
```
GET /api/owner/statistics
Response: OwnerStatistics

Calculation Logic:
- totalActiveVehicles: COUNT(vehicles WHERE status = 'active')
- totalPendingLoads: COUNT(loads WHERE status = 'pending')
- totalAllocatedLoads: COUNT(allocations WHERE status = 'active')
- totalCompletedLoads: COUNT(loads WHERE status = 'completed')
- allocationRate: (totalAllocatedLoads / totalPendingLoads) * 100
- averageVehicleUtilization: SUM(vehicle_utilization) / totalActiveVehicles
```

**UI Requirements**:
- Display metrics in a card-based layout
- Format percentages with % symbol
- Format counts as integers
- Update statistics every 30 seconds
- Show last updated timestamp

### 2. Manual Allocation Interface Component

**Purpose**: Enable owners to manually assign vehicles to loads.

**Data Models**:
```
AllocationRequest {
  vehicleId: string
  loadId: string
  allocatedAt: timestamp
  allocatedBy: string (owner_id)
}

AllocationRecord {
  id: string
  vehicleId: string
  loadId: string
  status: 'active' | 'completed' | 'cancelled'
  allocatedAt: timestamp
  allocatedBy: string
  completedAt?: timestamp
  cancelledAt?: timestamp
  createdAt: timestamp
  updatedAt: timestamp
}

VehicleInfo {
  id: string
  name: string
  currentLocation: {
    latitude: number
    longitude: number
    address: string
  }
  status: 'available' | 'allocated' | 'deadheading'
  distanceToNearestLoad: number (in km)
}

LoadInfo {
  id: string
  pickupLocation: {
    latitude: number
    longitude: number
    address: string
  }
  destination: {
    latitude: number
    longitude: number
    address: string
  }
  status: 'pending' | 'allocated' | 'in_transit' | 'completed'
  specialInstructions?: string
}
```

**Interfaces**:
```
GET /api/allocations/available-vehicles
Response: VehicleInfo[]

GET /api/allocations/unallocated-loads
Response: LoadInfo[]

POST /api/allocations
Request: AllocationRequest
Response: AllocationRecord | Error

DELETE /api/allocations/:allocationId
Response: { success: boolean }

GET /api/allocations/compatible-loads?vehicleId=:vehicleId
Response: LoadInfo[] (sorted by distance)

GET /api/allocations/compatible-vehicles?loadId=:loadId
Response: VehicleInfo[] (sorted by distance)
```

**Validation Rules**:
- Vehicle must have status = 'available'
- Load must have status = 'pending'
- Vehicle location must be within 50km of load pickup location
- Vehicle must not be assigned by deadheading
- Load must not be assigned by deadheading

**UI Requirements**:
- Display unallocated loads in a list/table
- Display available vehicles in a list/table
- Show distance from vehicle to load pickup
- Highlight compatible loads when vehicle is selected
- Highlight compatible vehicles when load is selected
- Show error messages for failed allocations
- Provide cancel allocation functionality

### 3. Driver Allocated Loads Section Component

**Purpose**: Display all loads allocated to a driver.

**Data Models**:
```
DriverAllocatedLoad {
  id: string
  loadId: string
  pickupLocation: {
    latitude: number
    longitude: number
    address: string
  }
  destination: {
    latitude: number
    longitude: number
    address: string
  }
  status: 'allocated' | 'picked_up' | 'in_transit' | 'completed'
  estimatedDistanceToPickup: number (in km)
  estimatedTimeToPickup: number (in minutes)
  totalEstimatedDistance: number (in km)
  totalEstimatedTime: number (in minutes)
  specialInstructions?: string
}

DriverAllocatedLoadsSummary {
  totalLoads: number
  totalDistance: number (in km)
  totalTime: number (in minutes)
  loads: DriverAllocatedLoad[]
}
```

**Interfaces**:
```
GET /api/driver/allocated-loads
Response: DriverAllocatedLoadsSummary

POST /api/driver/allocated-loads/:loadId/pickup
Response: { success: boolean }

POST /api/driver/allocated-loads/:loadId/complete
Response: { success: boolean }

GET /api/driver/allocated-loads/:loadId/details
Response: DriverAllocatedLoad
```

**UI Requirements**:
- Add "Allocated Loads" section to driver navbar
- Display all allocated loads with pickup and destination
- Show estimated distance and time to pickup
- Show total distance and time for all loads
- Display "No active loads" message when empty
- Allow driver to select a load to view details
- Allow driver to mark load as picked up
- Allow driver to mark load as completed
- Show notification badge for unread notifications

### 4. Live Navigation Map Component

**Purpose**: Provide real-time route tracking and navigation for drivers.

**Data Models**:
```
NavigationState {
  currentLocation: {
    latitude: number
    longitude: number
    accuracy: number (in meters)
    timestamp: timestamp
  }
  pickupPoint: {
    latitude: number
    longitude: number
    address: string
  }
  destination: {
    latitude: number
    longitude: number
    address: string
  }
  route: {
    waypoints: Array<{latitude, longitude}>
    totalDistance: number (in km)
    totalTime: number (in minutes)
  }
  nextWaypoint: 'pickup' | 'destination'
  distanceToNextWaypoint: number (in km)
  timeToNextWaypoint: number (in minutes)
}

LocationUpdate {
  latitude: number
  longitude: number
  accuracy: number
  timestamp: timestamp
}
```

**Interfaces**:
```
GET /api/navigation/route?currentLat=:lat&currentLng=:lng&pickupLat=:lat&pickupLng=:lng&destLat=:lat&destLng=:lng
Response: NavigationState

POST /api/navigation/location-update
Request: LocationUpdate
Response: { success: boolean }

GET /api/navigation/current-location
Response: LocationUpdate

POST /api/navigation/waypoint-reached?waypointType=:type
Response: { success: boolean, notification: Notification }
```

**Real-time Updates**:
- Location updates via WebSocket or polling (every 30 seconds minimum)
- Route recalculation on significant location changes
- Distance and time updates with each location change
- Waypoint notifications when driver reaches pickup or destination

**UI Requirements**:
- Display interactive map with current location marker
- Show pickup point marker
- Show destination marker
- Draw route from current → pickup → destination
- Display current distance and time to next waypoint
- Display total distance and time
- Update location marker in real-time
- Provide visual/audio notifications at waypoints
- Allow driver to complete load from map view

### 5. Notification System Component

**Purpose**: Send real-time notifications to drivers about allocations and waypoints.

**Data Models**:
```
Notification {
  id: string
  driverId: string
  type: 'allocation' | 'waypoint' | 'completion'
  title: string
  message: string
  loadDetails?: {
    loadId: string
    pickupAddress: string
    destinationAddress: string
    specialInstructions?: string
  }
  waypointType?: 'pickup' | 'destination'
  isRead: boolean
  createdAt: timestamp
}
```

**Interfaces**:
```
POST /api/notifications/send
Request: Notification
Response: { success: boolean }

GET /api/notifications/unread-count
Response: { count: number }

POST /api/notifications/:notificationId/read
Response: { success: boolean }

GET /api/notifications
Response: Notification[]
```

**Notification Types**:
- **Allocation**: "New load allocated - Pickup at [address]"
- **Pickup Waypoint**: "You've reached the pickup point"
- **Destination Waypoint**: "You've reached the destination"

### 6. Deadheading Compatibility Manager

**Purpose**: Ensure manual allocations don't conflict with deadheading assignments.

**Logic**:
```
When displaying available vehicles:
- Exclude vehicles with status = 'deadheading'

When displaying unallocated loads:
- Exclude loads with status = 'deadheading'

When creating allocation:
- Verify vehicle is not assigned by deadheading
- Verify load is not assigned by deadheading

When cancelling allocation:
- Set vehicle status back to 'available'
- Set load status back to 'pending'
- Allow deadheading to consider these again
```

## Data Models

### Database Schema

```sql
-- Allocations Table
CREATE TABLE allocations (
  id UUID PRIMARY KEY,
  vehicle_id UUID NOT NULL REFERENCES vehicles(id),
  load_id UUID NOT NULL REFERENCES loads(id),
  status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
  allocated_at TIMESTAMP NOT NULL,
  allocated_by UUID NOT NULL REFERENCES owners(id),
  completed_at TIMESTAMP,
  cancelled_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(load_id) -- Each load can only be allocated once
);

-- Location History Table
CREATE TABLE location_history (
  id UUID PRIMARY KEY,
  vehicle_id UUID NOT NULL REFERENCES vehicles(id),
  latitude DECIMAL(10, 8) NOT NULL,
  longitude DECIMAL(11, 8) NOT NULL,
  accuracy DECIMAL(5, 2) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications Table
CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  driver_id UUID NOT NULL REFERENCES drivers(id),
  type ENUM('allocation', 'waypoint', 'completion') NOT NULL,
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  load_id UUID REFERENCES loads(id),
  waypoint_type ENUM('pickup', 'destination'),
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_allocations_vehicle_id ON allocations(vehicle_id);
CREATE INDEX idx_allocations_load_id ON allocations(load_id);
CREATE INDEX idx_allocations_status ON allocations(status);
CREATE INDEX idx_location_history_vehicle_id ON location_history(vehicle_id);
CREATE INDEX idx_location_history_recorded_at ON location_history(recorded_at);
CREATE INDEX idx_notifications_driver_id ON notifications(driver_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
```

### Existing Tables (No Modifications)

The design maintains compatibility with existing tables:
- `vehicles` - No changes
- `loads` - No changes
- `drivers` - No changes
- `owners` - No changes

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Dashboard Statistics Accuracy

*For any* set of vehicles, loads, and allocations in the system, the displayed statistics should match the actual counts and calculations from the database.

**Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**

### Property 2: Vehicle-Load Compatibility Filtering

*For any* vehicle and load pair, if the vehicle location is more than 50km from the load pickup location, the allocation should be rejected with a distance validation error.

**Validates: Requirements 2.8**

### Property 3: Allocation State Consistency

*For any* allocation, after creation, the vehicle status should be 'allocated' and the load status should be 'allocated', and these statuses should persist until the allocation is completed or cancelled.

**Validates: Requirements 2.9, 5.1**

### Property 4: Allocation Persistence Round Trip

*For any* allocation created in the system, if the system is restarted, querying the database should return the same allocation with all original data intact.

**Validates: Requirements 5.1, 5.4**

### Property 5: Deadheading Exclusion

*For any* vehicle assigned by deadheading, that vehicle should not appear in the list of available vehicles for manual allocation.

**Validates: Requirements 6.1, 6.4**

### Property 6: Deadheading Load Exclusion

*For any* load assigned by deadheading, that load should not appear in the list of unallocated loads for manual allocation.

**Validates: Requirements 6.2, 6.5**

### Property 7: Allocation Cancellation Reversion

*For any* active allocation, after cancellation, the vehicle status should revert to 'available' and the load status should revert to 'pending'.

**Validates: Requirements 2.12, 6.3**

### Property 8: Driver Allocated Loads Completeness

*For any* driver, the Allocated Loads section should display all loads with status 'allocated' or 'picked_up' that are assigned to that driver.

**Validates: Requirements 3.2**

### Property 9: Allocated Load Information Completeness

*For any* allocated load displayed to a driver, the display should include pickup location, destination, status, estimated distance to pickup, and estimated time to pickup.

**Validates: Requirements 3.3, 3.4**

### Property 10: Navigation Route Correctness

*For any* navigation route displayed, the route should contain exactly three waypoints in order: current location, pickup point, destination.

**Validates: Requirements 4.5**

### Property 11: Location Update Frequency

*For any* active navigation session, location updates should occur at least every 30 seconds, and the displayed location should be within 10 meters of the actual GPS position.

**Validates: Requirements 4.12, 4.11**

### Property 12: Waypoint Notification Triggering

*For any* driver location update, if the driver is within 100 meters of the pickup point and hasn't been notified yet, a pickup waypoint notification should be sent.

**Validates: Requirements 4.8**

### Property 13: Notification Inclusion

*For any* allocation notification sent to a driver, the notification should include the load's pickup location, destination, and any special instructions.

**Validates: Requirements 7.2**

### Property 14: Notification Persistence

*For any* notification created in the system, if the system is restarted, querying the notifications table should return the same notification with all original data intact.

**Validates: Requirements 7.3**

### Property 15: Unread Notification Badge

*For any* driver with unread notifications, the Allocated Loads navbar item should display a badge indicating the count of unread notifications.

**Validates: Requirements 7.5**

## Error Handling

### Allocation Errors

**Invalid Vehicle State**:
- Error: "Vehicle is not available for allocation"
- Cause: Vehicle status is not 'available'
- Recovery: Display available vehicles only

**Invalid Load State**:
- Error: "Load is not available for allocation"
- Cause: Load status is not 'pending'
- Recovery: Display unallocated loads only

**Distance Validation Failed**:
- Error: "Vehicle is too far from pickup location (distance: Xkm, max: 50km)"
- Cause: Vehicle location > 50km from load pickup
- Recovery: Suggest closer vehicles or loads

**Deadheading Conflict**:
- Error: "Vehicle/Load is already assigned by deadheading system"
- Cause: Vehicle or load has deadheading assignment
- Recovery: Exclude from available lists

### Location Tracking Errors

**GPS Accuracy Below Threshold**:
- Warning: "GPS accuracy is low (Xm), navigation may be inaccurate"
- Cause: GPS accuracy > 10 meters
- Recovery: Continue with warning, retry location update

**Location Update Timeout**:
- Error: "Location update failed, retrying..."
- Cause: Location service unavailable
- Recovery: Retry with exponential backoff

### Notification Errors

**Notification Delivery Failed**:
- Error: "Failed to send notification to driver"
- Cause: WebSocket or API connection issue
- Recovery: Queue notification for retry

## Testing Strategy

### Unit Testing

Unit tests verify specific examples, edge cases, and error conditions:

**Owner Dashboard Statistics**:
- Test statistics calculation with various vehicle/load combinations
- Test formatting of percentages and counts
- Test edge case: zero vehicles or loads
- Test edge case: 100% allocation rate

**Manual Allocation**:
- Test allocation creation with valid inputs
- Test allocation rejection with invalid vehicle state
- Test allocation rejection with invalid load state
- Test allocation rejection with distance validation failure
- Test allocation cancellation
- Test error message display

**Driver Allocated Loads**:
- Test display of allocated loads for a driver
- Test "no loads" message when driver has no allocations
- Test load status transitions (allocated → picked_up → completed)
- Test distance and time calculations

**Live Navigation**:
- Test route generation with valid coordinates
- Test location marker updates
- Test waypoint notification triggering
- Test GPS accuracy validation

### Property-Based Testing

Property-based tests verify universal properties across all inputs using randomization:

**Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with feature name and property number
- Tag format: `Feature: manual-vehicle-load-allocation, Property N: [property_text]`

**Property Test Examples**:

```javascript
// Property 1: Dashboard Statistics Accuracy
// Feature: manual-vehicle-load-allocation, Property 1: Dashboard Statistics Accuracy
test('statistics should match database counts', () => {
  fc.assert(
    fc.property(
      fc.array(vehicleArbitrary()),
      fc.array(loadArbitrary()),
      fc.array(allocationArbitrary()),
      (vehicles, loads, allocations) => {
        const stats = calculateStatistics(vehicles, loads, allocations);
        expect(stats.totalActiveVehicles).toBe(
          vehicles.filter(v => v.status === 'active').length
        );
        expect(stats.totalPendingLoads).toBe(
          loads.filter(l => l.status === 'pending').length
        );
        // ... more assertions
      }
    ),
    { numRuns: 100 }
  );
});

// Property 3: Allocation State Consistency
// Feature: manual-vehicle-load-allocation, Property 3: Allocation State Consistency
test('allocation should update vehicle and load status', () => {
  fc.assert(
    fc.property(
      vehicleArbitrary(),
      loadArbitrary(),
      (vehicle, load) => {
        const allocation = createAllocation(vehicle.id, load.id);
        const updatedVehicle = getVehicle(vehicle.id);
        const updatedLoad = getLoad(load.id);
        
        expect(updatedVehicle.status).toBe('allocated');
        expect(updatedLoad.status).toBe('allocated');
      }
    ),
    { numRuns: 100 }
  );
});

// Property 5: Deadheading Exclusion
// Feature: manual-vehicle-load-allocation, Property 5: Deadheading Exclusion
test('deadheading vehicles should not appear in available list', () => {
  fc.assert(
    fc.property(
      fc.array(vehicleArbitrary()),
      (vehicles) => {
        const deadheadingVehicles = vehicles.filter(v => v.status === 'deadheading');
        const availableVehicles = getAvailableVehicles();
        
        deadheadingVehicles.forEach(dv => {
          expect(availableVehicles.find(av => av.id === dv.id)).toBeUndefined();
        });
      }
    ),
    { numRuns: 100 }
  );
});
```

### Integration Testing

Integration tests verify end-to-end flows:

- Owner allocates vehicle to load → Driver receives notification → Driver sees load in Allocated Loads
- Driver selects load → Navigation map displays → Location updates in real-time
- Driver marks load as picked up → Status updates → Navigation switches to destination
- Driver marks load as completed → Load removed from active list → Next load ready

