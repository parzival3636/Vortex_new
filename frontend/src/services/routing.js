/**
 * Routing Service using OSRM (Open Source Routing Machine)
 * Provides real road-to-road navigation like Google Maps
 */

const OSRM_BASE_URL = 'https://router.project-osrm.org';

/**
 * Get route between two points using OSRM
 * @param {Object} start - {lat, lng}
 * @param {Object} end - {lat, lng}
 * @returns {Promise<Object>} Route data with coordinates, distance, duration
 */
export const getRoute = async (start, end) => {
  try {
    const url = `${OSRM_BASE_URL}/route/v1/driving/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`;
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.code === 'Ok' && data.routes && data.routes.length > 0) {
      const route = data.routes[0];
      
      // Convert GeoJSON coordinates to Leaflet format [lat, lng]
      const coordinates = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
      
      return {
        coordinates,
        distance: route.distance, // meters
        duration: route.duration, // seconds
        distanceKm: (route.distance / 1000).toFixed(2),
        durationMin: Math.round(route.duration / 60)
      };
    }
    
    // Fallback to straight line if routing fails
    return {
      coordinates: [[start.lat, start.lng], [end.lat, end.lng]],
      distance: 0,
      duration: 0,
      distanceKm: '0',
      durationMin: 0,
      fallback: true
    };
  } catch (error) {
    console.error('Routing error:', error);
    // Fallback to straight line
    return {
      coordinates: [[start.lat, start.lng], [end.lat, end.lng]],
      distance: 0,
      duration: 0,
      distanceKm: '0',
      durationMin: 0,
      fallback: true
    };
  }
};

/**
 * Get route through multiple waypoints
 * @param {Array<Object>} waypoints - Array of {lat, lng} objects
 * @returns {Promise<Object>} Route data
 */
export const getRouteWithWaypoints = async (waypoints) => {
  try {
    if (waypoints.length < 2) {
      throw new Error('At least 2 waypoints required');
    }
    
    // Convert waypoints to OSRM format: lng,lat;lng,lat;...
    const coords = waypoints.map(wp => `${wp.lng},${wp.lat}`).join(';');
    const url = `${OSRM_BASE_URL}/route/v1/driving/${coords}?overview=full&geometries=geojson`;
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.code === 'Ok' && data.routes && data.routes.length > 0) {
      const route = data.routes[0];
      
      // Convert GeoJSON coordinates to Leaflet format [lat, lng]
      const coordinates = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
      
      return {
        coordinates,
        distance: route.distance,
        duration: route.duration,
        distanceKm: (route.distance / 1000).toFixed(2),
        durationMin: Math.round(route.duration / 60)
      };
    }
    
    // Fallback to straight lines
    return {
      coordinates: waypoints.map(wp => [wp.lat, wp.lng]),
      distance: 0,
      duration: 0,
      distanceKm: '0',
      durationMin: 0,
      fallback: true
    };
  } catch (error) {
    console.error('Routing error:', error);
    return {
      coordinates: waypoints.map(wp => [wp.lat, wp.lng]),
      distance: 0,
      duration: 0,
      distanceKm: '0',
      durationMin: 0,
      fallback: true
    };
  }
};

/**
 * Get multiple routes at once
 * @param {Array<Object>} routeRequests - Array of {start, end} objects
 * @returns {Promise<Array<Object>>} Array of route data
 */
export const getMultipleRoutes = async (routeRequests) => {
  try {
    const promises = routeRequests.map(req => getRoute(req.start, req.end));
    return await Promise.all(promises);
  } catch (error) {
    console.error('Multiple routes error:', error);
    return routeRequests.map(req => ({
      coordinates: [[req.start.lat, req.start.lng], [req.end.lat, req.end.lng]],
      distance: 0,
      duration: 0,
      distanceKm: '0',
      durationMin: 0,
      fallback: true
    }));
  }
};

export default {
  getRoute,
  getRouteWithWaypoints,
  getMultipleRoutes
};
