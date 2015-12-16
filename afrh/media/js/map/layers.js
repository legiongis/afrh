define([
    'openlayers',
    'map/resource-layers',
    'map/layer-model',
    'layers-i18n'
], function(ol, resourceLayers, LayerModel, layerI18n) {
    var layers = resourceLayers.layers;

    var arch_zones = new LayerModel({
        name: 'Archaeological Zones',
        categories: ["Reference"],
        icon: 'fa fa-bookmark-o',
        infoContent: "Showing the 11 archaeological zones at the AFRH",
        onMap: true,
        active: true,
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://afrh.adamcfcox.com/geoserver/zonemaps/wms/',
                params: {
                    'LAYERS': 'zonemaps:arch_zones_map',
                    'TILED': true,
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var char_areas = new LayerModel({
        name: 'Character Areas',
        categories: ["Reference"],
        icon: 'fa fa-bookmark-o',
        infoContent: "Showing the character areas at the AFRH",
        onMap: true,
        active: true,
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://afrh.adamcfcox.com/geoserver/zonemaps/wms/',
                params: {
                    'LAYERS': 'zonemaps:char_areas_map',
                    'TILED': true,
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var mp_zones = new LayerModel({
        name: 'Master Plan Zones',
        categories: ["Reference"],
        icon: 'fa fa-bookmark-o',
        infoContent: "Showing the master plan zones at the AFRH",
        onMap: true,
        active: true,
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://afrh.adamcfcox.com/geoserver/zonemaps/wms/',
                params: {
                    'LAYERS': 'zonemaps:mp_zones_map',
                    'TILED': true,
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var plss_ref = new LayerModel({
        name: 'PLSS Reference',
        categories: ["Reference"],
        icon: 'fa fa-bookmark-o',
        infoContent: "Use this for quick reference when trying to determine the Township/Range designation of a resource or location",
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://crhim.canerivernha.org/geoserver/vect/wms/',
                params: {
                    'LAYERS': 'vect:PLSS_towns',
                    'TILED': true,
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var amcem_shrubs = new LayerModel({
        name: 'American Cemetery Veg: Shrubs',
        categories: ["Vegetation"],
        icon: 'fa fa-circle',
        iconColor: '#A8302E',
        infoContent: "Vegetation data for the American Cemetery.  Mapped in the fall of 2014 by Laura Bradford.",
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://crhim.canerivernha.org/geoserver/vect/wms/',
                params: {
                    'LAYERS': 'vect:amcem_shrubs',
                },
                serverType: 'geoserver'
            })
        })
    });
    var amcem_grass = new LayerModel({
        name: 'American Cemetery Veg: Ornamental Grass',
        categories: ["Vegetation"],
        icon: 'fa fa-circle',
        iconColor: '#5EB5B4',
        infoContent: "Vegetation data for the American Cemetery.  Mapped in the fall of 2014 by Laura Bradford.",
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://crhim.canerivernha.org/geoserver/vect/wms/',
                params: {
                    'LAYERS': 'vect:amcem_grass',
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var amcem_stumps = new LayerModel({
        name: 'American Cemetery Veg: Stumps',
        categories: ["Vegetation"],
        icon: 'fa fa-circle',
        iconColor: '#533D31',
        infoContent: "Vegetation data for the American Cemetery.  Mapped in the fall of 2014 by Laura Bradford.",
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://crhim.canerivernha.org/geoserver/vect/wms/',
                params: {
                    'LAYERS': 'vect:amcem_stumps',
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var amcem_trees = new LayerModel({
        name: 'American Cemetery Veg: Trees',
        categories: ["Vegetation"],
        icon: 'fa fa-circle',
        iconColor: '#5CBF4E',
        infoContent: "Vegetation data for the American Cemetery.  Mapped in the fall of 2014 by Laura Bradford.",
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://crhim.canerivernha.org/geoserver/vect/wms/',
                params: {
                    'LAYERS': 'vect:amcem_trees',
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var amcem_vines = new LayerModel({
        name: 'American Cemetery Veg: Vines',
        categories: ["Vegetation"],
        icon: 'fa fa-circle',
        iconColor: '#B5AB50',
        infoContent: "Vegetation data for the American Cemetery.  Mapped in the fall of 2014 by Laura Bradford.",
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://crhim.canerivernha.org/geoserver/vect/wms/',
                params: {
                    'LAYERS': 'vect:amcem_vines',
                },
                serverType: 'geoserver'
            })
        })
    });
    
    var amcem_bulbs = new LayerModel({
        name: 'American Cemetery Veg: Bulbs',
        categories: ["Vegetation"],
        icon: 'fa fa-circle',
        iconColor: '#9C7ABF',
        infoContent: "Vegetation data for the American Cemetery.  Mapped in the fall of 2014 by Laura Bradford.",
        layer: new ol.layer.Tile({
            is_arches_layer: "nobutclose",
            source: new ol.source.TileWMS({
                url: 'http://crhim.canerivernha.org/geoserver/vect/wms/',
                params: {
                    'LAYERS': 'vect:amcem_bulbs',
                },
                serverType: 'geoserver'
            })
        })
    });
    
    
    layers.push(
        arch_zones,
        char_areas,
        mp_zones,
        plss_ref,
        amcem_bulbs,
        amcem_grass,
        amcem_shrubs,
        amcem_stumps,
        amcem_trees,
        amcem_vines
    );

    return layers;
});
