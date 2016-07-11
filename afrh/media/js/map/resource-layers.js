define([
        'openlayers',
        'underscore',
        'knockout',
        'arches',
        'resource-layer-info',
        'map/resource-layer-model',
        'map/layer_models/marker-layer-model',
        'map/layer_models/full-layer-model',
        'map/layer_models/polygon-layer-model',
        'map/layer_models/area-layer-model',
        'map/layer_models/arch-layer-model',
        'map/layer_models/arch-investigation-layer-model',
        'resource-types',
        'user-info'

], function(ol, _, ko, arches, resourceLayerInfo, ResourceLayerModel, MarkerLayerModel, FullLayerModel, PolygonLayerModel, AreaLayerModel, ArchLayerModel, ArchInvestigationModel, resourceTypes, userInfo) {
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
                item.infoContent = "this is the content";
            }

            layers.push(new newLayerModel(item, function(features) {
                resourceFeatures(resourceFeatures().concat(features));
            }));
            
            if (entitytypeid == "ARCHAEOLOGICAL_ZONE.E53"){
                item.infoContent = "this is the content";
                arch_invest_item = {
                    'active':false,
                    'color':"#f600f1",
                    'defaultDescription':"no description available",
                    'description':"this is description property speaking",
                    'descriptionNode':"ACTIVITY_SCOPE_OF_WORK_DESCRIPTION.E62",
                    'entitytypeid':"ACTIVITY_B.E7",
                    'fillColor':"#c8b2a3",
                    'icon':"fa fa-clipboard",
                    'iconColor':"#f600f1",
                    'id':"ARCHEOLOGICAL_ZONE_INVESTIGATION",
                    'infoContent':"",
                    'layerModel':"marker",
                    'makeLayer':true,
                    'name':"Field Investigations",
                    'onMap':true,
                    'restricted':true,
                    'strokeColor':"#a7673d",
                    'vectorColor':"#a44b0f"
                }

                var arch_invest_layer = new ArchInvestigationModel(
                    arch_invest_item, function(features) {
                    resourceFeatures(resourceFeatures().concat(features));
                });

                layers.push(arch_invest_layer);
            }
        });
        
        
        return {
            layers: layers,
            features: resourceFeatures
        };
});