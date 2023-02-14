const key = 'HDjaDoJpgHuEnYrXT4Ck';
const map = new maplibregl.Map({
  container: 'map', // container's id or the HTML element in which MapLibre GL JS will render the map
  style: `https://api.maptiler.com/maps/174f3e03-2ad9-4ab5-b178-5fa0bbfa7cc1/style.json?key=${key}`, // style URL
  center: [0, 30], // starting position [lng, lat]
  zoom: 1.25, // starting zoom
});
// map.boxZoom.disable();
// map.scrollZoom.disable();
var images = {
    'popup': 'https://maplibre.org/maplibre-gl-js-docs/assets/popup.png',
    'popup-debug':
        './legend.png'
};

var coord;

fetch("./Global_Launch_sites_022023.json")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            coord = data
        })

map.on('load', function () {
    //console.log(coord[1])
    main_data = []
    for (let x of coord) {
        schem = {
            'type': 'Feature',
            'properties': {
                'color': '#FFFFFF'
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [0, 0]
            }
        }
        // console.log(x['Longitude'])
        // console.log(x['Latitude'])
        // console.log(x['Operating_status'])
        schem['geometry']['coordinates'][0]=x['Longitude']
        schem['geometry']['coordinates'][1]=x['Latitude']
        // console.log(schem)
        if(x['Operating_status']=="TRUE"){
            schem['properties']['color']='#73D800'        }
        else{
            schem['properties']['color']='#D83F02'        }
        main_data.push(schem)
      }
    console.log(main_data)
    map.addSource('Launch-sites', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': main_data
        }
    });

    map.addLayer({
        'id': 'park-volcanoes',
        'type': 'circle',
        'source': 'Launch-sites',
        'paint': {
            'circle-radius': 5,
            'circle-color': ['get','color']
        },
        'filter': ['==', '$type', 'Point']
    });
});


loadImages(images, function (loadedImages) {
    map.on('load', function () {
        map.addImage('popup-debug', loadedImages['popup-debug'], {
            // The two (blue) columns of pixels that can be stretched horizontally:
            //   - the pixels between x: 25 and x: 55 can be stretched
            //   - the pixels between x: 85 and x: 115 can be stretched.
            stretchX: [
                [25, 55],
                [85, 115]
            ],
            // The one (red) row of pixels that can be stretched vertically:
            //   - the pixels between y: 25 and y: 100 can be stretched
            stretchY: [[25, 100]],
            // This part of the image that can contain text ([x1, y1, x2, y2]):
            content: [25, 25, 115, 100],
            // This is a high-dpi image:
            pixelRatio: 2.5
        });
       

        // the original, unstretched image for comparison
        map.addSource('original', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [-105, -20]
                        }
                    }
                ]
            }
        });
        map.addLayer({
            'id': 'original',
            'type': 'symbol',
            'source': 'original',
            'layout': {
                'text-field': '',
                'icon-image': 'popup-debug',
                'icon-overlap': 'always',
                'text-overlap': 'always'
            }
        });
    });
});

function loadImages(urls, callback) {
    var results = {};
    for (var name in urls) {
        map.loadImage(urls[name], makeCallback(name));
    }

    function makeCallback(name) {
        return function (err, image) {
            results[name] = err ? null : image;

            // if all images are loaded, call the callback
            if (Object.keys(results).length === Object.keys(urls).length) {
                callback(results);
            }
        };
    }
}
