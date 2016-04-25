define([
    'jquery',
    'underscore',
    'arches',
    'knockout', 
    'knockout-mapping', 
    'views/forms/base',
    'views/forms/sections/branch-list',
    'views/forms/sections/location-branch-list',
    'summernote'
], function ($, _, arches, ko, koMapping, BaseForm, BranchList, LocationBranchList) {
    return BaseForm.extend({
        initialize: function() {

            var self = this;
            BaseForm.prototype.initialize.apply(this);
            var resourcetypeid = $('#resourcetypeid').val();
            
            var locationBranchList = new LocationBranchList({
                el: this.$el.find('#geom-list-section')[0],
                data: this.data,
                dataKey: 'AREA_OF_PROBABILITY_GEOMETRY.E47'
            });
            
            locationBranchList.on('geometrychange', function(feature, wkt) {
                $.ajax({
                    url: arches.urls.get_admin_areas + '?geom=' + wkt,
                    success: function (response) {
                        _.each(response.results, function(item) {
                            var duplicate = false;
                            _.each(adminAreaBranchList.viewModel.branch_lists(), function(branch) {
                                var sameName = false;
                                var sameType = false;
                                _.each(branch.nodes(), function (node) {
                                    if (node.entitytypeid() === "CHARACTER_AREA.E44" &&
                                        node.label() === item.overlayty) {
                                        sameType = true;
                                    }
                                    if (node.entitytypeid() === "CHARACTER_AREA.E44" &&
                                        node.value() === item.overlayval) {
                                        sameName = true;
                                    }
                                });
                                if (sameName && sameType) {
                                    duplicate = true;
                                }
                            });
                            // adminAreaBranchList.viewModel.branch_lists
                            if (adminAreaTypeLookup[item.overlayty] && !duplicate) {
                                adminAreaBranchList.viewModel.branch_lists.push(koMapping.fromJS({
                                    'editing':ko.observable(false),
                                    'nodes': ko.observableArray([
                                        koMapping.fromJS({
                                          "property": "",
                                          "entitytypeid": "CHARACTER_AREA.E44",
                                          "entityid": "",
                                          "value": adminAreaTypeLookup[item.overlayty],
                                          "label": item.overlayty,
                                          "businesstablename": "",
                                          "child_entities": []
                                        }),
                                        koMapping.fromJS({
                                          "property": "",
                                          "entitytypeid": "CHARACTER_AREA.E44",
                                          "entityid": "",
                                          "value": item.overlayval,
                                          "label": "",
                                          "businesstablename": "",
                                          "child_entities": []
                                        })
                                    ])
                                }));
                            }
                        });
                    }
                })
            });
            
            this.addBranchList(locationBranchList);

        }
    });
});