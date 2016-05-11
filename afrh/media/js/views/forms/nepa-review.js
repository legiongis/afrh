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
                el: this.$el.find('#type-section')[0],
                data: this.data,
                dataKey: 'NEPA_DOCUMENTATION_TYPE.E55',
                validateBranch: function(nodes){
                    return vt.nodesHaveValues(nodes,'NEPA_DOCUMENTATION_TYPE.E55');
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#catex-section')[0],
                data: this.data,
                dataKey: 'CATEX_TYPE.E55',
                validateBranch: function(nodes){
                    return vt.nodesHaveValues(nodes,'CATEX_TYPE.E55');
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#ea-section')[0],
                data: this.data,
                dataKey: 'EA_TYPE.E55',
                validateBranch: function(nodes){
                    return vt.nodesHaveValues(nodes,'EA_TYPE.E55');
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#eis-section')[0],
                data: this.data,
                dataKey: 'EIS_TYPE.E55',
                validateBranch: function(nodes){
                    return vt.nodesHaveValues(nodes,'EIS_TYPE.E55');
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#documentation-section')[0],
                data: this.data,
                dataKey: 'NEPA_DOCUMENTATION.E31',
                validateBranch: function(nodes){
                    var ck1 = vt.isValidDate(nodes, 'NEPA_DOCUMENTATION_DATE.E49');
                    var ck2 = vt.nodesHaveValues(nodes,'NEPA_DOCUMENTATION.E31');
                    return ck1 && ck2;
                }
            }));

        }
    });
});