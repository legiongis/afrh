define(['jquery', 
    'underscore', 
    'knockout-mapping', 
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], 
    function ($, _, koMapping, BaseForm, ValidationTools, BranchList) {
        var vt = new ValidationTools;
        return BaseForm.extend({
            initialize: function() {
                BaseForm.prototype.initialize.apply(this);                
                
                var self = this;
                var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $(this).find('input').trigger('change'); 
                });


                this.addBranchList(new BranchList({
                    el: this.$el.find('#creation-date-section')[0],
                    data: this.data,
                    dataKey: 'TIME-SPAN_RESOURCE_CREATION_EVENT.E52',
                    validateBranch: function (nodes) {
                        var ck1 = vt.nodesHaveValues(nodes,['CREATION_FORMAT.E55']);
                        var ck2 = vt.isValidDate(nodes,['DATE_OF_CREATION.E50']);
                        return ck1 && ck2;
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#creator-section')[0],
                    data: this.data,
                    dataKey: 'CREATOR.E39',
                    validateBranch: function (nodes) {
                        return vt.nodesHaveValues(nodes, ['CREATOR_APPELLATION.E82','CREATOR_TYPE.E55']);
                    }
                }));
                

                this.addBranchList(new BranchList({
                    el: this.$el.find('#publishers-section')[0],
                    data: this.data,
                    dataKey: 'PUBLICATION_EVENT.E12',
                    validateBranch: function (nodes) {
                        var ck1 = vt.nodesHaveValues(nodes,['PUBLISHER_APPELLATION.E82']);
                        var ck2 = vt.isValidDate(nodes,['DATE_OF_PUBLICATION.E50']);
                        return ck1 && ck2;
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#rights-section')[0],
                    data: this.data,
                    dataKey: 'RIGHT_TYPE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
            }
        });
    }
);