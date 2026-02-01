# Implementation Plan: Manual Vehicle-Load Allocation

## Overview

This implementation plan breaks down the Manual Vehicle-Load Allocation feature into discrete coding tasks for a Python/FastAPI backend. The tasks are organized to build incrementally, starting with database schema and core models, then implementing business logic, APIs, and finally integrating with the frontend. All tasks maintain compatibility with the existing deadheading feature.

## Tasks

- [ ] 1. Set up database schema and models
  - [ ] 1.1 Create allocations table migration
    - Add allocations table with vehicle_id, load_id, status, timestamps, and audit fields
    - Add unique constraint on load_id
    - Add indexes on vehicle_id, load_id, and status
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ] 1.2 Create location_history table migration
    - Add location_history table with vehicle_id, latitude, longitude, accuracy, recorded_at
    - Add indexes on vehicle_id and recorded_at
    - _Requirements: 4.11, 4.12_
  
  - [ ] 1.3 Create notifications table migration
    - Add notifications table with driver_id, type, title, message, load_id, is_read
    - Add indexes on driver_id and is_read
    - _Requirements: 7.1, 7.3_
  
  - [ ] 1.4 Create SQLAlchemy models for allocations, location_history, and notifications
    - Define Allocation, LocationHistory, and Notification models
    - Add relationships to existing Vehicle, Load, and Driver models
    - _Requirements: 5.1, 5.2, 5.3_

- [ ] 2. Implement owner statistics calculation service
  - [ ] 2.1 Create StatisticsService class with calculation methods
    - Implement get_total_active_vehicles()
    - Implement get_total_pending_loads()
    - Implement get_total_allocated_loads()
    - Implement get_total_completed_loads()
    - Implement calculate_allocation_rate()
    - Implement calculate_average_vehicle_utilization()
    - _Requirements: 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_
  
  - [ ]* 2.2 Write property test for statistics accuracy
    - **Property 1: Dashboard Statistics Accuracy**
    - **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**
  
  - [ ] 2.3 Create GET /api/owner/statistics endpoint
    - Return OwnerStatistics with all calculated metrics
    - Format percentages and counts appropriately
    - Include lastUpdated timestamp
    - _Requirements: 1.1, 1.8_

- [ ] 3. Implement allocation validation and business logic
  - [ ] 3.1 Create AllocationValidator class
    - Implement validate_vehicle_available(vehicle_id)
    - Implement validate_load_unallocated(load_id)
    - Implement validate_distance(vehicle_location, load_pickup_location)
    - Implement validate_not_deadheading(vehicle_id, load_id)
    - Return detailed error messages for each validation failure
    - _Requirements: 2.7, 2.8, 6.1, 6.2_
  
  - [ ]* 3.2 Write property test for distance validation
    - **Property 2: Vehicle-Load Compatibility Filtering**
    - **Validates: Requirements 2.8**
  
  - [ ] 3.3 Create AllocationManager class
    - Implement create_allocation(vehicle_id, load_id, owner_id)
    - Implement cancel_allocation(allocation_id)
    - Update vehicle and load status on allocation/cancellation
    - Persist allocation records to database
    - _Requirements: 2.9, 2.12, 5.1, 5.2, 5.3_
  
  - [ ]* 3.4 Write property test for allocation state consistency
    - **Property 3: Allocation State Consistency**
    - **Validates: Requirements 2.9, 5.1**
  
  - [ ]* 3.5 Write property test for allocation persistence
    - **Property 4: Allocation Persistence Round Trip**
    - **Validates: Requirements 5.1, 5.4**

