define(['jquery',
    'underscore',
    'knockout-mapping',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list'],
    function ($, _, koMapping, BaseForm, ValidationTools, BranchList) {
        
        var vt = new ValidationTools;
        return BaseForm.extend({
            
            initialize: function() {
                BaseForm.prototype.initialize.apply(this);
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#form-section')[0],
                    data: this.data,
                    dataKey: 'FORM_TYPE.E55',
                    validateBranch: function (nodes) {
                        return vt.nodesHaveValues(nodes,["FORM_TYPE.E55"]);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#measurement-section')[0],
                    data: this.data,
                    dataKey: 'MEASUREMENT_TYPE.E55',
                    validateBranch: function (nodes) {
                        return vt.nodesHaveValues(nodes,["VALUE_OF_MEASUREMENT.E60","UNIT_OF_MEASUREMENT.E55");
                    }
                }));
            }
        });
    }
);

