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
                el: this.$el.find('#status-section')[0],
                data: this.data,
                dataKey: 'HISTORIC_AREA_STATUS.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#dates-section')[0],
                data: this.data,
                dataKey: 'PERIOD_OF_SIGNIFICANCE.E4',
                validateBranch: function(nodes){
                    var ck1 = vt.isValidDate(nodes,'PERIOD_OF_SIGNIFICANCE_BEGINNING_DATE.E49');
                    var ck2 = vt.isValidDate(nodes,'PERIOD_OF_SIGNIFICANCE_END_DATE.E49');
                    return ck1 && ck2;
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#criteria-section')[0],
                data: this.data,
                dataKey: 'NRHP_CRITERIA.E17',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#consideration-section')[0],
                data: this.data,
                dataKey: 'CRITERION_CONSIDERATIONS.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#significance-section')[0],
                data: this.data,
                dataKey: 'AREA_OF_SIGNIFICANCE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

        }
    });
});