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

            this.addBranchList(new BranchList({
                el: this.$el.find('#component-section')[0],
                data: this.data,
                dataKey: 'COMPONENT.E18',
                validateBranch: function (nodes) {
                    return vt.nodesHaveValues(nodes,['COMPONENT_TYPE.E55'])
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#modification-section')[0],
                data: this.data,
                dataKey: 'MODIFICATION_EVENT.E11',
                validateBranch: function (nodes) {
                    return vt.nodesHaveValues(nodes,['MODIFICATION_TYPE.E55']);
                }
            }));
        },
    });
});
