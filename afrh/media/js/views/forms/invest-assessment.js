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
            
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            this.addBranchList(new BranchList({
                el: this.$el.find('#prehistoric-section')[0],
                data: this.data,
                dataKey: 'PREHISTORIC_SITE_POTENTIAL_ASSESSMENT.E14',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#native-american-section')[0],
                data: this.data,
                dataKey: 'NATIVE_AMERICAN_SITE_POTENTIAL_ASSESSMENT.E14',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#historic-section')[0],
                data: this.data,
                dataKey: 'HISTORIC_SITE_POTENTIAL_ASSESSMENT.E14',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
        }
    });
});