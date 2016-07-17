define(['jquery',
    'summernote',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], function ($, summernote, BaseForm, ValidationTools, BranchList) {
        
    var vt = new ValidationTools;
    
    return BaseForm.extend({
        initialize: function() {
            
            var resourcetypeid = $('#resourcetypeid').val();

            BaseForm.prototype.initialize.apply(this);
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });
            
            if (resourcetypeid == 'ACTOR.E39') {
                this.addBranchList(new BranchList({
                    el: this.$el.find('#role-section')[0],
                    data: this.data,
                    dataKey: 'PHASE_TYPE_ASSIGNMENT.E17',
                    validateBranch: function (nodes) {
                        var ck1 = vt.isValidDate(nodes,'FROM_DATE.E49');
                        var ck2 = vt.isValidDate(nodes,'TO_DATE.E49');
                        var ck3 = vt.nodesHaveValues(nodes, ['ACTOR_TYPE.E55']);
                        return ck1 && ck2 && ck3;
                    }
            }));
            }

            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION.E62',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

            if (resourcetypeid == 'INVENTORY_RESOURCE.E18') {
                this.addBranchList(new BranchList({
                    el: this.$el.find('#style-section')[0],
                    data: this.data,
                    dataKey: 'STYLE.E55',
                    validateBranch: function(nodes){
                        return this.validateHasValues(nodes);
                    }
                }));
            }

        }
    });
});