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
        active: false,
        layer: new ol.layer.Tile({
            visible: false,
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
    
    var char_area_lyr_group = new ol.layer.Group({
        ///style: 'AerialWithLabels',
        layers: [
            new ol.layer.Tile({
                name: 'char_areas',
                source: new ol.source.TileWMS({
                    url: 'http://afrh.adamcfcox.com/geoserver/zonemaps/wms/',
                    params: {
                        'LAYERS': 'zonemaps:char_areas_map2',
                        'TILED': true,
                    },
                    serverType: 'geoserver'
                }),
            }),
            new ol.layer.Tile({
                name: 'char_areas',
                source: new ol.source.TileWMS({
                    url: 'http://afrh.adamcfcox.com/geoserver/zonemaps/wms/',
                    params: {
                        'LAYERS': 'zonemaps:circ_character_area',
                        'TILED': true,
                    },
                    serverType: 'geoserver'
                }),
            }),
        ],
        visible: false,
        is_arches_layer: "nobutclose",
    });
    
    var char_areas = new LayerModel({
        name: 'Character Areas',
        categories: ["Reference"],
        icon: 'fa fa-bookmark-o',
        infoContent: "Showing the character areas at the AFRH.<br><b>The following Character Areas are <em>not</em> shown here:</b> Circulation System, Recurring Resources, and Spatial Patterns.",
        onMap: true,
        active: false,
        layer: char_area_lyr_group,
    });
    
    var mp_zones = new LayerModel({
        name: 'Master Plan Zones',
        categories: ["Reference"],
        icon: 'fa fa-bookmark-o',
        infoContent: "Showing the master plan zones at the AFRH",
        onMap: true,
        active: false,
        layer: new ol.layer.Tile({
            visible: false,
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
    
    var mp_zones = new LayerModel({
        name: 'Master Plan Zones',
        categories: ["Reference"],
        icon: 'fa fa-bookmark-o',
        infoContent: "Showing the master plan zones at the AFRH",
        onMap: true,
        active: false,
        layer: new ol.layer.Tile({
            visible: false,
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
    
    layers.push(
        char_areas,
        mp_zones,
        arch_zones
    );

    return layers;
});
