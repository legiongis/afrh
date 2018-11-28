define([
    'jquery',
    'openlayers',
    'underscore',
    'arches'
], function($, ol, _, arches) {
    
    var osm_attr = new ol.Attribution({
        html: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors.'
    });

    //streets ol layer
    var streetLyr = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attributions: [osm_attr]
        }),
        visible: false,
    });
    
    //streets arches layer
    var street = {
        id: 'street',
        name: 'Streets',
        icon: arches.urls.media + 'img/map/osm.png',
        layer: streetLyr,
        altlayer: false,
        alttext: 'Open Street Map',
        showInfo: false,
    };
    street.layer.matchid = street.id;
    street.maxzoom = 20;
    
    var dc_attr = new ol.Attribution({
        html: '<a href="https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Ortho2013_WebMercator/MapServer" target="_blank">Ortho 2013 Map Service</a> &copy; <a href="http://octo.dc.gov/service/dc-gis-services" target="_blank">DC GIS</a>.'
    });
    
    var ms_attr = new ol.Attribution({
        html: '<a href="https://www.gis.ms.gov/portal/service.aspx?service=Aerial%20Photography" target="_blank">Mississippi Digital Earth Model, 2006</a>.'
    })
    
    // ol3 ortho layer which is a group, consisting of separate dc and ms hi-res orthos
    var orthoLyr = new ol.layer.Group({
        style: 'dcgis_imagery',
        layers: [
            
            //ol3 ortho layer from MS web services
            new ol.layer.Tile({
                preload: Infinity,
                source: new ol.source.TileArcGISRest({
                    url: 'https://www.maris.state.ms.us/arcgis2/rest/services/MDEM/MDEM_2006/MapServer',
                }),
                extent: [-10548293.782819713, 3491322.48132465, -9277237.966125775, 4199470.940998869],
            }),
            //ol3 ortho layer from DC GIS
            new ol.layer.Tile({
                preload: Infinity,
                source: new ol.source.XYZ({
                    url: 'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Ortho2013_WebMercator/MapServer/tile/{z}/{y}/{x}',
                    // turns out, attributions are taken from the top last layer in the list, not cumulatively from all.
                    attributions: [dc_attr,ms_attr]
                }),
            }),
            
        ],
        visible: false,
    });

    //arches ortho layer
    var imagery = {
        id: "imagery",
        name: "Imagery",
        icon: arches.urls.media + 'img/map/aerial.png',
        alttext: "",
        showInfo: false,
        layer: orthoLyr,
        altlayer: false,
    };
    imagery.layer.id = imagery.id;
    imagery.maxzoom = 20;

    //Make blank base layer in order to show no basemap
    var blankLyr = new ol.layer.Tile({
        name: "blank",
        source: new ol.source.XYZ({
            url: arches.urls.media + 'img/map/white_256x256.png',
        }),
        visible: false
    });  
    var blank = {
        id: 'blank',
        name: 'None',
        icon: arches.urls.media + 'img/map/thb_blank.png',
        layer: blankLyr,
        altlayer: false,
        alttext: 'Click to remove basemap',
        showInfo: 'When viewing some historic maps, it may be useful to remove the basemap altogether.',
    };
    blank.layer.matchid = blank.id;
    blank.maxzoom = 20;

    // aggregate layers in the baseLayers array
    var baseLayers = [
        street,
        imagery,
        blank,
    ];  

    //set default map style to Bing
    baseLayers[0].layer.setVisible(true);
    return baseLayers;
});