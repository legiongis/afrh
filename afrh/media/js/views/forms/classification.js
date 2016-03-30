define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/wizard-base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',
    'summernote'], function ($, _, ko, WizardBase, BranchList, datetimepicker, summernote) {
    
    //modified version of code from http://stackoverflow.com/questions/6177975/how-to-validate-date-with-format-mm-dd-yyyy-in-javascript
    function isValidDate(dateString){
        
        // Change to acceptable db format
        var replaceDate = dateString.replace(/\//g,"-");
        
        // Create output array
        var output = new Array(
            false,
            replaceDate
        );       
        
        // Deal with empty dates (they're ok!)
        if(output[1] == ""){
            output[0] = true;
            return output;
        }
        
        // First check for the pattern
        if(!/^\d{4}\-\d{1,2}\-\d{1,2}$/.test(dateString)){
            return output;
        }

        // Parse the date parts to integers       
        var parts = replaceDate.split("-");
        var day = parseInt(parts[2], 10);
        var month = parseInt(parts[1], 10);
        var year = parseInt(parts[0], 10);

        // Check the ranges of month and year
        if(year > 3000 || month == 0 || month > 12){
            return output;
        }
        var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

        // Adjust for leap years
        if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0)){
            monthLength[1] = 29;
        }
            
        // Check the range of the day
        output[0] = day > 0 && day <= monthLength[month - 1];
        output[1] = replaceDate;
        return output;
    };

    return WizardBase.extend({

        initialize: function() {
            WizardBase.prototype.initialize.apply(this);

            var self = this;
            var date_picker = $('.datetimepicker').datetimepicker({
                pickTime: false, 
                dateFormat: 'yy-mm-dd'
            });            
            var currentEditedClassification = this.getBlankFormData();

            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            this.editClassification = function(branchlist){
                self.switchBranchForEdit(branchlist);
            }

            this.deleteClassification = function(branchlist){
                self.deleteClicked(branchlist);
            }
            
            ko.applyBindings(this, this.$el.find('#existing-classifications')[0]);

            this.addBranchList(new BranchList({
                data: currentEditedClassification,
                dataKey: 'PHASE_TYPE_ASSIGNMENT.E17'
            }));
            this.addBranchList(new BranchList({
                el: this.$el.find('#resource-type-section')[0],
                data: currentEditedClassification,
                dataKey: 'HERITAGE_RESOURCE_TYPE.E55',
                singleEdit: true
            }));
            this.addBranchList(new BranchList({
                el: this.$el.find('#resource-use-section')[0],
                data: currentEditedClassification,
                dataKey: 'HERITAGE_RESOURCE_USE_TYPE.E55',
                singleEdit: true
            }));
            this.addBranchList(new BranchList({
                el: this.$el.find('#related-features-section')[0],
                data: currentEditedClassification,
                dataKey: 'ANCILLARY_FEATURE_TYPE.E55',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            this.addBranchList(new BranchList({
                el: this.$el.find('#to-date-section')[0],
                data: currentEditedClassification,
                dataKey: 'TO_DATE.E49',
                singleEdit: true,
                validateBranch: function (nodes) {
                    var check_to = isValidDate(nodes[0]['value']);
                    nodes[0]['value'] = check_to[1];
                    return check_to[0];
                }
            }));   
            this.addBranchList(new BranchList({
                el: this.$el.find('#from-date-section')[0],
                data: currentEditedClassification,
                dataKey: 'FROM_DATE.E49',
                singleEdit: true,
                validateBranch: function (nodes) {
                    var check_from = isValidDate(nodes[0]['value']);
                    nodes[0]['value'] = check_from[1];
                    return check_from[0];
                }
            })); 
        },     

        startWorkflow: function() { 
            this.switchBranchForEdit(this.getBlankFormData());
        },

        switchBranchForEdit: function(classificationData){
            this.prepareData(classificationData);

            _.each(this.branchLists, function(branchlist){
                branchlist.data = classificationData;
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
            return this.prepareData({
                'HERITAGE_RESOURCE_TYPE.E55': {
                    'branch_lists':[]
                },
                'HERITAGE_RESOURCE_USE_TYPE.E55': {
                    'branch_lists':[]
                },
                'ANCILLARY_FEATURE_TYPE.E55': {
                    'branch_lists':[]
                },
                'FROM_DATE.E49': {
                    'branch_lists': []
                },
                'TO_DATE.E49': {
                    'branch_lists': []
                },
                'PHASE_TYPE_ASSIGNMENT.E17': {
                    'branch_lists':[]
                }
            })
        },

        deleteClicked: function(branchlist) {
            var warningtext = '';

            this.deleted_assessment = branchlist;
            this.confirm_delete_modal = this.$el.find('.confirm-delete-modal');
            this.confirm_delete_modal_yes = this.confirm_delete_modal.find('.confirm-delete-yes');
            this.confirm_delete_modal_yes.removeAttr('disabled');

            warningtext = this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text();
            this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text(warningtext + ' ' + branchlist['HERITAGE_RESOURCE_TYPE.E55'].branch_lists[0].nodes[0].label);           
            this.confirm_delete_modal.modal('show');
        },
        
        

    });
});