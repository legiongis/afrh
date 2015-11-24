define(['jquery',
    'summernote',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list', ], function ($, summernote, BaseForm, ValidationTools, BranchList) {
        
    var vt = new ValidationTools;
    
    return BaseForm.extend({
        initialize: function() {
            
            var resourcetypeid = $('#resourcetypeid').val();

            BaseForm.prototype.initialize.apply(this);
            
            if (resourcetypeid == 'ACTOR.E39') {
                // this.addBranchList(new BranchList({
                    // el: this.$el.find('#roles-section')[0],
                    // data: this.data,
                    // dataKey: 'STYLE.E55',
                    // validateBranch: function(nodes){
                        // return this.validateHasValues(nodes);
                    // }
                // }));
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