mapboxgl.accessToken = 'pk.eyJ1IjoieW9uYXRoYW42MTIiLCJhIjoiY20xd2hjNDduMGw3YjJpcTFpamZlOWFsZyJ9.6bSbM59bBUpR6W2l_Puauw';

navigator.geolocation.getCurrentPosition(successLocation, errorLocation, { enableHighAccuracy: true });

function successLocation(position) {
    setupMap([-87.6298, 41.8781]); // Centering on Chicago
}

function errorLocation() {
    setupMap([-87.6298, 41.8781]);
}

function setupMap(center) {
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: center,
        zoom: 12,
        pitch: 45,
        bearing: -17.6,
        antialias: true
    });

    // Navigation control
    const nav = new mapboxgl.NavigationControl();
    map.addControl(nav);

    // Load the custom image
    map.loadImage('apple.png', function (error, image) {
        if (error) throw error; // Handle any loading error

        // Add the image to the map
        map.addImage('apple-icon', image);  // 'apple-icon' is the name you can use to reference this image

        // Fetch the external GeoJSON file and add it to the map
        fetch('stores.geojson')  // Replace with your actual file path or URL
            .then(response => response.json())
            .then(data => {
                // Add a GeoJSON source with the fetched data
                map.addSource('stores', {
                    type: 'geojson',
                    data: data  // The fetched GeoJSON data
                });

                // Add a layer to visualize the GeoJSON points with the custom icon
                map.addLayer({
                    'id': 'store-markers',
                    'type': 'symbol',
                    'source': 'stores',
                    'layout': {
                        'icon-image': 'apple-icon',  // Reference the image name here
                        'icon-size': 0.02,  // Adjust the size of the icon
                        'icon-allow-overlap': true  // Allow icons to overlap
                    }
                });
            })
            .catch(error => console.log('Error loading the GeoJSON file:', error));
    });

    // Add 3D buildings layer (optional)
    map.on('load', function () {
        var layers = map.getStyle().layers;
        var labelLayerId;
        for (var i = 0; i < layers.length; i++) {
            if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
                labelLayerId = layers[i].id;
                break;
            }
        }

        map.addLayer({
            'id': '3d-buildings',
            'source': 'composite',
            'source-layer': 'building',
            'filter': ['==', 'extrude', 'true'],
            'type': 'fill-extrusion',
            'minzoom': 15,
            'paint': {
                'fill-extrusion-color': '#aaa',
                'fill-extrusion-height': [
                    'interpolate', ['linear'], ['zoom'],
                    15, 0,
                    15.05, ['get', 'height']
                ],
                'fill-extrusion-base': [
                    'interpolate', ['linear'], ['zoom'],
                    15, 0,
                    15.05, ['get', 'min_height']
                ],
                'fill-extrusion-opacity': 0.6
            }
        }, labelLayerId);
    });
}
