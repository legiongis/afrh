require([
    'jquery',
    'underscore',
    'arches',
    'bootstrap',
    'views/map',
    'views/related-resources-graph',
    'openlayers', 
    'knockout',
    'utils'
], function($, _, arches, bootstrap, MapView, RelatedResourcesGraph, ol, ko, utils) {
    
    var ReportView = Backbone.View.extend({

        initialize: function(options) {
 
            var resize;
            var self = this;
            var resourcetypeid = $('#resource_type').val();
            console.log(resourcetypeid);
            
            $(".section-toggle").click(function (){ 
                iconEl = $(this).find('i');
                sectionEl = $(this).closest('.report-section');
                contentEl = $(sectionEl).find('.report-content');
                if (contentEl.is(":visible")){
                    contentEl.hide("fast");
                } else {
                    contentEl.show("fast");
                }
                $(iconEl).toggleClass("fa-folder-open");
                $(iconEl).toggleClass("fa-folder");
            });
            
            if(resourcetypeid == "ACTIVITY_A.E7") {
                var pa_val = $('#pa_geometry').val();
                var ape_val = $('#ape_geometry').val();
                
                if(pa_val != 'null' || ape_val != 'null') {
                    
                    this.map = new MapView({
                        el: $('#map')
                    });

                    ko.applyBindings(this.map, $('#basemaps-panel')[0]);
                    ko.applyBindings(this.map, $('#historicmaps-panel')[0]);
                    
                    // set this level so the feature will always be on top of the historic map layers
                    if (pa_val != 'null') {
                        var pa_geom = JSON.parse(pa_val);
                        pa_lvl = this.map.historicLayers.length + this.map.baseLayers.length + 1;
                        //this.highlightFeatures(pa_geom,[16,199,272],pa_lvl);
                    } else {
                        var pa_geom = false;
                    }
                    
                    if (ape_val != 'null') {
                        var ape_geom = JSON.parse(ape_val);
                        ape_lvl = this.map.historicLayers.length + this.map.baseLayers.length + 2;
                        //this.highlightFeatures(ape_geom,[69,89,2],ape_lvl);
                    } else {
                        var ape_geom = false;
                    }
                    
                    this.displayProjectAreas(pa_geom,ape_geom,pa_lvl);
                    this.zoomToResource('1');
                }
            }
            
            if(resourcetypeid == "ARCHAEOLOGICAL_ZONE.E53") {
                
                var resource_geometry = $('#resource_geometry');
                if(resource_geometry.length > 0){
                    var geom = JSON.parse(resource_geometry.val());
                    this.map = new MapView({
                        el: $('#map')
                    });
                    featlvl = this.map.historicLayers.length + this.map.baseLayers.length + 1;

                    ko.applyBindings(this.map, $('#basemaps-panel')[0]);
                    ko.applyBindings(this.map, $('#historicmaps-panel')[0]);

                    this.highlightFeatures(geom,[66,139,202],featlvl);
                    this.zoomToResource('1');
                }
                
                var prob_hr = $('#prob_hr').val();
                var prob_na = $('#prob_na').val();
                var prob_p = $('#prob_p').val();
                var prob_da = $('#prob_da').val();
                
                if (prob_hr != 'null' || prob_na != 'null' || prob_p != 'null' || prob_da != 'null' || geom != 'null') {
                    
                    if (prob_hr != 'null') {
                        var hr_geom = JSON.parse(prob_hr);
                    } else {
                        var hr_geom = false;
                    }
                    
                    if (prob_na != 'null') {
                        var na_geom = JSON.parse(prob_na);
                    } else {
                        var na_geom = false;
                    }
                    
                    if (prob_p != 'null') {
                        var p_geom = JSON.parse(prob_p);
                    } else {
                        var p_geom = false;
                    }
                    console.log(JSON.parse(prob_da));
                    if (prob_da != 'null') {
                        var da_geom = JSON.parse(prob_da);
                        
                    } else {
                        var da_geom = false;
                    }

                    this.displayProbabilityAreas(hr_geom,na_geom,p_geom,da_geom,featlvl+1);
                }
            }

            var resource_geometry = $('#resource_geometry');
            if(resource_geometry.length > 0 && resourcetypeid != "ARCHAEOLOGICAL_ZONE.E53"){

                var geom = JSON.parse(resource_geometry.val());
                this.map = new MapView({
                    el: $('#map')
                });

                ko.applyBindings(this.map, $('#basemaps-panel')[0]);
                ko.applyBindings(this.map, $('#historicmaps-panel')[0]);
                
                // set this level so the feature will always be on top of the historic map layers
                featlvl = this.map.historicLayers.length + this.map.baseLayers.length + 1;
                this.highlightFeatures(geom,[66,139,202],featlvl);
                this.zoomToResource('1');
            }
            
            var hideAllPanels = function(){
                $("#basemaps-panel").addClass("hidden");
                $("#historicmaps-panel").addClass("hidden");
                $("#inventory-basemaps")
                    .removeClass("arches-map-tools-pressed")
                    .addClass("arches-map-tools")
                $("#inventory-historicmaps")
                    .removeClass("arches-map-tools-pressed")
                    .addClass("arches-map-tools")
            };

            //Inventory-basemaps button opens basemap panel
            $("#inventory-basemaps").click(function (){
                if ($(this).hasClass('arches-map-tools-pressed')) {
                    hideAllPanels();
                } else {
                    $("#basemaps-panel").removeClass("hidden");
                    $("#historicmaps-panel").addClass("hidden");
                    $("#inventory-basemaps")
                        .addClass("arches-map-tools-pressed")
                        .removeClass("arches-map-tools")
                }
            });
            
            $("#inventory-historicmaps").click(function (){
                if ($(this).hasClass('arches-map-tools-pressed')) {
                    hideAllPanels();
                } else {
                    $("#historicmaps-panel").removeClass("hidden");
                    $("#basemaps-panel").addClass("hidden");
                    $("#inventory-historicmaps")
                        .addClass("arches-map-tools-pressed")
                        .removeClass("arches-map-tools")
                }
            });

            $(".basemap").click(function (){ 
                var basemap = $(this).attr('id');
                _.each(self.map.baseLayers, function(baseLayer){ 
                    baseLayer.layer.setVisible(baseLayer.id == basemap);
                });
                hideAllPanels();
            });
            
            // activate historic map when button is clicked, stays on until clicked again
            // historic map panel doesn't close automatically
            $(".historicmap").click(function (){
                var historicmap = $(this).attr('id');
                _.each(self.map.historicLayers, function(historicLayer){
                    if (historicLayer.id == historicmap){
                        historicLayer.layer.setVisible(!historicLayer.layer.getVisible());
                        // if activated, set layer on top of all historic maps/basemaps
                        // also highlight layer button by changing background
                        if (historicLayer.layer.getVisible() == true) {
                            setlyrs = self.map.historicLayers.length + self.map.baseLayers.length;
                            
                            self.map.map.removeLayer(historicLayer.layer);
                            self.map.map.getLayers().insertAt(setlyrs, historicLayer.layer);
                            
                            $('#'+historicLayer.id).css("background","#eaeaea");
                        } else {
                            $('#'+historicLayer.id).css("background","");
                        }
                    }
                });
            });

            //Close Button
            $(".close").click(function (){ 
                hideAllPanels();
            });
            
            $("#map").click(function (){
                hideAllPanels();
            });

            var resize = function() {
                var header = $('.breadcrumbs').outerHeight() + $('.header').outerHeight();
                $('#report-body').height($(window).height() - header);
            };            

            $('body').removeClass('scroll-y');
            resize();
            $(window).resize(resize); 

            _.each($('.report-item-list'), function(list) {
                if ($(list).find('.report-list-item').length === 0) {
                    $(list).find('.empty-message').show();
                }
            })
            
            var info_el = document.getElementById("report_info");
            if (info_el){
                self.showRelatedResourcesGraph()
            }
        },
        
        showRelatedResourcesGraph: function () {
            
            var info_el = document.getElementById("report_info");
            var graph_info = JSON.parse(info_el.getAttribute('value'));
            
            var section = document.getElementById("related-resources-graph-section");
            var graphPanel = $(section).find('.arches-related-resource-panel');
            var nodeInfoPanel = graphPanel.find('.node_info');
            if (!graphPanel.hasClass('view-created')) {
                new RelatedResourcesGraph({
                    el: graphPanel[0],
                    resourceId: graph_info['resourceid'],
                    resourceName: graph_info['primaryname'],
                    resourceTypeId: graph_info['entitytypeid']
                });
            }
            nodeInfoPanel.hide();
        },
        
        zoomToResource: function(resourceid){
            this.cancelFitBaseLayer = true;
            console.log(resourceid)
            var feature = this.selectedFeatureLayer.getSource().getFeatureById(resourceid);
            if(feature.getGeometry().getGeometries().length > 1){
                var extent = feature.getGeometry().getExtent();
                var minX = extent[0];
                var minY = extent[1];
                var maxX = extent[2];
                var maxY = extent[3];
                var polygon = new ol.geom.Polygon([[[minX, minY], [maxX, minY], [maxX, maxY], [minX, maxY], [minX, minY]]]);
                this.map.map.getView().fitGeometry(polygon, this.map.map.getSize(), {maxZoom:17}); 
            }else{
                this.map.map.getView().fitGeometry(feature.getGeometry().getGeometries()[0], this.map.map.getSize(), {maxZoom:17});
            }
        },
        
        displayProjectAreas: function(pa_geom,ape_geom,lvl){
            var self = this;
            var pa_lvl = lvl;
            var ape_lvl = lvl+1;
            var f = new ol.format.GeoJSON({defaultDataProjection: 'EPSG:4326'});
            
            if (pa_geom) {
                var pa_layer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: [new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: 'rgba(0, 255, 50, 0.4)',
                        }),
                        stroke: new ol.style.Stroke({
                            color: 'rgba(0, 255, 50, 0.9)',
                            width: 2
                        }),
                    })],
                    name: 'feature'
                });
                pa_feature = {
                    'type': 'Feature',
                    'id': '1',
                    'geometry':  pa_geom
                };
                pa_layer.getSource().addFeature(f.readFeature(pa_feature, {featureProjection: 'EPSG:3857'}))
                
                this.map.map.addLayer(pa_layer);
                this.map.map.getLayers().setAt(pa_lvl,pa_layer);
                this.selectedFeatureLayer = pa_layer;
            }
            
            if (ape_geom) {
                var ape_layer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: [new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(255, 0, 10, 0.9)',
                            width: 4,
                            lineDash: [5, 8]
                        }),
                    })],
                    name: 'feature'
                });
                ape_feature = {
                    'type': 'Feature',
                    'id': '2',
                    'geometry':  ape_geom
                };
                ape_layer.getSource().addFeature(f.readFeature(ape_feature, {featureProjection: 'EPSG:3857'}))
                
                this.map.map.addLayer(pa_layer);
                this.map.map.getLayers().setAt(ape_lvl,ape_layer);
            }
        },
        
        displayProbabilityAreas: function(hr_geom,na_geom,p_geom,da_geom,lvl){
            var self = this;
            var f = new ol.format.GeoJSON({defaultDataProjection: 'EPSG:4326'});
            
            if (hr_geom) {
                var hr_layer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: [new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(255, 255, 0, 0.9)',
                            width: 2.5,
                            lineDash: [5, 8]
                        }),
                    })],
                    name: 'feature'
                });
                hr_feature = {
                    'type': 'Feature',
                    'id': '1',
                    'geometry':  hr_geom
                };
                hr_layer.getSource().addFeature(f.readFeature(hr_feature, {featureProjection: 'EPSG:3857'}))
                
                this.map.map.addLayer(hr_layer);
                this.map.map.getLayers().setAt(lvl,hr_layer);
            }
            if (na_geom) {
                var na_layer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: [new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(255, 88, 0, 0.9)',
                            width: 2.5,
                            lineDash: [5, 8]
                        }),
                    })],
                    name: 'feature'
                });
                na_feature = {
                    'type': 'Feature',
                    'id': '1',
                    'geometry':  na_geom
                };
                na_layer.getSource().addFeature(f.readFeature(na_feature, {featureProjection: 'EPSG:3857'}))
                
                this.map.map.addLayer(na_layer);
                this.map.map.getLayers().setAt(lvl+2,na_layer);
            }
            if (p_geom) {
                var p_layer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: [new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(202, 0, 224, 0.9)',
                            width: 2.5,
                            lineDash: [5, 8]
                        }),
                    })],
                    name: 'feature'
                });
                p_feature = {
                    'type': 'Feature',
                    'id': '1',
                    'geometry':  p_geom
                };
                p_layer.getSource().addFeature(f.readFeature(p_feature, {featureProjection: 'EPSG:3857'}))
                
                this.map.map.addLayer(p_layer);
                this.map.map.getLayers().setAt(lvl+2,p_layer);
            }
            if (da_geom) {
                var da_layer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: [new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: 'rgba(255, 0, 8, 0.9)',
                            width: 2.5,
                            lineDash: [5, 8]
                        }),
                    })],
                    name: 'feature'
                });
                da_feature = {
                    'type': 'Feature',
                    'id': '1',
                    'geometry':  da_geom
                };
                da_layer.getSource().addFeature(f.readFeature(da_feature, {featureProjection: 'EPSG:3857'}))
                
                this.map.map.addLayer(da_layer);
                this.map.map.getLayers().setAt(lvl+3,da_layer);
            }
        },

        highlightFeatures: function(geometry,rgb,lvl){
            var source, geometries;
            var self = this;
            var f = new ol.format.GeoJSON({defaultDataProjection: 'EPSG:4326'});
            console.log(1);
            if(!this.selectedFeatureLayer){
                var zIndex = 100;
                var styleCache = {};
                console.log(2);
                var style = function(feature, resolution) {
                    return [new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: 'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+', 0.4)',
                        }),
                        stroke: new ol.style.Stroke({
                            color: 'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+', 0.9)',
                            width: 2
                        }),
                        image: new ol.style.Circle({
                            radius: 10,
                            fill: new ol.style.Fill({
                                color: 'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+', 0.4)',
                            }),
                            stroke: new ol.style.Stroke({
                                color: 'rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+', 0.9)',
                                width: 2
                            })
                        })
                    })];
                };                     
                this.selectedFeatureLayer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: style,
                    name: 'feature'
                });
                this.map.map.addLayer(this.selectedFeatureLayer);
                this.map.map.getLayers().setAt(lvl,this.selectedFeatureLayer);
            }
            this.selectedFeatureLayer.getSource().clear();
            console.log(3);
            feature = {
                'type': 'Feature',
                'id': '1',
                'geometry':  geometry
            };
            console.log(this.selectedFeatureLayer);
            console.log(this.selectedFeatureLayer.getSource());
            console.log(feature);
            //console.log(this.selectedFeatureLayer);
            this.selectedFeatureLayer.getSource().addFeature(f.readFeature(feature, {featureProjection: 'EPSG:3857'}));
            console.log(4);
        }
    });

    var rv = new ReportView();
});
