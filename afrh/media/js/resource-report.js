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
            
            var resource_geometry = $('#resource_geometry');
            console.log(resource_geometry.length);
            if(resource_geometry.length > 0){

                var geom = JSON.parse(resource_geometry.val());
                this.map = new MapView({
                    el: $('#map')
                });

                ko.applyBindings(this.map, $('#basemaps-panel')[0]);
                ko.applyBindings(this.map, $('#historicmaps-panel')[0]);
                
                // set this level so the feature will always be on top of the historic map layers
                featlvl = this.map.historicLayers.length + this.map.baseLayers.length + 1;
                this.highlightFeatures(geom,featlvl);
                this.zoomToResource('1');
                
                var hideAllPanels = function(){
                    $("#basemaps-panel").addClass("hidden");
                    $("#historicmaps-panel").addClass("hidden");

                    //Update state of remaining buttons
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

                        //Update state of current button and adjust position
                        $("#inventory-basemaps")
                            .addClass("arches-map-tools-pressed")
                            .removeClass("arches-map-tools")
                            //.css("border-bottom-left-radius", "5px");
                    }
                });
                
                $("#inventory-historicmaps").click(function (){
                    if ($(this).hasClass('arches-map-tools-pressed')) {
                        hideAllPanels();
                    } else {
                        $("#historicmaps-panel").removeClass("hidden");
                        $("#basemaps-panel").addClass("hidden");

                        //Update state of current button and adjust position
                        $("#inventory-historicmaps")
                            .addClass("arches-map-tools-pressed")
                            .removeClass("arches-map-tools")
                            //.css("border-bottom-left-radius", "5px");
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
                    self.highlightFeatures(geom);
                });

                //Close Button
                $(".close").click(function (){ 
                    hideAllPanels();
                });
                
                $("#map").click(function (){
                    hideAllPanels();
                });
               
            }else{
                $('#map-container').hide();
            }

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
            var feature = this.selectedFeatureLayer.getSource().getFeatureById(resourceid);
            if(feature.getGeometry().getGeometries().length > 1){
                var extent = feature.getGeometry().getExtent();
                var minX = extent[0];
                var minY = extent[1];
                var maxX = extent[2];
                var maxY = extent[3];
                var polygon = new ol.geom.Polygon([[[minX, minY], [maxX, minY], [maxX, maxY], [minX, maxY], [minX, minY]]]);
                this.map.map.getView().fitGeometry(polygon, this.map.map.getSize(), {maxZoom:18}); 
            }else{
                this.map.map.getView().fitGeometry(feature.getGeometry().getGeometries()[0], this.map.map.getSize(), {maxZoom:18});                    
            }
        },

        highlightFeatures: function(geometry,lvl){
            var source, geometries;
            var self = this;
            var f = new ol.format.GeoJSON({defaultDataProjection: 'EPSG:4326'});

            if(!this.selectedFeatureLayer){
                var zIndex = 100;
                var styleCache = {};

                var style = function(feature, resolution) {
                    return [new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: 'rgba(66, 139, 202, 0.4)'
                        }),
                        stroke: new ol.style.Stroke({
                            color: 'rgba(66, 139, 202, 0.9)',
                            width: 2
                        }),
                        image: new ol.style.Circle({
                            radius: 10,
                            fill: new ol.style.Fill({
                                color: 'rgba(66, 139, 202, 0.4)'
                            }),
                            stroke: new ol.style.Stroke({
                                color: 'rgba(66, 139, 202, 0.9)',
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

            feature = {
                'type': 'Feature',
                'id': '1',
                'geometry':  geometry
            };

            this.selectedFeatureLayer.getSource().addFeature(f.readFeature(feature, {featureProjection: 'EPSG:3857'}));
        }
    });

    var rv = new ReportView();
    //rv.showRelatedResourcesGraph();
});
