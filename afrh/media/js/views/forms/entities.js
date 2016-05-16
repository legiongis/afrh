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

            if (resourcetypeid == "ACTIVITY_A.E7"){
                this.addBranchList(new BranchList({
                    el: this.$el.find('#project-contact-section')[0],
                    data: this.data,
                    dataKey: 'AFRH_PROJECT_CONTACT.E39',
                    validateBranch: function(nodes){
                        return this.validateHasValues(nodes);
                    }
                }));
            }
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#architect-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_ARCHITECT.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#contractor-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_CONTRACTOR.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#engineer-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_ENGINEER.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#archaeologist-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_ARCHAEOLOGIST.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#consultant-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_CONSULTANT.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#consulting-party-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_CONSULTING_PARTY.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#ncpc-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_NCPC_CONTACT.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#cfa-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_CFA_CONTACT.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#dcshpo-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_DCSHPO_CONTACT.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#notes-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_ENTITIES_NOTE.E62',
                singleEdit: true,
                
            }));

        }
    });
});