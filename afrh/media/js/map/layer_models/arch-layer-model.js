define([
    'jquery',
    'openlayers',
    'underscore',
    'arches',
    'map/layer-model',
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
            // var styleCache = {};
            
            var superStyle = function(feature, resolution) {
                var mouseOver = feature.get('mouseover');
                var text = '1 ' + mouseOver;

                if (!feature.get('arches_marker')) {
                    feature.set('arches_marker', true);
                }

                // if (styleCache[text]) {
                    // return styleCache[text];
                // }
                
                var iconSize = mouseOver ? 38 : 32;

                var featType = feature.get('type');
                
                var boundStyle = [
                    new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b+',0.25)',
                            width: 8,
                        }),
                        zIndex: mouseOver ? zIndex*1000000000: zIndex
                    }),new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b+',0.9)',
                            width: 2,
                        }),
                        zIndex: mouseOver ? zIndex*2000000000: zIndex
                    })
                ];
                
                var probColors = {
                    'Historic Resources':'rgba(255, 255, 0',
                    'Native American Resources':'rgba(255, 88, 0',
                    'Paleosols':'rgba(202, 0, 224',
                    'Disturbed Area':'rgba(255, 0, 8',
                };

                var probStyle = [
                    new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: probColors[featType]+',0.25)',
                            width: 6,
                            lineDash: [5, 8],
                        }),
                        zIndex: mouseOver ? zIndex*1000000000: zIndex
                    }),new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: probColors[featType]+',0.9)',
                            width: 2,
                            lineDash: [5, 8],
                        }),
                        zIndex: mouseOver ? zIndex*2000000000: zIndex
                    })
                ];
                
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
                
                if (featType == 'boundary') {
                    var styles = boundStyle;
                } else {
                    if (featType == 'shovel test') {
                        var styles = stStyle;
                    } else {
                        var styles = probStyle;
                    }
                } 

                zIndex += 2;

                // styleCache[text] = styles;
                return styles;
            };

            json_source = new ol.source.GeoJSON({
                projection: 'EPSG:3857',
                url: arches.urls.arch_layer
            });

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
            
            var arch_layer = new ol.layer.Vector({
                source: json_source,
                style: superStyle,
                visible: false,
                is_arches_layer: true,
            });

            return arch_layer
        };
        
        return new LayerModel(_.extend({
                layer: layer,
                onMap: true,
                isArchesLayer: true
            }, config)
        );
    };
});