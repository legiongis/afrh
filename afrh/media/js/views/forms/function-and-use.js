define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',
    'summernote'],
    function ($, _, ko, BaseForm, ValidationTools, BranchList, datetimepicker, summernote) {
        
        var vt = new ValidationTools;
        return BaseForm.extend({

            initialize: function() {
                
                BaseForm.prototype.initialize.apply(this);
                var self = this;
                
                //date picker code
                var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $(this).find('input').trigger('change'); 
                });

                this.addBranchList(new BranchList({
                    el: this.$el.find('#function-section')[0],
                    data: this.data,
                    dataKey: 'PHASE_TYPE_ASSIGNMENT.E17',
                    validateBranch: function (nodes) {
                        var chk1 = vt.isValidDate(nodes, 'FROM_DATE.E49');
                        var chk2 = vt.isValidDate(nodes, 'TO_DATE.E49');
                        var chk3 = vt.nodesHaveValues(nodes, ['FUNCTION.E62','FUNCTION_PERIOD.E55']);
                        return chk1 == true && chk2 == true && chk3 == true;
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#current-use-section')[0],
                    data: this.data,
                    dataKey: 'HERITAGE_ASSET_REPORT.E3',
                    validateBranch: function (nodes) {
                        var chk1 = vt.isValidDate(nodes, 'HERITAGE_ASSET_REPORT_DATE.E49');
                        var chk2 = vt.nodesHaveValues(nodes, ['CURRENT_USER.E39','CURRENT_OPERATION_STATUS.E55','HERITAGE_ASSET_REPORT_DATE.E49']);
                        return chk1 == true && chk2 == true;
                    }
                }));
            }
        });
    }
);
        
