define([
    'jquery',
    'backbone',
    'underscore',
    'openlayers',
    'arches',
    'map/base-layers',
    'map/historic-layers',
    'bootstrap'
], function($, Backbone, _, ol, arches, baseLayers, historicLayers) {
    return Backbone.View.extend({
        events: {
            'mousemove': 'handleMouseMove',
            'mouseout': 'handleMouseOut'
        },

        overlays: [],
        initialize: function(options) {
            var self = this;
            var projection = ol.proj.get('EPSG:3857');
            var layers = [];
            var dragAndDropInteraction = new ol.interaction.DragAndDrop({
                formatConstructors: [
                    ol.format.GPX,
                    ol.format.GeoJSON,
                    ol.format.IGC,
                    ol.format.KML,
                    ol.format.TopoJSON
                ]
            });

            _.extend(this, _.pick(options, 'overlays', 'enableSelection'));

            this.baseLayers = baseLayers;
            this.historicLayers = historicLayers;

            _.each(this.baseLayers, function(baseLayer) {
                layers.push(baseLayer.layer);
            });
            _.each(this.overlays, function(overlay) {
                layers.push(overlay);
            });
            _.each(this.historicLayers, function(historicLayer) {
                layers.push(historicLayer.layer);
            });

            console.log("pushed layers");

            dragAndDropInteraction.on('addfeatures', function(event) {
                var vectorSource = new ol.source.Vector({
                    features: event.features,
                    projection: event.projection
                });
                var vectorLayer = new ol.layer.Vector({
                    source: vectorSource,
                    style: new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: 'rgba(92, 184, 92, 0.5)'
                        }),
                        stroke: new ol.style.Stroke({
                            color: '#0ff',
                            width: 1
                        })
                    })
                });
                self.map.addLayer(vectorLayer);
                var view = self.map.getView();
                view.fitExtent(vectorSource.getExtent(), (self.map.getSize()));
                self.trigger('layerDropped', vectorLayer, event.file.name);
            });

            this.map = new ol.Map({
                layers: layers,
                interactions: ol.interaction.defaults({
                    altShiftDragRotate: false,
                    dragPan: false,
                    rotate: false,
                    mouseWheelZoom:false
                }).extend([new ol.interaction.DragPan({kinetic: null})]).extend([dragAndDropInteraction]),
                target: this.el,
                view: new ol.View({
                    extent: arches.mapDefaults.extent ? arches.mapDefaults.extent.split(',') : undefined,
                    center: [arches.mapDefaults.x, arches.mapDefaults.y],
                    zoom: arches.mapDefaults.zoom,
                    minZoom: arches.mapDefaults.minZoom,
                    maxZoom: arches.mapDefaults.maxZoom
                })
            });
            
            if (this.enableSelection) {
                this.select = new ol.interaction.Select({
                    condition: ol.events.condition.click,
                    style: function(feature, resolution) {
                        var isSelectFeature = _.contains(feature.getKeys(), 'select_feature');
                        var fillOpacity = isSelectFeature ? 0.3 : 0;
                        var strokeOpacity = isSelectFeature ? 0.9 : 0;
                        return [new ol.style.Style({
                            fill: new ol.style.Fill({
                                color: 'rgba(0, 255, 255, ' + fillOpacity + ')'
                            }),
                            stroke: new ol.style.Stroke({
                                color: 'rgba(0, 255, 255, ' + strokeOpacity + ')',
                                width: 3
                            }),
                            image: new ol.style.Circle({
                                radius: 10,
                                fill: new ol.style.Fill({
                                    color: 'rgba(0, 255, 255, ' + fillOpacity + ')'
                                }),
                                stroke: new ol.style.Stroke({
                                    color: 'rgba(0, 255, 255, ' + strokeOpacity + ')',
                                    width: 3
                                })
                            })
                        })];
                    }
                });
                this.map.addInteraction(this.select);
            }

            this.map.on('moveend', function () {
                var view = self.map.getView();
                var extent = view.calculateExtent(self.map.getSize());
                self.trigger('viewChanged', view.getZoom(), extent);
            });
            
            // turn off basemap if max zoom level is exceeded, important to allow
            // the viewing of certain historic maps without the bad basemap underneath
            var switched = '';
            this.map.getView().on('change:resolution', function() {
                var zoomlevel = self.map.getView().getZoom()
                _.each(self.baseLayers, function(baseLayer){
                    if (baseLayer.layer.getVisible() == true && zoomlevel > baseLayer.maxzoom){
                        switched = baseLayer.id
                        baseLayer.layer.setVisible(false);
                    }
                    if (switched == baseLayer.id){
                        baseLayer.layer.setVisible(zoomlevel <= baseLayer.maxzoom);
                        self.baseLayers[6].layer.setVisible(zoomlevel > baseLayer.maxzoom);
                    }

                });
            });

            this.map.on('click', function(e) {
                var clickFeature = self.map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
                    return feature;
                });
                self.trigger('mapClicked', e, clickFeature);
            });
        },

        handleMouseMove: function(e) {
            var self = this;
            // see http://stackoverflow.com/questions/12704686/html5-with-jquery-e-offsetx-is-undefined-in-firefox
            if(e.offsetX==undefined) {
                // this works in Firefox
                xpos = e.pageX-$('#map').offset().left;
                ypos = e.pageY-$('#map').offset().top;
            } else { 
                // works in Chrome, IE and Safari
                xpos = e.offsetX;
                ypos = e.offsetY;
            }
            var pixels = [xpos, ypos];
            var coords = this.map.getCoordinateFromPixel(pixels);
            var point = new ol.geom.Point(coords);
            var format = ol.coordinate.createStringXY(4);
            var overFeature = this.map.forEachFeatureAtPixel(pixels, function (feature, layer) {
                return feature;
            });
            coords = point.transform("EPSG:3857", "EPSG:4326").getCoordinates();
            // swap order of coords so that they read "lat, long" not "long, lat"
            var coords_latlong = [Number(coords[1]), Number(coords[0])];
            if (coords.length > 0) {
                this.trigger('mousePositionChanged', format(coords_latlong), pixels, overFeature);
            } else {
                this.trigger('mousePositionChanged', '');
            }
        },

        handleMouseOut: function () {
            this.trigger('mousePositionChanged', '');
        }
    });
});