- [ ] 4. Implement deadheading compatibility logic
  - [ ] 4.1 Create DeadheadingCompatibilityManager class
    - Implement get_available_vehicles() excluding deadheading vehicles
    - Implement get_unallocated_loads() excluding deadheading loads
    - Implement is_vehicle_deadheading(vehicle_id)
    - Implement is_load_deadheading(load_id)
    - _Requirements: 6.1, 6.2, 6.4, 6.5_
  
  - [ ]* 4.2 Write property test for deadheading vehicle exclusion
    - **Property 5: Deadheading Exclusion**
    - **Validates: Requirements 6.1, 6.4**
  
  - [ ]* 4.3 Write property test for deadheading load exclusion
    - **Property 6: Deadheading Load Exclusion**
    - **Validates: Requirements 6.2, 6.5**
  
  - [ ]* 4.4 Write property test for allocation cancellation reversion
    - **Property 7: Allocation Cancellation Reversion**
    - **Validates: Requirements 2.12, 6.3**

- [ ] 5. Implement allocation API endpoints
  - [ ] 5.1 Create GET /api/allocations/available-vehicles endpoint
    - Return list of available vehicles with current location and distance to nearest load
    - Exclude deadheading vehicles
    - _Requirements: 2.2, 2.3, 6.4_
  
  - [ ] 5.2 Create GET /api/allocations/unallocated-loads endpoint
    - Return list of unallocated loads with pickup and destination
    - Exclude deadheading loads
    - _Requirements: 2.1, 2.4, 6.5_
  
  - [ ] 5.3 Create POST /api/allocations endpoint
    - Accept AllocationRequest with vehicleId and loadId
    - Validate allocation using AllocationValidator
    - Create allocation using AllocationManager
    - Return AllocationRecord or error response
    - _Requirements: 2.7, 2.8, 2.9_
  
  - [ ] 5.4 Create DELETE /api/allocations/:allocationId endpoint
    - Cancel allocation using AllocationManager
    - Revert vehicle and load status
    - _Requirements: 2.12_
  
  - [ ] 5.5 Create GET /api/allocations/compatible-loads?vehicleId=:vehicleId endpoint
    - Return loads compatible with vehicle, sorted by distance
    - _Requirements: 2.5_
  
  - [ ] 5.6 Create GET /api/allocations/compatible-vehicles?loadId=:loadId endpoint
    - Return vehicles compatible with load, sorted by distance
    - _Requirements: 2.6_

- [ ] 6. Implement notification system
  - [ ] 6.1 Create NotificationManager class
    - Implement send_allocation_notification(driver_id, load_id)
    - Implement send_waypoint_notification(driver_id, waypoint_type)
    - Include load details in allocation notifications
    - Persist notifications to database
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [ ]* 6.2 Write property test for notification inclusion
    - **Property 13: Notification Inclusion**
    - **Validates: Requirements 7.2**
  
  - [ ]* 6.3 Write property test for notification persistence
    - **Property 14: Notification Persistence**
    - **Validates: Requirements 7.3**
  
  - [ ] 6.4 Create POST /api/notifications/send endpoint
    - Accept notification request
    - Send via NotificationManager
    - Return success response
    - _Requirements: 7.1_
  
  - [ ] 6.5 Create GET /api/notifications/unread-count endpoint
    - Return count of unread notifications for driver
    - _Requirements: 7.5_
  
  - [ ] 6.6 Create POST /api/notifications/:notificationId/read endpoint
    - Mark notification as read
    - _Requirements: 7.4_
  
  - [ ] 6.7 Create GET /api/notifications endpoint
    - Return all notifications for driver
    - _Requirements: 7.3_

- [ ] 7. Implement driver allocated loads API
  - [ ] 7.1 Create DriverAllocatedLoadsService class
    - Implement get_allocated_loads(driver_id)
    - Implement calculate_distance_and_time(vehicle_location, pickup_location)
    - Implement get_load_details(load_id)
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6_
  
  - [ ]* 7.2 Write property test for allocated loads completeness
    - **Property 8: Driver Allocated Loads Completeness**
    - **Validates: Requirements 3.2**
  
  - [ ]* 7.3 Write property test for allocated load information completeness
    - **Property 9: Allocated Load Information Completeness**
    - **Validates: Requirements 3.3, 3.4**
  
  - [ ] 7.4 Create GET /api/driver/allocated-loads endpoint
    - Return DriverAllocatedLoadsSummary with all allocated loads
    - Include distance and time calculations
    - _Requirements: 3.2, 3.3, 3.4, 3.5_
  
  - [ ] 7.5 Create GET /api/driver/allocated-loads/:loadId/details endpoint
    - Return detailed information for a specific load
    - Include pickup address, destination, special instructions
    - _Requirements: 3.6_
  
  - [ ] 7.6 Create POST /api/driver/allocated-loads/:loadId/pickup endpoint
    - Update load status to 'picked_up'
    - Trigger navigation to destination
    - _Requirements: 3.7_
  
  - [ ] 7.7 Create POST /api/driver/allocated-loads/:loadId/complete endpoint
    - Update load status to 'completed'
    - Remove from active allocated loads
    - _Requirements: 3.8_

