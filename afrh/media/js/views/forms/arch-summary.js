define(['jquery',
    'summernote',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], function ($, summernote, BaseForm, ValidationTools, BranchList) {
        
    var vt = new ValidationTools;
    
    return BaseForm.extend({
        initialize: function() {
            
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });
            
            BaseForm.prototype.initialize.apply(this);

            this.addBranchList(new BranchList({
                el: this.$el.find('#name-section')[0],
                data: this.data,
                dataKey: 'ARCHAEOLOGICAL_ZONE_NAME.E48',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION.E62',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
        }
    });
});