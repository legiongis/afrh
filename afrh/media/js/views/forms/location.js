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
            var resourcetypeid = $('#resourcetypeid').val();
            var includeMap = (resourcetypeid !== 'ACTOR.E39');
            var includeAdminAreas = (resourcetypeid !== 'ACTOR.E39');
            var includeParcels = !_.contains(['ACTOR.E39', 'ACTIVITY.E7', 'HISTORICAL_EVENT.E5'], resourcetypeid);
            var adminAreaTypeLookup = {};

            BaseForm.prototype.initialize.apply(this);

            //_.each(this.data["ADMINISTRATIVE_SUBDIVISION.E48"].domains["ADMINISTRATIVE_SUBDIVISION_NAME.E55"], function (typeRecord) {
            //    adminAreaTypeLookup[typeRecord.text] = typeRecord.id;
            //});

            // if (includeAdminAreas) {
                // var adminAreaBranchList = new BranchList({
                    // el: this.$el.find('#admin-area-section')[0],
                    // data: this.data,
                    // dataKey: 'ADMINISTRATIVE_SUBDIVISION_NAME.E55'
                // });
                // this.addBranchList(adminAreaBranchList);
            // }

            if (includeMap) {
                var locationBranchList = new LocationBranchList({
                    el: this.$el.find('#geom-list-section')[0],
                    data: this.data,
                    dataKey: 'SPATIAL_COORDINATES_GEOMETRY.E47'
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

            this.addBranchList(new BranchList({
                el: this.$el.find('#address-section')[0],
                data: this.data,
                dataKey: 'PLACE_ADDRESS.E45'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION_OF_LOCATION.E62',
                singleEdit: true
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#character-area-section')[0],
                data: this.data,
                dataKey: 'CHARACTER_AREA.E44',
                validateBranch: function(nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#master-plan-zone-section')[0],
                data: this.data,
                dataKey: 'MASTER_PLAN_ZONE.E44',
                validateBranch: function(nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#archaeological-zone-section')[0],
                data: this.data,
                dataKey: 'ARCHAEOLOGICAL_ZONE.E44',
                validateBranch: function(nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
        }
    });
});