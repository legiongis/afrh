define([
    'jquery',
    'openlayers',
    'underscore',
    'arches'
], function($, ol, _, arches) {
    //var bingLayers = arches.bingLayers;
/*
    //get bing baselayers as an array
    _.each(bingLayers, function(layer) {
        layer.layer = new ol.layer.Tile({
            visible: false,
            preload: Infinity,
            source: new ol.source.BingMaps({
                key: arches.bingKey,
                imagerySet: layer.id
            })
        });
    });

     //pull desirable bing layers and set new thumbnails
    var bingstr = bingLayers[0];
    bingstr.icon = arches.urls.media + 'img/map/thb_bingstr.png';
    bingstr.alttext = 'Bing Streets';
    bingstr.layer.matchid = bingstr.id;
    bingstr.altlayer = false;
    bingstr.showInfo = false;
    bingstr.maxzoom = 19;

    var bingsat = bingLayers[1];
    bingsat.icon = arches.urls.media + 'img/map/thb_bingsat.png';
    bingsat.alttext = 'Bing Satellite Imagery';
    bingsat.layer.matchid = bingsat.id;
    bingsat.altlayer = false;
    bingsat.showInfo = false;
    bingsat.maxzoom = 19;

    var binghyb = bingLayers[2];
    binghyb.icon = arches.urls.media + 'img/map/thb_binghyb.png';
    binghyb.alttext = 'Bing Satellite and Streets';
    binghyb.layer.matchid = binghyb.id;
    binghyb.altlayer = false;
    binghyb.showInfo = false;
    binghyb.maxzoom = 19; */

    //streets ol layer (use osm from mapquest 6/20 updating to OpenCycleMap for better building rendering)
    var streetLyr = new ol.layer.Tile({
        // source: new ol.source.MapQuest({
            // layer: 'osm',
        // }),
        source: new ol.source.XYZ({
            url: 'https://a.tile.thunderforest.com/cycle/{z}/{x}/{y}.png',
            attributions: [
                new ol.Attribution({
                    html: '<a href="http://atlas.lsu.edu" target="_blank">Atlas: The Louisiana Statewide GIS</a>. LSU Department of Geography and Anthropology, Baton Rouge, LA.'
                })
            ],
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
    })
    
    //ol3 ortho layer from DC GIS
    orthoLyr = new ol.layer.Tile({
        name: 'dcgis_imagery',
        preload: Infinity,
        source: new ol.source.XYZ({
            url: 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Ortho2013_WebMercator/MapServer/tile/{z}/{y}/{x}',
            attributions: [dc_attr],
        }),
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
    
    //hybrid ol layer (which is actually an ol layer group)
    var hybridLyr = new ol.layer.Group({
        style: 'AerialWithLabels',
        layers: [
            new ol.layer.Tile({
                name: 'imagery',
                preload: Infinity,
                source: new ol.source.XYZ({
                    url: 'http://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Ortho2013_WebMercator/MapServer/tile/{z}/{y}/{x}',
                    attributions: [dc_attr],
                }),
            }),
            new ol.layer.Tile({
                source: new ol.source.MapQuest({layer: 'hyb'})
            })
        ],
        visible: false,
    });
    
    //hybrid arches layer
    var hybrid = {
        id: "hybrid",
        name: "Streets & Imagery",
        icon: arches.urls.media + 'img/map/hybrid.png',
        alttext: "",
        showInfo: false,
        layer: hybridLyr,
        altlayer: false
    };
    hybrid.layer.id = hybrid.id
    hybrid.maxzoom = 20;
    
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
    
/*     
    // ------------------------------------ NOT CURRENTLY USED ---------------------------------------
    
    //USGS Topo from CRNHA server
    var usgsLyr = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: 'http://crhim.canerivernha.org/tiles/drg/{z}/{x}/{y}.png',
            attributions: [
                new ol.Attribution({
                    html: '<a href="http://www.usgs.gov/" target="_blank"><img src="'+arches.urls.media + 'img/icons/USGS_trans.png"/></a> All U.S. Geological Survey maps are in the public domain.'
                })
            ],
        }),
        visible: false,
    });    
    var usgs = {
        id: 'usgs',
        name: 'USGS 24k Topo',
        icon: arches.urls.media + 'img/map/thb_usgs.png',
        layer: usgsLyr,
        altlayer: false,
        alttext: 'USGS Digital Raster Graphics, 1:24,000',
        showInfo: 'This is a seamless mosaic of 24k USGS Quads, obtained through the NRCS <a href="http://datagateway.nrcs.usda.gov/" target="_blank">Geospatial Data Gateway</a>.',
    };
    usgs.layer.matchid = usgs.id;
    usgs.maxzoom = 17;
     
    //Shaded Relief basemap from CRNHA server  
    var reliefLyr = new ol.layer.Tile({
        name: "relief",
        source: new ol.source.XYZ({
            url: 'http://crhim.canerivernha.org/tiles/relief_basemap/{z}/{x}/{y}.png',
            attributions: [
                new ol.Attribution({
                    html: '<a href="http://atlas.lsu.edu" target="_blank">Atlas: The Louisiana Statewide GIS</a>. LSU Department of Geography and Anthropology, Baton Rouge, LA.'
                })
            ],
        }),
        opacity: .95,
        visible: false,
    });
    
    // b/w altlayer for hillshade
    var hillshadeLyr = new ol.layer.Tile({
        name: "relief",
        source: new ol.source.XYZ({
            url: 'http://crhim.canerivernha.org/tiles/hillshade/{z}/{x}/{y}.png',
            https://[abc].tile.thunderforest.com/cycle/{z}/{x}/{y}.png
            attributions: [
                new ol.Attribution({
                    html: '<a href="http://atlas.lsu.edu" target="_blank">Atlas: The Louisiana Statewide GIS</a>. LSU Department of Geography and Anthropology, Baton Rouge, LA.'
                })
            ],
        }),
        visible: false,
    });
    var relief = {
        id: 'relief',
        name: 'Shaded Relief',
        icon: arches.urls.media + 'img/map/thb_relief.png',
        layer: reliefLyr,
        altlayer: hillshadeLyr,
        alttext: 'Shaded Relief from Louisiana Statewide LiDAR Project',
        showInfo: 'This layer is a hillshade derivative of LiDAR data distributed by <a href="http://atlas.lsu.edu" target="_blank">Atlas: The Louisiana Statewide GIS</a>, which was produced for the <a href="http://atlas.lsu.edu/central/la_lidar_project.pdf" target="_blank">Louisiana State LiDAR Project</a>, LSU Department of Geography and Anthropology, Baton Rouge, LA.',
    };

    relief.layer.matchid = relief.id;
    relief.altlayer.matchid = relief.id;
    relief.maxzoom = 18;

    
    
    //Make blank base layer in order to show no basemap
    var amcemLyr = new ol.layer.Tile({
        name: "amcem",
        source: new ol.source.TileWMS({
            url: 'http://crhim.canerivernha.org/geoserver/raster/wms/',
            params: {
                'LAYERS': 'raster:basemap_image',
                'TILED': true,
            },
            serverType: 'geoserver'   
        }),
        visible: false
    });  
    var amcem = {
        id: 'amcem',
        name: 'American Cemetery',
        icon: false,
        layer: amcemLyr,
        altlayer: false,
        alttext: 'Click to remove basemap',
        showInfo: 'When viewing some historic maps, it may be useful to remove the basemap altogether.',
    };
    blank.layer.matchid = blank.id;
    blank.maxzoom = 20;
    
    // ------------------------------------------------ END OF NOT CURRENTLY USED LAYERS ----------------------------
 */
    // aggregate layers in the baseLayers array
    var baseLayers = [
        street,
        imagery,
        //hybrid,
        blank,
    ];  

    //set default map style to Bing
    baseLayers[0].layer.setVisible(true);
    return baseLayers;
});