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
                el: this.$el.find('#identification-section')[0],
                data: this.data,
                dataKey: 'CFA_REVIEW_IDENTIFICATION.E15',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#submission-section')[0],
                data: this.data,
                dataKey: 'CFA_SUBMISSION.E5',
                validateBranch: function(nodes){
                    var ck1 = vt.nodesHaveValues(nodes,["CFA_SUBMISSION_TYPE","CFA_SUBMISSION_DATE.E49"]);
                    var ck2 = vt.isValidDate(nodes,"CFA_SUBMISSION_DATE.E49");
                    return ck1 && ck2;
                }
            }));

        }
    });
});