- [ ] 8. Implement location tracking service
  - [ ] 8.1 Create LocationTrackingService class
    - Implement update_vehicle_location(vehicle_id, latitude, longitude, accuracy)
    - Implement get_current_location(vehicle_id)
    - Implement get_location_history(vehicle_id, time_range)
    - Persist location updates to location_history table
    - _Requirements: 4.6, 4.7, 4.11, 4.12_
  
  - [ ] 8.2 Create POST /api/navigation/location-update endpoint
    - Accept LocationUpdate with coordinates and accuracy
    - Update location using LocationTrackingService
    - Return success response
    - _Requirements: 4.6, 4.11, 4.12_
  
  - [ ] 8.3 Create GET /api/navigation/current-location endpoint
    - Return current location for vehicle
    - _Requirements: 4.2_

- [ ] 9. Implement navigation route service
  - [ ] 9.1 Create NavigationRouteService class
    - Implement calculate_route(current_location, pickup_location, destination_location)
    - Implement calculate_distance_and_time(from_location, to_location)
    - Return NavigationState with route, waypoints, and distance/time
    - _Requirements: 4.1, 4.5, 4.7_
  
  - [ ]* 9.2 Write property test for navigation route correctness
    - **Property 10: Navigation Route Correctness**
    - **Validates: Requirements 4.5**
  
  - [ ] 9.3 Create GET /api/navigation/route endpoint
    - Accept current, pickup, and destination coordinates
    - Calculate route using NavigationRouteService
    - Return NavigationState
    - _Requirements: 4.1, 4.5_

- [ ] 10. Implement waypoint detection and notifications
  - [ ] 10.1 Create WaypointDetectionService class
    - Implement check_waypoint_reached(current_location, waypoint_location, threshold=100m)
    - Implement trigger_waypoint_notification(driver_id, waypoint_type)
    - _Requirements: 4.8, 4.9, 4.12_
  
  - [ ]* 10.2 Write property test for waypoint notification triggering
    - **Property 12: Waypoint Notification Triggering**
    - **Validates: Requirements 4.8**
  
  - [ ] 10.3 Create POST /api/navigation/waypoint-reached endpoint
    - Accept waypointType parameter
    - Trigger notification using WaypointDetectionService
    - Return success response with notification
    - _Requirements: 4.8, 4.9_

- [ ] 11. Checkpoint - Ensure all backend tests pass
  - Ensure all unit tests and property tests pass
  - Verify all API endpoints are working correctly
  - Check database migrations are applied
  - Ask the user if questions arise

- [ ] 12. Integrate with frontend - Owner Dashboard Statistics
  - [ ] 12.1 Update owner dashboard component to fetch statistics
    - Call GET /api/owner/statistics endpoint
    - Display statistics in card-based layout
    - Update every 30 seconds
    - _Requirements: 1.1, 1.8_
  
  - [ ] 12.2 Add statistics formatting utilities
    - Format percentages with % symbol
    - Format counts as integers
    - Display last updated timestamp
    - _Requirements: 1.8_

