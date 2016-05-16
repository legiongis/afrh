define(['jquery',
    'summernote',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], function ($, summernote, BaseForm, ValidationTools, BranchList) {
        
    var vt = new ValidationTools;
    
    return BaseForm.extend({
        initialize: function() {
            
            BaseForm.prototype.initialize.apply(this);

            this.addBranchList(new BranchList({
                el: this.$el.find('#project-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_B_PROJECT_TYPE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#use-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_B_USE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

        }
    });
});