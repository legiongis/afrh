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
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#measurement-section')[0],
                    data: this.data,
                    dataKey: 'MEASUREMENT_TYPE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
            }
        });
    }
);