- [ ] 13. Integrate with frontend - Manual Allocation UI
  - [ ] 13.1 Create manual allocation component
    - Display list of unallocated loads
    - Display list of available vehicles
    - Show distance from vehicle to load pickup
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [ ] 13.2 Implement vehicle selection and load highlighting
    - Highlight compatible loads when vehicle is selected
    - Sort loads by distance
    - _Requirements: 2.5_
  
  - [ ] 13.3 Implement load selection and vehicle highlighting
    - Highlight compatible vehicles when load is selected
    - Sort vehicles by distance
    - _Requirements: 2.6_
  
  - [ ] 13.4 Implement allocation creation
    - Call POST /api/allocations endpoint
    - Handle validation errors with user-friendly messages
    - _Requirements: 2.7, 2.8, 2.9, 2.11_
  
  - [ ] 13.5 Implement allocation cancellation
    - Call DELETE /api/allocations/:allocationId endpoint
    - Update UI after cancellation
    - _Requirements: 2.12_

- [ ] 14. Integrate with frontend - Driver Allocated Loads Section
  - [ ] 14.1 Add "Allocated Loads" navbar section to driver dashboard
    - Display in navbar with notification badge
    - _Requirements: 3.1, 7.5_
  
  - [ ] 14.2 Create allocated loads list component
    - Call GET /api/driver/allocated-loads endpoint
    - Display all allocated loads with pickup and destination
    - Show estimated distance and time to pickup
    - Show total distance and time
    - _Requirements: 3.2, 3.3, 3.4, 3.5_
  
  - [ ] 14.3 Implement "no loads" message
    - Display when driver has no allocated loads
    - _Requirements: 3.9_
  
  - [ ] 14.4 Implement load detail view
    - Call GET /api/driver/allocated-loads/:loadId/details endpoint
    - Display pickup address, destination, special instructions
    - _Requirements: 3.6_
  
  - [ ] 14.5 Implement pickup and completion actions
    - Call POST /api/driver/allocated-loads/:loadId/pickup endpoint
    - Call POST /api/driver/allocated-loads/:loadId/complete endpoint
    - Update UI after status changes
    - _Requirements: 3.7, 3.8_

- [ ] 15. Integrate with frontend - Live Navigation Map
  - [ ] 15.1 Create live navigation map component
    - Display interactive map with markers
    - Show current location, pickup point, destination
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [ ] 15.2 Implement route drawing
    - Call GET /api/navigation/route endpoint
    - Draw route from current → pickup → destination
    - _Requirements: 4.5_
  
  - [ ] 15.3 Implement real-time location updates
    - Poll GET /api/navigation/current-location every 30 seconds
    - Update location marker on map
    - _Requirements: 4.6, 4.12_
  
  - [ ] 15.4 Implement distance and time display
    - Call GET /api/navigation/route endpoint on location update
    - Display distance and time to next waypoint
    - Display total distance and time
    - _Requirements: 4.7_
  
  - [ ] 15.5 Implement waypoint notifications
    - Listen for waypoint notifications from backend
    - Display visual/audio notifications when reaching pickup or destination
    - _Requirements: 4.8, 4.9_
  
  - [ ] 15.6 Implement load completion from map
    - Allow driver to mark load as completed from map view
    - Clear route and prepare for next load
    - _Requirements: 4.10_

- [ ] 16. Integrate with frontend - Notifications
  - [ ] 16.1 Create notification center component
    - Display all notifications for driver
    - Show unread notification count
    - _Requirements: 7.3, 7.5_
  
  - [ ] 16.2 Implement notification read/dismiss
    - Call POST /api/notifications/:notificationId/read endpoint
    - Update badge count
    - _Requirements: 7.4, 7.5_
  
  - [ ] 16.3 Implement real-time notification delivery
    - Listen for allocation notifications
    - Display notification with load details
    - _Requirements: 7.1, 7.2_

- [ ] 17. Final checkpoint - Ensure all tests pass and integration complete
  - Ensure all unit tests and property tests pass
  - Verify all API endpoints are working correctly
  - Test end-to-end flows: allocation → notification → driver view → navigation
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- All code should be added to the vortexfinal backend folder
- Maintain compatibility with existing deadheading feature
- Use FastAPI for all new endpoints
- Use SQLAlchemy for all database operations
- Use Python type hints throughout

