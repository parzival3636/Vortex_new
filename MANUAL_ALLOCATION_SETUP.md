# Manual Allocation Feature - Setup & Testing Guide

## What Was Added

### ✅ Owner Dashboard
- **New Tab**: "Manual Allocation" (between Fleet Management and Financial Reports)
- **Features**:
  - Real-time statistics (6 metric cards)
  - Available vehicles list with current locations
  - Unallocated loads list
  - Smart compatibility highlighting
  - One-click allocation
  - Distance validation (500km max)

### ✅ Driver Dashboard
- **New Tab**: "Allocated Loads" (next to Deadheading Loads)
- **Features**:
  - Summary cards (total loads, distance, time)
  - Allocated loads list
  - Distance and time estimates
  - Mark pickup/complete actions
  - Navigate to load

## How to Test

### 1. Start the Backend
```bash
# Make sure you're in the project root
python main.py
```

Backend should start on `http://localhost:8000`

### 2. Test Backend APIs (Optional)
```bash
python test_manual_allocation.py
```

This will test all 6 main endpoints:
- Owner statistics
- Available vehicles
- Unallocated loads
- Driver allocated loads
- Notifications
- Unread count

### 3. Start the Frontend
```bash
cd frontend
npm run dev
```

Frontend should start on `http://localhost:5173`

### 4. Test Owner Dashboard

1. **Open Owner Dashboard**: Click "Owner Dashboard" from landing page
2. **Click "Manual Allocation" tab** (middle tab)
3. **You should see**:
   - 6 statistics cards at the top
   - Left panel: Available vehicles list
   - Right panel: Unallocated loads list

4. **Test Allocation**:
   - Click on a vehicle (it will highlight in blue)
   - Compatible loads will highlight in green
   - Click on a compatible load
   - Click "Allocate" button
   - You should see success message

### 5. Test Driver Dashboard

1. **Open Driver Dashboard**: Click "Driver Dashboard" from landing page
2. **Click "Allocated Loads" tab** (second tab)
3. **You should see**:
   - 3 summary cards (total loads, distance, time)
   - List of allocated loads (if any)
   - Each load shows pickup/destination
   - Distance and time estimates

4. **Test Actions**:
   - Click "Navigate" to start navigation
   - Click "Mark Picked Up" to update status
   - Click "Complete" to finish load

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'services.allocation_service'`
**Solution**: Make sure all new service files are created:
- `services/allocation_service.py`
- `services/driver_loads_service.py`
- `services/navigation_service.py`
- `api/allocations.py`

**Problem**: API returns 500 error
**Solution**: Check backend console for error details. Most likely:
- Database collection not initialized
- Missing imports in `main.py`

### Frontend Issues

**Problem**: "Manual Allocation" tab not showing
**Solution**: 
- Clear browser cache
- Check browser console for errors
- Make sure `OwnerStatistics.jsx` and `ManualAllocation.jsx` exist in `frontend/src/components/`

**Problem**: Components not loading
**Solution**:
```bash
cd frontend
npm install axios react-hot-toast
npm run dev
```

**Problem**: CORS errors
**Solution**: Backend already has CORS enabled. If still seeing errors:
- Restart backend
- Check backend is running on port 8000
- Check frontend is calling `http://localhost:8000`

## Demo Data

### To Add Test Data

If you don't see any vehicles or loads, you need to add demo data:

```python
# Run this in Python console or create a script
from db_chromadb import db

# Create owner
owner = db.create_owner("Demo Owner", "owner@demo.com")

# Create truck
truck = db.create_truck(owner['owner_id'], "DL-01-AB-1234")

# Create driver
driver = db.create_driver("Demo Driver", "+91-9876543210", truck['truck_id'])

# Create vendor
vendor = db.create_vendor("Demo Vendor", "vendor@demo.com", "+91-9876543210", 28.6139, 77.2090)

# Create load
load = db.create_load(
    vendor_id=vendor['vendor_id'],
    weight_kg=5000,
    pickup_lat=28.6139,
    pickup_lng=77.2090,
    pickup_address="Delhi, India",
    destination_lat=26.9124,
    destination_lng=75.7873,
    destination_address="Jaipur, India",
    price_offered=15000,
    currency="INR"
)

# Add vehicle location
db.add_location_update(truck['truck_id'], 28.6139, 77.2090, 10.0)

print("Demo data created!")
```

## API Endpoints Reference

### Owner Endpoints
- `GET /api/owner/statistics?owner_id={id}` - Dashboard statistics
- `GET /api/allocations/available-vehicles?owner_id={id}` - Available vehicles
- `GET /api/allocations/unallocated-loads` - Unallocated loads
- `POST /api/allocations` - Create allocation
- `DELETE /api/allocations/{id}` - Cancel allocation

### Driver Endpoints
- `GET /api/driver/allocated-loads?driver_id={id}` - Get allocated loads
- `POST /api/driver/allocated-loads/{id}/pickup` - Mark picked up
- `POST /api/driver/allocated-loads/{id}/complete` - Mark completed

### Navigation Endpoints
- `POST /api/navigation/location-update` - Update location
- `GET /api/navigation/current-location?vehicle_id={id}` - Get location
- `GET /api/navigation/route` - Calculate route

### Notification Endpoints
- `GET /api/notifications?driver_id={id}` - Get notifications
- `GET /api/notifications/unread-count?driver_id={id}` - Unread count
- `POST /api/notifications/{id}/read` - Mark as read

## Next Steps

1. ✅ Backend APIs working
2. ✅ Frontend components integrated
3. ✅ Owner dashboard has Manual Allocation tab
4. ✅ Driver dashboard has Allocated Loads tab
5. 🔄 Add demo data for testing
6. 🔄 Test allocation workflow end-to-end
7. 🔄 Add live navigation map integration
8. 🔄 Add notification badges

## Success Criteria

✅ Owner can see statistics
✅ Owner can view available vehicles
✅ Owner can view unallocated loads
✅ Owner can create allocations
✅ Driver can see allocated loads
✅ Driver can mark loads as picked up
✅ Driver can complete loads
✅ System prevents deadheading conflicts

## Support

If you encounter any issues:
1. Check backend console for errors
2. Check browser console for errors
3. Run `test_manual_allocation.py` to verify backend
4. Check `MANUAL_ALLOCATION_IMPLEMENTATION.md` for detailed docs
