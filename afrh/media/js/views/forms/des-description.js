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
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION.E62',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#number-section')[0],
                data: this.data,
                dataKey: 'NUMBER_OF_RESOURCES.E62',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

        }
    });
});