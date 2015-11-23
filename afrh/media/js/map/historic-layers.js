define([
    'jquery',
    'openlayers',
    'underscore',
    'arches'
], function($, ol, _, arches) {
    
    // 1850 george riggs farm map
    var hm1850 = {
        id: 'hm1850',
        name: '1865 George W. Riggs Farm Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1850_George_Riggs',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the george riggs map"
    };
    hm1850.layer.matchid = hm1850.id;

    // 1865 barnard map
    var hm1865 = {
        id: 'hm1865',
        name: '1865 Barnard Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1865_Barnard',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the barnard map"
    };
    hm1865.layer.matchid = hm1865.id;
    
    console.log("layer made");
    
    // 1866-67 michler map
    var hm1866 = {
        id: 'hm1866',
        name: '1866-67 Michler Memory Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1866-67_Michler_Memory',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the michler memory map"
    };
    hm1866.layer.matchid = hm1866.id;
    
    // bootes map
    var hm1873 = {
        id: 'hm1873',
        name: '1873 Bootes Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1873_Bootes',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the bootes map"
    };    
    hm1873.layer.matchid = hm1873.id;
    
    // 1877 entwhistle map
    var hm1877 = {
        id: 'hm1877',
        name: '1877 JC Entwhistle Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1877_JC_Entwhistle',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the jc entwhistle map"
    };    
    hm1877.layer.matchid = hm1877.id;
    
    // 1892 usgs map
    var hm1892 = {
        id: 'hm1892',
        name: '1892 Beautiful USGS Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1892_USGS',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the gorgeous usgs map"
    };    
    hm1892.layer.matchid = hm1892.id;
    
    // 1903 acoe map
    var hm1903 = {
        id: 'hm1903',
        name: '1903 Army Corps of Engineers Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1903_ACoE',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the army corps of engineers map"
    };    
    hm1903.layer.matchid = hm1903.id;
    
    // 1914 topo map
    var hm1914 = {
        id: 'hm1914',
        name: '1914 Topographical Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1914_Topo',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the 1914 topo map"
    };    
    hm1914.layer.matchid = hm1914.id;
    
    // 1944 topo map
    var hm1944 = {
        id: 'hm1944',
        name: '1944 Topographical Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1914_Topo',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the 1944 topo map"
    };    
    hm1944.layer.matchid = hm1944.id;
    
    // 1953 master plan map
    var hm1953 = {
        id: 'hm1953',
        name: '1953 Master Plan Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1953_Master_Plan',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for the master plan map"
    };    
    hm1953.layer.matchid = hm1953.id;
    
    // 1967 topo map
    var hm1967 = {
        id: 'hm1967',
        name: '1967 Topographic Map',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1967_Topo',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for 1967 topo map"
    };    
    hm1967.layer.matchid = hm1967.id;
    
    var hm1975 = {
        id: 'hm1975',
        name: '1975 Schedule of Structures',
        icon: arches.urls.media + 'img/map/bing_satellite.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1975_Schedule_of_Structures',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "this is the info for schedule of structures"
    };    
    hm1975.layer.matchid = hm1975.id;

    // aggregate layers in historicLayers array
    var historicLayers = [
        hm1850,
        hm1865,
        hm1866,
        hm1873,
        hm1877,
        hm1892,
        hm1903,
        hm1914,
        hm1944,
        hm1953,
        hm1967,
        hm1975,
    ]  
   
    return historicLayers;
});