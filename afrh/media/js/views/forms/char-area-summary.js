define(['jquery', 
    'underscore', 
    'knockout-mapping', 
    'views/forms/base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], 
    function ($, _, koMapping, BaseForm, BranchList) {
        return BaseForm.extend({
            initialize: function() {
                BaseForm.prototype.initialize.apply(this);
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#name-section')[0],
                    data: this.data,
                    dataKey: 'NAME.E48',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#significance-section')[0],
                    data: this.data,
                    dataKey: 'RELATIVE_LEVEL_OF_SIGNIFICANCE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
                
            }
        });
    }
);