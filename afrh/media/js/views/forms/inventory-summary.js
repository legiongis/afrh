define(['jquery', 
    'underscore', 
    'knockout-mapping',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], 
    function ($, _, koMapping, BaseForm, ValidationTools, BranchList) {
        
        //load all validation functions stored in views/forms/sections/validation.js
        var vt = new ValidationTools;
        
        return BaseForm.extend({
            
            initialize: function() {

                BaseForm.prototype.initialize.apply(this);                
                
                var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $(this).find('input').trigger('change'); 
                });

                this.addBranchList(new BranchList({
                    el: this.$el.find('#nrhp-type-section')[0],
                    data: this.data,
                    dataKey: 'NRHP_RESOURCE_TYPE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }//,
                    // onSelect2Selecting: function(item, select2Config){
                    //     _.each(this.editedItem(), function(node){
                    //         if (node.entitytypeid() === select2Config.dataKey){
                    //             var labels = node.label().split(',');
                    //             if(node.label() === ''){
                    //                 node.label(item.value);
                    //             }else{
                    //                 if(item.value !== ''){
                    //                     labels.push(item.value);
                    //                 }
                    //                 node.label(labels.join());
                    //             }
                    //             //node.value(item.id);
                    //             node.entitytypeid(item.entitytypeid);
                    //         }
                    //     }, this);
                    //     this.trigger('change', 'changing', item);
                    //}
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#nrhp-category-section')[0],
                    data: this.data,
                    dataKey: 'NRHP_RESOURCE_CATEGORY.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#resource-subcategory-section')[0],
                    data: this.data,
                    dataKey: 'NRHP_RESOURCE_SUBCATEGORY.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#wuzit-section')[0],
                    data: this.data,
                    dataKey: 'WUZIT.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#names-section')[0],
                    data: this.data,
                    dataKey: 'NAME.E41',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                        // the validation below almost works but not quite. so it's ignored for now.
                        var valid = true;
                        var primaryname_conceptid = this.data['primaryname_conceptid'];
                        _.each(nodes, function (node) {
                            if (node.entitytypeid === 'NAME.E41') {
                                if (node.value === ''){
                                    valid = false;
                                }
                            }
                            if (node.entitytypeid === 'NAME_TYPE.E55') {
                                if (node.value === primaryname_conceptid){
                                    _.each(this.data['NAME.E41']['branch_lists'], function (branch_list) {
                                        _.each(branch_list.nodes, function (node) {
                                            console.log(node.value);
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
                    el: this.$el.find('#building-number-section')[0],
                    data: this.data,
                    dataKey: 'BUILDING_NUMBER.E42',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#dates-section')[0],
                    data: this.data,
                    dataKey: 'important_dates',
                    validateBranch: function (nodes) {
                        var ck1 = vt.isValidDate(nodes, 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49');
                        var ck2 = vt.nodesHaveValues(nodes, ['START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49','BEGINNING_OF_EXISTENCE_TYPE.E55,END_OF_EXISTENCE_TYPE.E55','BEGINNING_OF_EXISTENCE_TYPE.E55','END_OF_EXISTENCE_TYPE.E55']);
                        return ck1 == true && ck2 == true;
                    }
                }));
            }
        });
    }
);