define(['jquery', 
    'underscore', 
    'summernote', 
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker'], function ($, _, summernote, BaseForm, ValidationTools, BranchList) {

    var vt = new ValidationTools;
    
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);
            
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $(this).find('input').trigger('change'); 
                });

            this.addBranchList(new BranchList({
                el: this.$el.find('#component-section')[0],
                data: this.data,
                dataKey: 'COMPONENT.E18',
                validateBranch: function (nodes) {
                    var ck1 = vt.isValidDate(nodes, 'COMPONENT_TIME-SPAN_DATE.E50');
                    var ck2 = vt.nodesHaveValues(nodes,['COMPONENT_TYPE.E55']);
                    return ck1 && ck2;
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#modification-section')[0],
                data: this.data,
                dataKey: 'MODIFICATION_EVENT.E11',
                validateBranch: function (nodes) {
                    var ck1 = vt.isValidDate(nodes, 'MODIFICATION_EVENT_TIME-SPAN_DATE.E50');
                    var ck2 = vt.nodesHaveValues(nodes,['MODIFICATION_TYPE.E55']);
                    return ck1 && ck2;
                }
            }));
        },
    });
});
