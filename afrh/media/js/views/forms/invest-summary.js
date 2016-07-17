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
                el: this.$el.find('#assessment-section')[0],
                data: this.data,
                dataKey: 'INVESTIGATION_ASSESSMENT.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#method-section')[0],
                data: this.data,
                dataKey: 'INVESTIGATION_METHOD.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#date-section')[0],
                data: this.data,
                dataKey: 'INVESTIGATION_DATE.E49',
                validateBranch: function(nodes){
                    var ck1 = vt.isValidDate(nodes,'INVESTIGATION_DATE.E49');
                    var ck2 = vt.nodesHaveValues(nodes,['INVESTIGATION_DATE.E49']);
                    return ck1 && ck2;
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#report-section')[0],
                data: this.data,
                dataKey: 'DCSHPO_REPORT_NUMBER.E42',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#zone-section')[0],
                data: this.data,
                dataKey: 'ARCHAEOLOGICAL_ZONE.E55',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'INVESTIGATION_DESCRIPTION.E62',
                singleEdit: true,
            }));
            
        }
    });
});