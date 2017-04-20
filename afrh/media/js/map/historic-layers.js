define([
    'jquery',
    'openlayers',
    'underscore',
    'arches'
], function($, ol, _, arches) {
    
    // 1851 george riggs farm map
    var hm1851 = {
        id: 'hm1851',
        name: 'c. 1851 Plat Map',
        icon: arches.urls.media + 'img/map/1850_George_Riggs_icon.png',
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
        showInfo: "c. 1851 plat map of the George W. Riggs Property, which was purchased by the federal government in 1851 to establish the Washington branch of the U.S. Military Asylum, later to become AFRH-W; (image courtesy of the National Archives Records Administration, Washington, D.C.; filed under “Plat Map of the George W. Rigge’s [sic] Property”)"
    };
    hm1851.layer.matchid = hm1851.id;

    // 1865 barnard map
    var hm1865 = {
        id: 'hm1865',
        name: '1865 Boschke/Barnard Map',
        icon: arches.urls.media + 'img/map/1865_Barnard_icon.png',
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
        showInfo: "<em>Map of the Environs of Washington Compiled from Boschke’s Map of the District of Columbia and from Surveys of the U.S. Coast Survey Showing the Line of the Defences of Washington as Constructed During the War from 1861 to 1865—Inclusive</em>, to accompany the report by Brevet Major General John G. Barnard, Colonel of Engineers, Late Chief Engineer of Defences, 1865 (image courtesy of the Library of Congress)."
    };
    hm1865.layer.matchid = hm1865.id;
    
    console.log("layer made");
    
    // 1867 michler map
    var hm1867 = {
        id: 'hm1867',
        name: '1867 Michler Map',
        icon: arches.urls.media + 'img/map/1866-67_Michler_Memory_icon.png',
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
        showInfo: "<em>Topographical Sketch of the Environs of Washington, D.C.</em>, to accompany report of Nathanial Michler, topographical engineer for the Federal Army, made in compliance with Senate Resolution of 18 July 1866, Survey of Locality for Public Park of Site for a Presidential Mansion. Approved by Committee of Public Buildings and Grounds of the Senate 20 February 1867 (image courtesy of the Library of Congress)."
    };
    hm1867.layer.matchid = hm1867.id;
    
    // bootes map
    var hm1873 = {
        id: 'hm1873',
        name: '1873 Map',
        icon: arches.urls.media + 'img/map/1873_Bootes_icon.png',
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
        showInfo: "<em>Map of Soldiers’ Home near Washington, D.C.</em>, compiled from surveys by S. Bootes, Lewis Carbery, and B.D. Carpenter; American Photo-Lithograph Company, New York, 1873 (image courtesy of the Library of Congress)."
    };    
    hm1873.layer.matchid = hm1873.id;
    
    // 1877 entwhistle map
    var hm1877 = {
        id: 'hm1877',
        name: '1877 J.C. Entiwistle Map',
        icon: arches.urls.media + 'img/map/1877_JC_Entwhistle_icon.png',
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
        showInfo: "<em>Map of Soldiers’ Home Near Washington, D.C.</em>, J.C. Entiwistle Lithographs, 1877 (image courtesy of the Library of Congress)."
    };    
    hm1877.layer.matchid = hm1877.id;
    
    // 1892 usgs map
    var hm1892 = {
        id: 'hm1892',
        name: '1892 USGS Map',
        icon: arches.urls.media + 'img/map/1892_USGS_icon.png',
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
        showInfo: "United States Geological Survey Map, Washington West, 7-1/2 minute topographic quadrangle map (image courtesy of USGS)"
    };    
    hm1892.layer.matchid = hm1892.id;
    
    // 1910 acoe map
    var hm1910 = {
        id: 'hm1910',
        name: '1910 Army Corps of Engineers Map',
        icon: arches.urls.media + 'img/map/1903_Army_icon.png',
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
        showInfo: "<em>Map of the U.S. Soldiers’ Home, Washington D.C.</em>, surveyed by 1st Lieutenant P.S. Bond, Corps of Engineers of the U.S. Army, June 1903 (image courtesy of the National Archives Records Administration, Washington, D.C.). Map notes that the survey was based on U.S. C. and G.S. topography of 1892 and boundary survey of William H. Benton in 1902, revised by E.T. Cudworth 15 December 1908, and revised 1 September 1910. This map is one of the most detailed records of physical conditions of the U.S. Soldiers’ Home during the height of its development."
    };    
    hm1910.layer.matchid = hm1910.id;
    
    // 1914 topo map
    var hm1914 = {
        id: 'hm1914',
        name: '1914 Topographical Map',
        icon: arches.urls.media + 'img/map/1914_Topographic_icon.png',
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
        showInfo: "<em>Map of the U.S. Soldiers’ Home</em>; map notes that the topographical contour lines shown are traced from a map made from the original survey of 1892, with revisions made to show the exact locations of buildings, roads, walks, surface, and subsurface drains as they were on 20 July 1914. This map is one of the most detailed records of physical conditions of the U.S. Soldiers’ Home during the height of its development. (image courtesy of AFRH-W)."
    };    
    hm1914.layer.matchid = hm1914.id;
    
    // 1944 topo map
    var hm1944 = {
        id: 'hm1944',
        name: '1944 Topographical Map',
        icon: arches.urls.media + 'img/map/1944_Topo_icon.png',
        layer: new ol.layer.Tile({
            source: new ol.source.TileWMS({
                url: 'http://52.27.146.197/geoserver/historicmaps/wms/',
                params: {
                    'LAYERS':'historicmaps:1944_Topo',
                    'TILED':true,
                },
                serverType: 'geoserver'
            }),
            visible: false,
        }),
        altlayer: false,
        showInfo: "Topographical survey of the U.S. Soldiers’ Home, November 1944. The map references Porter and Lockie (architect engineer), W.N. Browning (surveyor), William Karunsky (mechanical engineer), and Marshall B. Gongwer (structural engineers). This is the last detailed map and schedule of buildings from the period of significance of the AFRH-W Historic District, prior to the disposition of land and demolition of several buildings in the 1950s."
    };    
    hm1944.layer.matchid = hm1944.id;
    
    // 1953 master plan map
    var hm1953 = {
        id: 'hm1953',
        name: '1953 Master Plan Map',
        icon: arches.urls.media + 'img/map/1953_Master_Plan_icon.png',
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
        showInfo: "U.S. Soldiers’ Home, Washington, D.C. Existing Water System, prepared by S.E. Sanders-C.H. Turrell & Associates, Land Planners, 15 May 1953 (image courtesy of AFRH-W). Map shows campus prior to disposition of eastern parcel."
    };    
    hm1953.layer.matchid = hm1953.id;
    
    // 1967 topo map
    var hm1967 = {
        id: 'hm1967',
        name: '1967 Topographical Map',
        icon: arches.urls.media + 'img/map/1967_Topographic_icon.png',
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
        showInfo: "Topographical Map, United States Soldiers’ Home, prepared by Hayes, Seay, Mattern & Mattern, August 1967 (image courtesy of AFRH-W). Map shows campus prior to disposition of eastern parcel."
    };    
    hm1967.layer.matchid = hm1967.id;
    
    var hm1975 = {
        id: 'hm1975',
        name: '1975 Schedule of Structures',
        icon: arches.urls.media + 'img/map/1975_Shedule_icon.png',
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
        showInfo: "United States Soldiers’ and Airmen’s Home, Schedule of Structures, November 1975 (image courtesy of AFRH-W). Map shows campus prior to disposition of eastern parcel."
    };    
    hm1975.layer.matchid = hm1975.id;

    // aggregate layers in historicLayers array
    var historicLayers = [
        hm1851,
        hm1865,
        hm1867,
        hm1873,
        hm1877,
        hm1892,
        hm1910,
        hm1914,
        hm1944,
        hm1953,
        hm1967,
        hm1975,
    ]  
   
    return historicLayers;
});