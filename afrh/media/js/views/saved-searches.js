define(['jquery',
    'backbone',
    'underscore',
    'arches',
    'resource-types',
    'browse-info'], function($, Backbone, _, arches, resourceTypes, browseInfo) {
        console.log("loaded 1a");
        console.log(browseInfo["NHRP_RESOURCE_TYPE"]);
        console.log("loaded 2a");
        // _.each(browseInfo){
            // console.
        
        
        // var createURLs = function (input, name) {
            // $.each(input, function(){
                // var url = encodeURIComponent(String(input));
                // console.log(url);
            // });
        // }
        
        // createURLs(browseInfo["NHRP_RESOURCE_TYPE"]);
        
    return Backbone.View.extend({
        
        initialize: function(options) {
            console.log("loaded 1b");
            console.log(browseInfo);
            console.log("loaded 2b");
        },

    });
});
    