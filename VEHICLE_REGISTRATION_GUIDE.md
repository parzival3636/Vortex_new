# Vehicle Registration Feature - Complete Guide

## ✅ What Was Added

### Owner Dashboard - Manual Allocation Tab
Now has **3 sections** in this order:

1. **Admin Panel** (Purple box)
   - Seed Demo Data button
   - Clear All Data button

2. **Vehicle Registration** (Blue "Register New Vehicle" button)
   - Click to open registration form
   - Add vehicles with drivers
   - Set GPS location

3. **Owner Statistics** (6 metric cards)
   - Shows real-time stats

4. **Manual Allocation** (Vehicle & Load lists)
   - Allocate vehicles to loads

## 🚗 How to Register a Vehicle

### Option 1: Quick Start with Demo Data
1. Open Owner Dashboard → Manual Allocation tab
2. Click **"Seed Demo Data"** in Admin Panel
3. ✅ Instantly creates 5 vehicles with drivers!

### Option 2: Manual Registration
1. Open Owner Dashboard → Manual Allocation tab
2. Click **"Register New Vehicle"** button
3. Fill in the form:

#### Vehicle Information
- **License Plate** (Required): e.g., `DL-01-AB-1234`
- **Fuel Consumption Rate**: Default 0.35 L/km

#### Driver Information
- **Driver Name** (Required): e.g., `Rajesh Kumar`
- **Driver Phone** (Required): e.g., `+91-9876543210`

#### Current Location (Optional)
- **Latitude**: e.g., `28.6139`
- **Longitude**: e.g., `77.2090`
- **Address**: e.g., `Delhi, India`

4. Click **"Register Vehicle"**
5. ✅ Vehicle appears in Available Vehicles list!

## 📋 Form Fields Explained

### Required Fields
- ✅ License Plate - Unique identifier for the truck
- ✅ Driver Name - Who will drive this truck
- ✅ Driver Phone - Contact number

### Optional Fields
- Fuel Consumption Rate - Defaults to 0.35 L/km if not provided
- Current Location - Defaults to Delhi (28.6139, 77.2090) if not provided

## 🎯 What Happens When You Register

1. **Truck Created** - Added to database with license plate
2. **Driver Created** - Assigned to the truck
3. **Location Set** - GPS coordinates stored
4. **Status Set** - Vehicle marked as "idle" (available)
5. **Auto-Refresh** - Statistics and vehicle list update automatically

## 💡 Tips

### Getting GPS Coordinates
1. **Google Maps**: Right-click location → Copy coordinates
2. **Manual Entry**: 
   - Delhi: `28.6139, 77.2090`
   - Mumbai: `19.0760, 72.8777`
   - Bangalore: `12.9716, 77.5946`
   - Jaipur: `26.9124, 75.7873`

### License Plate Format
- Indian format: `XX-00-XX-0000`
- Examples:
  - `DL-01-AB-1234` (Delhi)
  - `MH-02-CD-5678` (Maharashtra)
  - `KA-03-EF-9012` (Karnataka)

### Phone Number Format
- Include country code: `+91-9876543210`
- Or without: `9876543210`

## 🔄 Workflow

### Complete Owner Workflow
1. **Seed Demo Data** (or register vehicles manually)
2. **View Statistics** - See total vehicles
3. **View Available Vehicles** - See your fleet
4. **View Unallocated Loads** - See available work
5. **Allocate** - Assign vehicle to load
6. **Driver Gets Notified** - Automatic notification

### After Registration
- Vehicle appears in "Available Vehicles" (0)
- Statistics update automatically
- Vehicle ready for allocation
- Driver can see it in their dashboard

## 🎨 UI Features

### Registration Form
- **Collapsible** - Click button to show/hide
- **Color-Coded Sections**:
  - Blue = Vehicle info
  - Green = Driver info
  - Purple = Location info
- **Validation** - Required fields marked with *
- **Loading State** - Shows "Registering..." during save

### After Registration
- ✅ Success toast notification
- ✅ Form resets automatically
- ✅ Form closes automatically
- ✅ Vehicle list refreshes
- ✅ Statistics update

## 🐛 Troubleshooting

### "Failed to register vehicle"
**Cause**: Backend not running or API error
**Solution**: 
1. Check backend is running: `python main.py`
2. Check console for errors
3. Restart backend if needed

### Vehicle not appearing
**Cause**: Page not refreshed
**Solution**: 
1. Wait 2 seconds (auto-refresh)
2. Or manually refresh page
3. Or switch tabs and back

### Duplicate license plate
**Cause**: License plate already exists
**Solution**: Use a different license plate number

## 📊 Database Structure

### What Gets Created
```
Truck:
- truck_id: UUID
- owner_id: Your owner ID
- license_plate: What you entered
- fuel_consumption_rate: 0.35 or custom
- status: "idle"

Driver:
- driver_id: UUID
- name: What you entered
- phone: What you entered
- truck_id: Links to truck
- hourly_rate: 25.0 (default)

Location:
- location_id: UUID
- vehicle_id: Links to truck
- latitude: What you entered or 28.6139
- longitude: What you entered or 77.2090
- accuracy: 10.0
```

## 🚀 Quick Test

1. Open Owner Dashboard
2. Click "Manual Allocation" tab
3. Click "Seed Demo Data" → Creates 5 vehicles
4. Click "Register New Vehicle"
5. Fill: 
   - License: `TEST-01-XX-9999`
   - Driver: `Test Driver`
   - Phone: `+91-9999999999`
6. Click "Register Vehicle"
7. ✅ See 6 vehicles now (5 demo + 1 new)

## 🎉 Success Indicators

✅ "Vehicle registered successfully!" toast
✅ Form closes automatically
✅ Statistics show +1 vehicle
✅ Vehicle appears in Available Vehicles list
✅ Can allocate the new vehicle to loads

## 📝 API Endpoint

```
POST /api/vehicles/register

Request:
{
  "ownerId": "demo-owner-123",
  "licensePlate": "DL-01-AB-1234",
  "driverName": "Rajesh Kumar",
  "driverPhone": "+91-9876543210",
  "fuelConsumptionRate": 0.35,
  "currentLocation": {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "address": "Delhi, India"
  }
}

Response:
{
  "success": true,
  "message": "Vehicle registered successfully",
  "truck": {...},
  "driver": {...}
}
```

## 🔗 Related Features

- **Admin Panel** - Seed demo data
- **Owner Statistics** - View fleet metrics
- **Manual Allocation** - Assign vehicles to loads
- **Driver Dashboard** - Drivers see their assigned vehicle

The vehicle registration feature is now fully integrated and ready to use! 🚀
