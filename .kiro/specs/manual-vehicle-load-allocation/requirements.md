# Requirements Document: Manual Vehicle-Load Allocation

## Introduction

The Manual Vehicle-Load Allocation feature enables owners to manually assign vehicles to loads based on vehicle location, and provides drivers with visibility into their allocated loads and live navigation capabilities. This feature enhances the existing deadheading system by adding owner-controlled allocation logic and driver-facing load management with real-time route tracking.

## Glossary

- **Owner**: A business owner who manages vehicles and loads
- **Driver**: A truck driver who operates vehicles and completes loads
- **Vehicle**: A truck or transport vehicle with a current location
- **Load**: A shipment or cargo that needs to be transported from a pickup point to a destination
- **Allocation**: The assignment of a vehicle to a load
- **Deadheading**: The existing feature for automatic vehicle-load matching
- **Live Navigation**: Real-time route tracking from current location through pickup to destination
- **Vehicle Location**: The current GPS coordinates or location of a vehicle
- **Load Location**: The pickup point and destination coordinates of a load
- **Owner Dashboard**: The interface where owners view statistics and manage allocations
- **Driver Dashboard**: The interface where drivers view their allocated loads and navigate
- **Route**: The path from current vehicle location → pickup point → destination

## Requirements

### Requirement 1: Owner Dashboard Statistics

**User Story:** As an owner, I want to see my business statistics on the dashboard, so that I can monitor my fleet performance and business metrics.

#### Acceptance Criteria

1. WHEN an owner visits the dashboard THEN the system SHALL display a statistics section with relevant business metrics
2. WHEN the dashboard loads THEN the system SHALL calculate and display the total number of active vehicles
3. WHEN the dashboard loads THEN the system SHALL calculate and display the total number of pending loads
4. WHEN the dashboard loads THEN the system SHALL calculate and display the total number of allocated loads
5. WHEN the dashboard loads THEN the system SHALL calculate and display the total number of completed loads
6. WHEN the dashboard loads THEN the system SHALL calculate and display the allocation rate (allocated loads / total loads)
7. WHEN the dashboard loads THEN the system SHALL calculate and display the average vehicle utilization percentage
8. WHEN statistics are displayed THEN the system SHALL format all numeric metrics with appropriate units and precision

### Requirement 2: Manual Allocation Interface

**User Story:** As an owner, I want to manually assign vehicles to loads based on their current location, so that I can optimize vehicle-load matching according to my business logic.

#### Acceptance Criteria

1. WHEN an owner accesses the manual allocation section THEN the system SHALL display a list of unallocated loads
2. WHEN an owner accesses the manual allocation section THEN the system SHALL display a list of available vehicles with their current locations
3. WHEN displaying vehicles THEN the system SHALL show each vehicle's current location, status, and distance to the nearest unallocated load
4. WHEN displaying loads THEN the system SHALL show each load's pickup location, destination, and current status
5. WHEN an owner selects a vehicle THEN the system SHALL highlight compatible loads based on vehicle location proximity
6. WHEN an owner selects a load THEN the system SHALL highlight compatible vehicles based on their proximity to the load's pickup location
7. WHEN an owner initiates an allocation THEN the system SHALL validate that the vehicle is available and the load is unallocated
8. WHEN an owner initiates an allocation THEN the system SHALL validate that the vehicle location is within a reasonable distance of the load's pickup location
9. WHEN an allocation is valid THEN the system SHALL create the allocation record and update vehicle and load status
10. WHEN an allocation is created THEN the system SHALL notify the assigned driver of the new allocated load
11. WHEN an allocation fails validation THEN the system SHALL display a clear error message explaining the reason for failure
12. WHEN an owner cancels an allocation THEN the system SHALL revert the vehicle and load to available status

### Requirement 3: Allocated Loads Section in Driver Dashboard

**User Story:** As a driver, I want to see all loads allocated to me, so that I can manage my assigned work and plan my route.

#### Acceptance Criteria

