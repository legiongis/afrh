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
                el: this.$el.find('#scope-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_SCOPE_OF_WORK.E89',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#building-section')[0],
                data: this.data,
                dataKey: 'BUILDING_STRUCTURES_RECOMMENDATION_TYPE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#object-section')[0],
                data: this.data,
                dataKey: 'OBJECT_RECOMMENDATION_TYPE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#landscape-section')[0],
                data: this.data,
                dataKey: 'LANDSCAPE_RECOMMENDATION_TYPE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#condition-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_CONDITION.E3',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

        }
    });
});