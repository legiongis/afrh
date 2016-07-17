define(['jquery',
    'summernote',
    'dropzone',
    'arches',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], function ($, summernote, dropzone, arches, BaseForm, ValidationTools, BranchList) {
        
    var vt = new ValidationTools;
    
    return BaseForm.extend({
        initialize: function() {
            
            BaseForm.prototype.initialize.apply(this);

            var self = this;
            var dropzoneEl = this.$el.find('.dropzone');

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
                    console.log(this.filebranchlist);
                    
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

            this.filebranchlist = this.addBranchList(new BranchList({
                el: this.$el.find('#image-section')[0],
                data: this.data,
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
                        //self.dropzoneInstance.emit("complete", mockFile);

                        // If you use the maxFiles option, make sure you adjust it to the
                        // correct amount:
                        // var existingFileCount = 1; // The number of files already uploaded
                        // myDropzone.options.maxFiles = myDropzone.options.maxFiles - existingFileCount;
                    }, this);
                }
            }));
            
            this.filebranchlist.addMockFiles();
        },

        // startWorkflow: function() { 
            // this.switchBranchForEdit(this.getBlankFormData());
        // },

        // switchBranchForEdit: function(conditionAssessmentData){
            // this.prepareData(conditionAssessmentData);

            // _.each(this.branchLists, function(branchlist){
                // branchlist.data = conditionAssessmentData;
                // branchlist.undoAllEdits();
            // }, this);

            // this.filebranchlist.addMockFiles();
            // this.toggleEditor();
        // },

        // prepareData: function(assessmentNode){
            // _.each(assessmentNode, function(value, key, list){
                // assessmentNode[key].domains = this.data.domains;
            // }, this);
            // return assessmentNode;
        // },

        // getBlankFormData: function(){
            // return this.prepareData({
                // 'CONDITION_ASSESSMENT.E14': {
                    // 'branch_lists': []
                // },
                // 'DISTURBANCE_TYPE.E55': {
                    // 'branch_lists': []
                // },
                // 'CONDITION_TYPE.E55': {
                    // 'branch_lists': []
                // },
                // 'CONDITION_ASSESSMENT_TYPE.E55': {
                    // 'branch_lists': []
                // },
                // 'THREAT_TYPE.E55': {
                    // 'branch_lists': []
                // },
                // 'RECOMMENDATION_TYPE.E55': {
                    // 'branch_lists': []
                // },
                // 'DATE_CONDITION_ASSESSED.E49': {
                    // 'branch_lists': []
                // },
                // 'CONDITION_DESCRIPTION.E62': {
                    // 'branch_lists': []
                // },
                // 'CONDITION_IMAGE.E73': {
                    // 'branch_lists': []
                // }
            // })
        // },

        // deleteClicked: function(branchlist) {
            // var warningtext = '';

            // this.deleted_assessment = branchlist;
            // this.confirm_delete_modal = this.$el.find('.confirm-delete-modal');
            // this.confirm_delete_modal_yes = this.confirm_delete_modal.find('.confirm-delete-yes');
            // this.confirm_delete_modal_yes.removeAttr('disabled');

            // warningtext = this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text();
            // this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text(warningtext + ' ' + branchlist['DATE_CONDITION_ASSESSED.E49'].branch_lists[0].nodes[0].label + ': ' + branchlist['CONDITION_TYPE.E55'].branch_lists[0].nodes[0].label);           
            // this.confirm_delete_modal.modal('show');
        // }

    });
    
});