define(['jquery',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list'
    ], function ($, BaseForm, ValidationTools, BranchList) {
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
                    el: this.$el.find('#names-section')[0],
                    data: this.data,
                    dataKey: 'NAME.E41',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                        //not using the function below
                        // var valid = true;
                        // var primaryname_count = 0;
                        // var primaryname_conceptid = this.viewModel.primaryname_conceptid;
                        // _.each(nodes, function (node) {
                            // if (node.entitytypeid === 'NAME.E41') {
                                // if (node.value === ''){
                                    // valid = false;
                                // }
                            // }
                            // if (node.entitytypeid === 'NAME_TYPE.E55') {
                                // if (node.value === primaryname_conceptid){
                                    // _.each(self.viewModel['branch_lists'], function (branch_list) {
                                        // _.each(branch_list.nodes, function (node) {
                                            // if (node.entitytypeid === 'NAME_TYPE.E55' && node.value === primaryname_conceptid) {
                                                // valid = false;
                                            // }
                                        // }, this);
                                    // }, this);
                                // }
                            // }
                        // }, this);
                        // return valid;
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#actions-section')[0],
                    data: this.data,
                    dataKey: 'PHASE_TYPE_ASSIGNMENT.E17',
                    validateBranch: function (nodes) {
                        var ck1 = vt.isValidDate(nodes,'FROM_DATE.E49');
                        var ck2 = vt.isValidDate(nodes,'TO_DATE.E49');
                        var ck3 = vt.nodesHaveValues(nodes, ['ACTIVITY_TYPE.E55']);
                        return ck1 == true && ck2 == true && ck3 == true;
                    }
                }));
            }
        });
});


