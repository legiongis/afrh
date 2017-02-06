define([
        'openlayers',
        'underscore',
        'knockout',
        'arches',
        'resource-layer-info',
        'map/layer-models/marker-layer-model',
        'map/layer-models/full-layer-model',
        'map/layer-models/polygon-layer-model',
        'map/layer-models/area-layer-model',
        'map/layer-models/arch-layer-model',
        'map/layer-models/point-layer-model',
        'map/layer-models/act-a-layer-model',
        'resource-types',
        'user-info'

], function(ol, _, ko, arches, resourceLayerInfo, MarkerLayerModel, FullLayerModel, PolygonLayerModel, AreaLayerModel, ArchLayerModel, PointLayerModel, ActALayerModel, resourceTypes, userInfo) {
        var resourceFeatures = ko.observableArray();
        var layers = [];
        
        var layerModelMap = {
            'area':AreaLayerModel,
            'poly':PolygonLayerModel,
            'marker':MarkerLayerModel,
            'arch':ArchLayerModel,
            'point':PointLayerModel,
            'act-a':ActALayerModel,
        }
        
        _.each(resourceTypes, function (item, entitytypeid) {
            
            //exclude if not mappy resource
            if (item.makeLayer == false){return true;}
            
            //exclude based on user permissions
            if (userInfo.name != 'anonymous'){
                if (userInfo.view[entitytypeid] == false){return true;}
            } else {
                if (item.restricted){return true;}
            }

            item.entitytypeid = entitytypeid;
            item.onMap = true;
            item.active = false;
            if (entitytypeid == "INVENTORY_RESOURCE.E18"){
                item.active = true;
            }
            
            // set infoContent to equal the HTML content of a legend div in map.htm
            if (entitytypeid == "ARCHAEOLOGICAL_ZONE.E53"){
                if (userInfo.name != 'anonymous') {
                    item.infoContent = $("#arch-legend").html();
                }
            }
            if (entitytypeid == "ACTIVITY_A.E7"){
                item.infoContent = $("#act-a-legend").html();
            }
            
            //select which layer model to use based on resource type layer_model value
            var newLayerModel = layerModelMap[item.layerModel];
            
            layers.push(new newLayerModel(item, function(features) {
                resourceFeatures(resourceFeatures().concat(features));
            }));
            
        });
        
        
        return {
            layers: layers,
            features: resourceFeatures
        };
});