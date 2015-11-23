define(['jquery', 
    'underscore', 
    'knockout-mapping', 
    'views/forms/base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], 
    function ($, _, ko, koMapping, BaseForm, BranchList) {
        return BaseForm.extend({
            initialize: function() {
                console.log("initial");
                BaseForm.prototype.initialize.apply(this);                
                console.log("initial +1");
                var self = this;
                var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $(this).find('input').trigger('change'); 
                });

                // var currentEditedClassification = this.getBlankFormData();

                // this.editClassification = function(branchlist){
                    // self.switchBranchForEdit(branchlist);
                // }
                // this.deleteClassification = function(branchlist){
                    // self.deleteClicked(branchlist);
                // }
                // ko.applyBindings(this, this.$el.find('#heritage_type_section')[0]);

                // console.log("1");
                // this.addBranchList(new BranchList({                   
                    // data: currentEditedClassification,
                    // dataKey: 'PHASE_TYPE_ASSIGNMENT.E17',
                // }));
                // console.log("2");
                // this.addBranchList(new BranchList({
                    // el: this.$el.find('#heritage-type-section')[0],
                    // data: this.data,
                    // dataKey: 'PRODUCTION.E12',
                    // validateBranch: function (nodes) {
                        // return true;
                    // }
                // }));
                console.log("before");
                this.addBranchList(new BranchList({
                    el: this.$el.find('#heritage-type-section')[0],
                    data: this.data,
                    dataKey: 'HERITAGE_RESOURCE_GROUP_TYPE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
                console.log("after");
                // this.addBranchList(new BranchList({
                    // el: this.$el.find('#heritage-type-use-dropdown')[0],
                    // data: currentEditedClassification,
                    // dataKey: 'HERITAGE_RESOURCE_GROUP_USE_TYPE.E55',
                    // validateBranch: function (nodes) {
                        // return true;
                    // }
                // }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#names-section')[0],
                    data: this.data,
                    dataKey: 'NAME.E41',
                    validateBranch: function (nodes) {
                        var valid = true;
                        var primaryname_count = 0;
                        var primaryname_conceptid = this.viewModel.primaryname_conceptid;
                        _.each(nodes, function (node) {
                            if (node.entitytypeid === 'NAME.E41') {
                                if (node.value === ''){
                                    valid = false;
                                }
                            }
                            if (node.entitytypeid === 'NAME_TYPE.E55') {
                                if (node.value === primaryname_conceptid){
                                    _.each(self.viewModel['branch_lists'], function (branch_list) {
                                        _.each(branch_list.nodes, function (node) {
                                            if (node.entitytypeid === 'NAME_TYPE.E55' && node.value === primaryname_conceptid) {
                                                valid = false;
                                            }
                                        }, this);
                                    }, this);
                                }
                            }
                        }, this);
                        return valid;
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#dates-section')[0],
                    data: this.data,
                    dataKey: 'important_dates',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#subjects-section')[0],
                    data: this.data,
                    dataKey: 'KEYWORD.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
            },
            
            // prepareData: function(assessmentNode){
                // _.each(assessmentNode, function(value, key, list){
                    // assessmentNode[key].domains = this.data.domains;
                // }, this);
                // return assessmentNode;
            // },
            
            // getBlankFormData: function(){
                // return this.prepareData({
                    // 'HERITAGE_RESOURCE_GROUP_TYPE.E55': {
                        // 'branch_lists':[]
                    // },
                    // 'HERITAGE_RESOURCE_GROUP_USE_TYPE.E55': {
                        // 'branch_lists':[]
                    // },
                    // 'PHASE_TYPE_ASSIGNMENT.E17': {
                        // 'branch_lists':[]
                    // }
                // });
            // },
        });
    }
);