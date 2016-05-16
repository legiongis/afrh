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

                if (feature.get('type') == 'boundary'){
                    var thickcolor = 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b + ',0.25)';
                    var thincolor = 'rgba(' + strokergb.r + ',' + strokergb.g + ',' + strokergb.b + ',0.9)';
                } else {
                    var thickcolor = 'rgba(45,11,244,0.25)';
                    var thincolor = 'rgba(45,11,244,0.9)';
                };

                var styles = [
                    new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: thickcolor,
                            width: 8
                        }),
                        zIndex: mouseOver ? zIndex*1000000000: zIndex
                    }),new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: thincolor,
                            width: 2
                        }),
                        zIndex: mouseOver ? zIndex*2000000000: zIndex
                    })
                ];
                
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
            
            var boundaryLayer = new ol.layer.Vector({
                source: json_source,
                style: superStyle,
                visible: false,
            });
            
            return boundaryLayer
        };
        
        return new LayerModel(_.extend({
                layer: layer,
                onMap: true,
                isArchesLayer: true
            }, config)
        );
    };
});