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
                el: this.$el.find('#name-section')[0],
                data: this.data,
                dataKey: 'HISTORIC_AREA_NAME.E48',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#designation-section')[0],
                data: this.data,
                dataKey: 'HISTORIC_AREA_DESIGNATION.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#designation-type-section')[0],
                data: this.data,
                dataKey: 'HISTORIC_AREA_TYPE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#date-section')[0],
                data: this.data,
                dataKey: 'ADMINISTRATIVE_DATE.E49',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

        }
    });
});