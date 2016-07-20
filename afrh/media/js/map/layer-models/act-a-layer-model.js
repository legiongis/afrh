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

            var polyStyle = function(feature, resolution) {
                var mouseOver = feature.get('mouseover');
                var text = '1 ' + mouseOver;

                if (!feature.get('arches_marker')) {
                    feature.set('arches_marker', true);
                }

                if (styleCache[text]) {
                    return styleCache[text];
                }
                
                var iconSize = mouseOver ? 38 : 32;
                
                var apeStyle = [
                    new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b + ',0.25)',
                            width: 6,
                            lineDash: [5, 8],
                        }),
                        zIndex: mouseOver ? zIndex*1000000000: zIndex
                    }),new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b + ',0.9)',
                            width: 2,
                            lineDash: [5, 8],
                        }),
                        zIndex: mouseOver ? zIndex*2000000000: zIndex
                    })
                ]
                
                var paStyle = [
                    new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b + ',0.25)',
                            width: 8
                        }),
                        zIndex: mouseOver ? zIndex*1000000000: zIndex
                    }),new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b + ',0.9)',
                            width: 2
                        }),
                        zIndex: mouseOver ? zIndex*2000000000: zIndex
                    })
                ];
                
                zIndex += 2;

                styleCache[text] = styles;
                
                var featType = feature.get('type');

                if (featType == "Project Area") {
                    var styles = paStyle;
                }
                if (featType == "Area of Potential Effect") {
                    var styles = apeStyle;
                }
                return styles;
            };

            var layerConfig = {
                projection: 'EPSG:3857',
                url: arches.urls.act_a_layer
                
            };

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
                style: polyStyle,
                visible: config.entitytypeid == "INVENTORY_RESOURCE.E18",
                is_arches_layer: true,
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