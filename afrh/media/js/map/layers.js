define([
    'openlayers',
    'map/resource-layers',
    'map/layer-models/base-layer-model',
], function(ol, resourceLayers, LayerModel) {
    var layers = resourceLayers.layers;

    layers.push();

    return layers;
});
