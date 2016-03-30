define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',
    'summernote'],
    function ($, _, ko, BaseForm, BranchList, datetimepicker, summernote) {
    
        //insert validation functions here
        
        return BaseForm.extend({

            initialize: function() {
                BaseForm.prototype.initialize.apply(this);
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#current-use-section')[0],
                    data: this.data,
                    dataKey: 'CURRENT_HERITAGE_ASSET_STATE.E3',
                    validateBranch: function (nodes) {
                        return true;
                        return this.validateHasValues(nodes);
                    }
                }));
            }
        });
    }
);