1. WHEN a driver views their dashboard THEN the system SHALL display an "Allocated Loads" section in the navbar
2. WHEN a driver accesses the Allocated Loads section THEN the system SHALL display all loads currently allocated to that driver
3. WHEN displaying allocated loads THEN the system SHALL show each load's pickup location, destination, and current status
4. WHEN displaying allocated loads THEN the system SHALL show the estimated distance and time to the pickup point
5. WHEN displaying allocated loads THEN the system SHALL show the total estimated distance and time for all allocated loads
6. WHEN a driver selects an allocated load THEN the system SHALL display detailed information including pickup address, destination address, and special instructions
7. WHEN a driver marks a load as picked up THEN the system SHALL update the load status and begin navigation to the destination
8. WHEN a driver marks a load as completed THEN the system SHALL update the load status and remove it from active allocated loads
9. WHEN a driver has no allocated loads THEN the system SHALL display a message indicating no active loads

### Requirement 4: Live Navigation Map

**User Story:** As a driver, I want live navigation from my current location through pickup to destination, so that I can efficiently complete my assigned loads.

#### Acceptance Criteria

1. WHEN a driver selects an allocated load THEN the system SHALL display a live navigation map
2. WHEN the navigation map displays THEN the system SHALL show the driver's current location
3. WHEN the navigation map displays THEN the system SHALL show the pickup point location
4. WHEN the navigation map displays THEN the system SHALL show the destination location
5. WHEN the navigation map displays THEN the system SHALL draw the route from current location → pickup point → destination
6. WHEN the driver's location updates THEN the system SHALL update the current location marker on the map in real-time
7. WHEN the driver's location updates THEN the system SHALL recalculate and display the updated distance and time to the next waypoint
8. WHEN the driver reaches the pickup point THEN the system SHALL provide visual and/or audio notification
9. WHEN the driver reaches the destination THEN the system SHALL provide visual and/or audio notification
10. WHEN the driver completes a load THEN the system SHALL clear the current route and prepare for the next allocated load
11. WHEN the map is displayed THEN the system SHALL maintain accuracy within 10 meters of actual GPS position
12. WHEN the map is displayed THEN the system SHALL update location data at least every 30 seconds

### Requirement 5: Allocation Data Persistence

**User Story:** As a system, I want to persist all allocation data, so that allocations survive system restarts and can be audited.

#### Acceptance Criteria

1. WHEN an allocation is created THEN the system SHALL persist the allocation record to the database
2. WHEN an allocation is updated THEN the system SHALL persist the updated allocation record to the database
3. WHEN an allocation is cancelled THEN the system SHALL mark the allocation as cancelled in the database
4. WHEN the system restarts THEN the system SHALL restore all active allocations from the database
5. WHEN querying allocations THEN the system SHALL return allocations with complete audit information (created_at, updated_at, created_by)

### Requirement 6: Compatibility with Existing Deadheading Feature

**User Story:** As a system, I want manual allocation to coexist with the existing deadheading feature, so that owners can choose their allocation strategy.

#### Acceptance Criteria

1. WHEN a vehicle is manually allocated THEN the system SHALL prevent automatic deadheading assignment to that vehicle
2. WHEN a vehicle is manually allocated THEN the system SHALL not interfere with existing deadheading logic for other vehicles
3. WHEN an allocation is cancelled THEN the system SHALL allow the vehicle to be considered for deadheading again
4. WHEN displaying available vehicles THEN the system SHALL exclude vehicles already assigned by deadheading
5. WHEN displaying available loads THEN the system SHALL exclude loads already assigned by deadheading

### Requirement 7: Real-time Notifications

**User Story:** As a driver, I want to receive notifications about my allocated loads, so that I stay informed about my assignments.

#### Acceptance Criteria

1. WHEN an owner allocates a load to a driver THEN the system SHALL send a real-time notification to the driver
2. WHEN a notification is sent THEN the system SHALL include the load details (pickup location, destination, special instructions)
3. WHEN a driver receives a notification THEN the system SHALL display it in the driver's notification center
4. WHEN a driver dismisses a notification THEN the system SHALL mark it as read
5. WHEN a driver has unread notifications THEN the system SHALL display a notification badge on the Allocated Loads navbar item

