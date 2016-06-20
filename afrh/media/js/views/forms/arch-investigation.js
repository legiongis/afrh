define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/wizard-base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'views/forms/sections/location-branch-list',
    'bootstrap-datetimepicker',
    'arches',
    'dropzone',
    'summernote',
    'blueimp-gallery',
    'blueimp-jquery',
    'plugins/bootstrap-image-gallery.min'], function ($, _, ko, WizardBase, ValidationTools, BranchList, LocationBranchList, datetimepicker, arches, dropzone, summernote) {
    
    var vt = new ValidationTools;
    
    return WizardBase.extend({
        initialize: function() {
            WizardBase.prototype.initialize.apply(this);

            var self = this;
            var dropzoneEl = this.$el.find('.dropzone');
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});            
            var currentEditedInvestigation = this.getBlankFormData();

            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });
            
            

            // detect if dropzone is attached, and if not init
            if (!dropzoneEl.hasClass('dz-clickable')) {
                this.dropzoneInstance = new dropzone(dropzoneEl[0], {
                    url: arches.urls.concept,
                    acceptedFiles: 'image/*',
                    addRemoveLinks: true,
                    autoProcessQueue: false
                });

                this.dropzoneInstance.on("addedfile", function(file) {
                    if (file.mock){

                    }else{
                        var el = self.el.appendChild(this.hiddenFileInput);
                        el.setAttribute('name', _.uniqueId('file_'));
                        self.filebranchlist.files.push({
                            file: file,
                            el: el
                        })
                        this.hiddenFileInput = false;
                    }
                });

                this.dropzoneInstance.on("removedfile", function(filetoremove) {
                    if (filetoremove.mock){
                        self.filebranchlist.deleteItem(filetoremove.branchlist);
                    }else{
                        var index;
                        _.each(self.filebranchlist.files, function(file, i){
                            if (file.file === filetoremove){
                                index = i;
                            }
                        }, this);

                        self.el.removeChild(self.filebranchlist.files[index].el);
                        self.filebranchlist.files.splice(index, 1);
                    }
                });
            }

            this.editAssessment = function(branchlist){
                self.switchBranchForEdit(branchlist);
            }

            this.deleteAssessment = function(branchlist){
                self.deleteClicked(branchlist);
            }

            ko.applyBindings(this, this.$el.find('#existing-investigations')[0]);

            this.addBranchList(new BranchList({
                data: currentEditedInvestigation,
                dataKey: 'INVESTIGATION.E7',
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#assessment-type-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'INVESTIGATION_ASSESSMENT.E55',
                singleEdit: true,
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#method-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'INVESTIGATION_METHOD.E55',
                singleEdit: true,
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#date-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'INVESTIGATION_DATE.E49',
                singleEdit: true,
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#report-number-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'DCSHPO_REPORT_NUMBER.E42',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'INVESTIGATION_DESCRIPTION.E62',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#tp-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'TEST_PIT.E7',
                validateBranch: function (nodes) {
                    return vt.nodesHaveValues(nodes,['TEST_PIT_ID.E42','TEST_PIT_METHOD.E55']);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#prehist-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'PREHISTORIC_SITE_POTENTIAL_ASSESSMENT.E14',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#native-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'NATIVE_AMERICAN_SITE_POTENTIAL_ASSESSMENT.E14',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#historic-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'HISTORIC_SITE_POTENTIAL_ASSESSMENT.E14',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#recs-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'INVESTIGATION_RECOMMENDATIONS.E62',
                singleEdit: true,
            }));

            this.filebranchlist = this.addBranchList(new BranchList({
                el: this.$el.find('#files-section')[0],
                data: currentEditedInvestigation,
                dataKey: 'INVESTIGATION_IMAGE.E73',
                files: [],
                validateBranch: function (nodes) {
                    return true;
                },
                addMockFiles: function(){
                    self.dropzoneInstance.removeAllFiles();
                    $('.dz-preview.dz-image-preview').remove();
                    _.each(this.getBranchLists(), function(list){
                        // Create the mock file:
                        var mockFile = { name: '', size: 0, mock: true, branchlist: list};
                        var thumbnail = '';

                        // And optionally show the thumbnail of the file:
                        _.each(ko.toJS(list.nodes), function(node){
                            if (node.entitytypeid === 'INVESTIGATION_IMAGE_FILE_PATH.E62'){
                                mockFile.name = node.value
                            }
                            if (node.entitytypeid === 'INVESTIGATION_IMAGE_THUMBNAIL.E62'){
                                thumbnail = node.value;
                            }
                        }, this);

                        // Call the default addedfile event handler
                        self.dropzoneInstance.emit("addedfile", mockFile);
                        self.dropzoneInstance.emit("thumbnail", mockFile, thumbnail);

                        // Make sure that there is no progress bar, etc...
                        // self.dropzoneInstance.emit("complete", mockFile);

                        // If you use the maxFiles option, make sure you adjust it to the
                        // correct amount:
                        // var existingFileCount = 1; // The number of files already uploaded
                        // self.dropzoneInstance.options.maxFiles = self.dropzoneInstance.options.maxFiles - existingFileCount;
                    }, this);
                }
            }));
        },

        startWorkflow: function() { 
            this.switchBranchForEdit(this.getBlankFormData());
        },

        switchBranchForEdit: function(conditionAssessmentData){
            
            var self = this;
            this.prepareData(conditionAssessmentData);

            _.each(this.branchLists, function(branchlist){
                branchlist.data = conditionAssessmentData;
                branchlist.undoAllEdits();
            }, this);

            this.filebranchlist.addMockFiles();
            
            this.toggleEditor();
            
            // $("#map-tab").on('click', function() {
                // console.log("map tab!");
                // self.addBranchList(new LocationBranchList({
                    // el: self.$el.find('#geom-list-section')[0],
                    // data: conditionAssessmentData,
                    // dataKey: 'TEST_PIT_LOCATIONS_GEOMETRY.E47',
                    // initialize: function () {
                        // console.log("initialize function");
                    // }
                // }));
            // });

        },

        prepareData: function(assessmentNode){
            _.each(assessmentNode, function(value, key, list){
                assessmentNode[key].domains = this.data.domains;
            }, this);
            return assessmentNode;
        },

        getBlankFormData: function(){
            return this.prepareData({
                'INVESTIGATION.E7': {
                    'branch_lists': []
                },
                'INVESTIGATION_ASSESSMENT.E55': {
                    'branch_lists': []
                },
                'INVESTIGATION_METHOD.E55': {
                    'branch_lists': []
                },
                'INVESTIGATION_DATE.E49': {
                    'branch_lists': []
                },
                'DCSHPO_REPORT_NUMBER.E42': {
                    'branch_lists': []
                },
                'INVESTIGATION_DESCRIPTION.E62': {
                    'branch_lists': []
                },
                'TEST_PIT.E7': {
                    'branch_lists': []
                },
                'INVESTIGATION_IMAGE.E73': {
                    'branch_lists': []
                },
                'PREHISTORIC_SITE_POTENTIAL_ASSESSMENT.E14': {
                    'branch_lists': []
                },
                'NATIVE_AMERICAN_SITE_POTENTIAL_ASSESSMENT.E14': {
                    'branch_lists': []
                },
                'HISTORIC_SITE_POTENTIAL_ASSESSMENT.E14': {
                    'branch_lists': []
                },
                'INVESTIGATION_RECOMMENDATIONS.E62': {
                    'branch_lists': []
                },
                // 'GUIDELINE_IMAGE_NOTE.E62': {
                    // 'branch_lists': []
                // }
            })
        },

        deleteClicked: function(branchlist) {
            var warningtext = '';
            this.deleted_assessment = branchlist;
            this.confirm_delete_modal = this.$el.find('.confirm-delete-modal');
            this.confirm_delete_modal_yes = this.confirm_delete_modal.find('.confirm-delete-yes');
            this.confirm_delete_modal_yes.removeAttr('disabled');

            warningtext = this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text();
            this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text(warningtext + ' ' + branchlist['INVESTIGATION_ASSESSMENT.E55'].branch_lists[0].nodes[0].label);           
            this.confirm_delete_modal.modal('show');
        }

    });
});