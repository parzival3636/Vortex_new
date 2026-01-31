# Address Input Guide - Improved System

## Overview
The address input system has been completely redesigned for speed, accuracy, and ease of use. You can now select specific streets, landmarks, and buildings with GPS precision.

## How to Use

### For Vendors (Posting Loads)

1. **Click "Post New Load"** button in Vendor Dashboard

2. **Enter Pickup Address**:
   - Start typing (minimum 3 characters)
   - Wait for suggestions to appear (300ms)
   - See loading spinner while searching
   - Select from dropdown suggestions

3. **Enter Destination Address**:
   - Same process as pickup
   - Select specific delivery location

4. **Fill Weight and Price**

5. **Click "Post Load"**

### For Drivers/Owners (Finding Loads)

1. **Enter Origin (Current Location)**:
   - Type your current location
   - Select from suggestions
   - GPS coordinates captured automatically

2. **Enter Destination (Home/Base)**:
   - Type your home or base location
   - Select from suggestions

3. **Click "Find Return Loads"**:
   - AI will automatically find best loads
   - Or manually select from available loads

## Tips for Best Results

### ✅ DO:
- **Type at least 3 characters** before expecting suggestions
- **Include street name** for better accuracy (e.g., "MG Road Bangalore")
- **Add landmarks** for specific locations (e.g., "Azadpur Mandi Gate 3")
- **Select from dropdown** instead of typing full address
- **Wait for suggestions** to load (shows spinner)

### ❌ DON'T:
- Don't type too fast - wait for suggestions
- Don't use abbreviations (use "Road" not "Rd")
- Don't skip the dropdown selection
- Don't enter just city names (be specific)

## Example Searches

### Good Examples ✅
```
"MG Road Bangalore"          → Shows specific MG Road locations
"Azadpur Mandi Delhi"        → Shows market gates and sections
"Connaught Place Block A"    → Shows specific blocks
"Marine Drive Mumbai"        → Shows exact locations along the drive
"Sector 18 Noida"           → Shows sector-specific locations
```

### Poor Examples ❌
```
"Bangalore"                  → Too generic, many results
"Delhi"                      → City-level only, not precise
"Market"                     → Too vague
"MG"                        → Too short, no suggestions
```

## Features

### 🚀 Fast Autocomplete
- Results appear in 300-500ms
- Debounced input (waits for you to stop typing)
- Cached results for common searches

### 📍 Street-Level Precision
- Specific street segments
- Building numbers
- Landmarks and gates
- Neighborhood details

### 🎯 Smart Suggestions
- Sorted by relevance
- Shows location type (road, building, market, etc.)
- Displays full address with components
- Up to 8 suggestions per search

### 💡 Visual Feedback
- Loading spinner while searching
- Clear button to reset input
- Hover effects on suggestions
- Icons for different location types

## Troubleshooting

### No Suggestions Appearing?
- Check you've typed at least 3 characters
- Wait 300ms for debounce
- Check internet connection
- Try more specific search terms

### Wrong Location Selected?
- Click the X button to clear
- Type more specific address
- Include street name or landmark
- Select different suggestion from dropdown

### Slow Performance?
- First search may be slower (no cache)
- Subsequent searches are faster (cached)
- Check internet speed
- Try shorter, more specific queries

## Technical Details

### Search Process
1. Type 3+ characters
2. Wait 300ms (debounce)
3. API call to geocoding service
4. Results cached for speed
5. Display up to 8 suggestions
6. Select → GPS coordinates captured

### Data Returned
- **Address**: Full formatted address
- **GPS**: Latitude and longitude
- **Type**: Location type (road, building, etc.)
- **Components**: City, state, country, etc.
- **Relevance**: Importance score

### Performance
- **First Search**: 500-1000ms
- **Cached Search**: 50-100ms
- **Debounce Delay**: 300ms
- **API Rate Limit**: 0.5s between calls

## API Endpoints

### Search Places (Autocomplete)
```
GET /api/v1/vendors/geocode/search?query=MG Road&limit=8
```

### Geocode Address
```
GET /api/v1/vendors/geocode/address?address=Azadpur Mandi Delhi
```

### Structured Geocoding
```
GET /api/v1/vendors/geocode-structured?street=MG Road&city=Bangalore
```

## Support

If you experience issues:
1. Check the browser console for errors
2. Verify internet connection
3. Try clearing browser cache
4. Use more specific search terms
5. Contact support with error details

## Updates

**Version 2.0** (Current)
- ✅ Debounced input (300ms)
- ✅ 8 suggestions (up from 5)
- ✅ Street-level precision
- ✅ Caching for speed
- ✅ Loading indicators
- ✅ Clear buttons
- ✅ Better visual design
- ✅ Address components
- ✅ Relevance sorting

**Version 1.0** (Old)
- ❌ No debouncing
- ❌ Only 5 suggestions
- ❌ City-level accuracy
- ❌ No caching
- ❌ Slow (1-2s per search)
