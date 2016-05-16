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
                dataKey: 'NAME.E48',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#zone-type-section')[0],
                data: this.data,
                dataKey: 'ZONE_TYPE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#planned-use-section')[0],
                data: this.data,
                dataKey: 'PLANNED_USE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#date-section')[0],
                data: this.data,
                dataKey: 'MASTER_PLAN_ZONE_ACTIVITY.E7',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

        }
    });
});