var truckLocation = [127.070, 37.500];
var warehouseLocation = [127.070, 37.500];
var lastQueryTime = 0;
var lastAtRestaurant = 0;
var keepTrack = [];
var currentSchedule = [];
var currentRoute = null;
var pointHopper = {};
var pause = true;
var speedFactor = 50;
var dropoffs = turf.featureCollection([]);
var nothing = turf.featureCollection([]);
// Add your access token
mapboxgl.accessToken = 'pk.eyJ1IjoidWhuNjEiLCJhIjoiY2tpNGU1cDBlMjBpeDJwcjA3a3k0MG1pNSJ9.bIdr0HK6T40QFkwGunGLQg';
// Initialize a map
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v10',
    center: truckLocation, // starting position
    zoom: 12
  });
map.on('load', function() {
    map.addSource('route', {
        "type": 'geojson',
        "data": geojson
    });
    map.addLayer({
        id: 'route',
        type: 'line',
        source: 'route',
        layout: {
        'line-join': 'round',
        'line-cap': 'round'
        },
        paint: {
        'line-color': '#3887be',
        'line-width': 5,
        'line-opacity': 0.75
        }
    });
    map.addLayer({
        id: 'dropoffs-symbol',
        type: 'symbol',
        source: {
          data: dropoffs,
          type: 'geojson'
        },
        layout: {
          'icon-allow-overlap': true,
          'icon-ignore-placement': true,
          'icon-image': 'embassy-15',
          'icon-size': 1
        }
      }); 
    map.addLayer({
        id: 'routearrows',
        type: 'symbol',
        source: 'route',
        layout: {
            'symbol-placement': 'line',
            'text-field': '▶',
            'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            24,
            22,
            60
            ],
            'symbol-spacing': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            30,
            22,
            160
            ],
            'text-keep-upright': false
        },
        paint: {
            'text-color': '#3887be',
            'text-halo-color': 'hsl(55, 11%, 96%)',
            'text-halo-width': 3
        }
        },
        'waterway-label'
    );
});
    //https://docs.mapbox.com/help/tutorials/optimization-api/