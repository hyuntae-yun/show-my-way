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

// Add your access token
mapboxgl.accessToken = 'pk.eyJ1IjoidWhuNjEiLCJhIjoiY2tpNGU1cDBlMjBpeDJwcjA3a3k0MG1pNSJ9.bIdr0HK6T40QFkwGunGLQg';
var dropoffs = turf.featureCollection([]);
// Initialize a map
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/mapbox/streets-v10', // stylesheet location
    center: truckLocation, // starting position
    zoom: 12 // starting zoom
});
map.on('load', function() {
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

});
map.on('click', function(e) {
    newDropoff(map.unproject(e.point));
    updateDropoffs(dropoffs);
  });
function newDropoff(coords) {
    var pt = turf.point(
        [coords.lng, coords.lat]
    );
    dropoffs.features.push(pt);
}
  
function updateDropoffs(geojson) {
map.getSource('dropoffs-symbol')
    .setData(geojson);
}
    //https://docs.mapbox.com/help/tutorials/optimization-api/