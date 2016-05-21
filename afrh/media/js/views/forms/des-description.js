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

            var $select = $(".0-200");
            for (i=0;i<=200;i++){
                $select.append($('<option></option>').val(i).html(i))
            }

            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION.E62',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#non-contributing-section')[0],
                data: this.data,
                dataKey: 'NUMBER_OF_NON_CONTRIBUTING_RESOURCES.E62',
                singleEdit: true,
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#contributing-section')[0],
                data: this.data,
                dataKey: 'NUMBER_OF_CONTRIBUTING_RESOURCES.E62',
                singleEdit: true,
            }));

        }
    });
});