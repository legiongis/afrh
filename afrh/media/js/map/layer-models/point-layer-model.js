define([
    'jquery',
    'openlayers',
    'underscore',
    'arches',
    'map/layer-models/base-layer-model',
    'utils'
], function($, ol, _, arches, LayerModel, utils) {
    return function(config, featureCallback) {
        config = _.extend({
            entitytypeid: 'all',
            vectorColor: '#808080'
        }, config);

        var layer = function () {
            var fillrgb = utils.hexToRgb(config.fillColor);
            var strokergb = utils.hexToRgb(config.strokeColor);
            var zIndex = 0;
            var styleCache = {};

            var pointStyle = function(feature, resolution) {
                var mouseOver = feature.get('mouseover');
                var text = '1 ' + mouseOver;

                if (!feature.get('arches_marker')) {
                    feature.set('arches_marker', true);
                }

                if (styleCache[text]) {
                    return styleCache[text];
                }
                
                var iconSize = mouseOver ? 38 : 32;

                var stStyle = [
                    new ol.style.Style({
                        image: new ol.style.Circle({
                            radius: 3,
                            fill: new ol.style.Fill({
                              color: '#000000',
                              opacity: 0.6
                            }),
                            stroke: new ol.style.Stroke({
                              color: '#ffffff',
                              opacity: 0.4
                            })
                       })
                    })
                ];
                
                zIndex += 2;

                styleCache[text] = stStyle;
                return stStyle;
            };

            var layerConfig = {
                projection: 'EPSG:3857'
            };
            
            if (config.entitytypeid !== null) {
                layerConfig.url = arches.urls.polygon_layers + config.entitytypeid;
            }

            json_source = new ol.source.GeoJSON(layerConfig)
            
            $('.map-loading').show();
            var loadListener = json_source.on('change', function(e) {
                if (json_source.getState() == 'ready') {
                    if(typeof(featureCallback) === 'function'){
                        featureCallback(json_source.getFeatures());
                    }
                    ol.Observable.unByKey(loadListener);
                    $('.map-loading').hide();
                }
            });
            
            output_layer = new ol.layer.Vector({
                source: json_source,
                style: pointStyle,
                visible: config.entitytypeid == "INVENTORY_RESOURCE.E18",
                is_arches_layer: true,
                name: config.entitytypeid,
            });
            return output_layer
        };
        
        return new LayerModel(_.extend({
                layer: layer,
                onMap: true,
                isArchesLayer: true
            }, config)
        );
    };
});