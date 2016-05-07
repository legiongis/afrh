define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/wizard-base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',
    'arches',
    'summernote',
    'blueimp-gallery',
    'blueimp-jquery',
    'plugins/bootstrap-image-gallery.min'], function ($, _, ko, WizardBase, ValidationTools, BranchList, datetimepicker, arches, summernote) {
    
    var vt = new ValidationTools;
    
    return WizardBase.extend({
        initialize: function() {
            WizardBase.prototype.initialize.apply(this);
            
            var resourcetypeid = $('#resourcetypeid').val();
            
            var self = this;
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});            
            var currentEditedConsultation = this.getBlankFormData();

            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            this.editAssessment = function(branchlist){
                self.switchBranchForEdit(branchlist);
            }

            this.deleteAssessment = function(branchlist){
                self.deleteClicked(branchlist);
            }

            ko.applyBindings(this, this.$el.find('#existing-consultations')[0]);

            this.addBranchList(new BranchList({
                data: currentEditedConsultation,
                dataKey: 'ACTIVITY_CONSULTATION.E5',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#method-section')[0],
                data: currentEditedConsultation,
                dataKey: 'CONSULTATION_METHOD.E55',
                singleEdit: true,
            }));

            if (resourcetypeid == "ACTIVITY_A.E7") {
                this.addBranchList(new BranchList({
                    el: this.$el.find('#type-section')[0],
                    data: currentEditedConsultation,
                    dataKey: 'CONSULTATION_TYPE.E55',
                    singleEdit: true,
                }));
            }
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#date-section')[0],
                data: currentEditedConsultation,
                dataKey: 'CONSULTATION_DATE.E49',
                singleEdit: true,
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#note-section')[0],
                data: currentEditedConsultation,
                dataKey: 'CONSULTATION_NOTE.E62',
                singleEdit: true
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#documentation-section')[0],
                data: currentEditedConsultation,
                dataKey: 'CONSULTATION_DOCUMENTATION_TYPE.E55',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#attendee-section')[0],
                data: currentEditedConsultation,
                dataKey: 'CONSULTATION_ATTENDEE.E39',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
        },

        startWorkflow: function() { 
            this.switchBranchForEdit(this.getBlankFormData());
        },

        switchBranchForEdit: function(conditionAssessmentData){
            this.prepareData(conditionAssessmentData);

            _.each(this.branchLists, function(branchlist){
                branchlist.data = conditionAssessmentData;
                branchlist.undoAllEdits();
            }, this);

            this.toggleEditor();
        },

        prepareData: function(assessmentNode){
            _.each(assessmentNode, function(value, key, list){
                assessmentNode[key].domains = this.data.domains;
            }, this);
            return assessmentNode;
        },

        getBlankFormData: function(){
            var data_to_prepare = {
                'ACTIVITY_CONSULTATION.E5': {
                    'branch_lists': []
                },
                'CONSULTATION_METHOD.E55': {
                    'branch_lists': []
                },
                'CONSULTATION_DOCUMENTATION_TYPE.E55': {
                    'branch_lists': []
                },
                'CONSULTATION_ATTENDEE.E39': {
                    'branch_lists': []
                },
                'CONSULTATION_DATE.E49': {
                    'branch_lists': []
                },
                'CONSULTATION_NOTE.E62': {
                    'branch_lists': []
                }
            }
            if (resourcetypeid.value == "ACTIVITY_A.E7"){
                data_to_prepare['CONSULTATION_TYPE.E55'] = {
                    'branch_lists': []
                }
            }
            return this.prepareData(data_to_prepare)
        },

        deleteClicked: function(branchlist) {
            var warningtext = '';
            this.deleted_assessment = branchlist;
            this.confirm_delete_modal = this.$el.find('.confirm-delete-modal');
            this.confirm_delete_modal_yes = this.confirm_delete_modal.find('.confirm-delete-yes');
            this.confirm_delete_modal_yes.removeAttr('disabled');

            warningtext = this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text();
            this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text(warningtext + ' ' + branchlist['CONSULTATION_METHOD.E55'].branch_lists[0].nodes[0].label);           
            this.confirm_delete_modal.modal('show');
        }

    });
});