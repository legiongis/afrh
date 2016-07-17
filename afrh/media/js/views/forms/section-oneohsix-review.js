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
                el: this.$el.find('#exemption-section')[0],
                data: this.data,
                dataKey: 'SECTION_106_EXEMPTION.E55',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#urr-section')[0],
                data: this.data,
                dataKey: 'DCSHPO_URR.E42',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#submission-section')[0],
                data: this.data,
                dataKey: 'DCSHPO_SUBMISSION.E5',
                validateBranch: function(nodes){
                    ck1 = vt.nodesHaveValues(nodes,[
                        'DCSHPO_SUBMISSION_TYPE.E55',
                        'DCSHPO_SUBMISSION_METHOD.E55',
                        'DCSHPO_SUBMISSION_DATE.E49',
                        'AFRH_DETERMINATION_OF_EFFECT.E55'
                    ]);
                    var ck2 = vt.isValidDate(nodes,'DCSHPO_SUBMISSION_DATE.E49');
                    return ck1 && ck2;
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#response-section')[0],
                data: this.data,
                dataKey: 'DCSHPO_RESPONSE.E5',
                validateBranch: function(nodes){
                    ck1 = vt.nodesHaveValues(nodes,[
                        'DCSHPO_RESPONSE_TYPE.E55',
                        'DCSHPO_RESPONSE_EVALUATION.E55',
                        'DCSHPO_RESPONSE_FILE_NUMBER.E42',
                        'DCSHPO_RESPONSE_DATE.E49'
                    ]);
                    var ck2 = vt.isValidDate(nodes,'DCSHPO_RESPONSE_DATE.E49');
                    return ck1 && ck2;
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#notification-section')[0],
                data: this.data,
                dataKey: 'SECTION_106_NOTIFICATION.E5',
                validateBranch: function(nodes){
                    ck1 = vt.nodesHaveValues(nodes,[
                        'SECTION_106_NOTIFICATION_TYPE.E55',
                        'SECTION_106_NOTIFICATION_METHOD.E55',
                        'SECTION_106_NOTIFICATION_DATE.E49'
                    ]);
                    var ck2 = vt.isValidDate(nodes,'SECTION_106_NOTIFICATION_DATE.E49');
                    return ck1 && ck2;
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#dispute-section')[0],
                data: this.data,
                dataKey: 'SECTION_106_DISPUTE_RESOLUTION_NOTES.E62',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#agreement-section')[0],
                data: this.data,
                dataKey: 'SECTION_106_AGREEMENT.E5',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

        }
    });
});