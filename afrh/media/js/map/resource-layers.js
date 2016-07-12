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
        'resource-types',
        'user-info'

], function(ol, _, ko, arches, resourceLayerInfo, MarkerLayerModel, FullLayerModel, PolygonLayerModel, AreaLayerModel, ArchLayerModel, resourceTypes, userInfo) {
        var resourceFeatures = ko.observableArray();
        var layers = [];
        
        var layerModelMap = {
            'area':AreaLayerModel,
            'poly':PolygonLayerModel,
            'marker':MarkerLayerModel,
            'arch':ArchLayerModel,
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

            //select which layer model to use based on resource type layer_model value
            var newLayerModel = layerModelMap[item.layerModel];
            
            if (entitytypeid == "ARCHAEOLOGICAL_ZONE.E53"){
                item.infoContent = true;
            }

            layers.push(new newLayerModel(item, function(features) {
                resourceFeatures(resourceFeatures().concat(features));
            }));
            
        });
        
        
        return {
            layers: layers,
            features: resourceFeatures
        };
});