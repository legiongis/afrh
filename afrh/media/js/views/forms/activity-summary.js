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
            
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });
            
            if (resourcetypeid == 'ACTIVITY_B.E7') {
                this.addBranchList(new BranchList({
                    el: this.$el.find('#permit-section')[0],
                    data: this.data,
                    dataKey: 'BUILDING_PERMIT_NUMBER.E42',
                    validateBranch: function(nodes){
                        return this.validateHasValues(nodes);
                    }
                }));
            }

            this.addBranchList(new BranchList({
                el: this.$el.find('#name-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_NAME.E41',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            if (resourcetypeid == 'ACTIVITY_A.E7') {
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#work-order-section')[0],
                    data: this.data,
                    dataKey: 'WORK_ORDER_ASSIGNMENT.E13',
                    validateBranch: function(nodes){
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#request-date-section')[0],
                    data: this.data,
                    dataKey: 'ACTION_AGENT_REQUEST_DATE.E49',
                    singleEdit: true,
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#procedure-section')[0],
                    data: this.data,
                    dataKey: 'ACTIVITY_PROCEDURE_TYPE.E55',
                    validateBranch: function(nodes){
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#procedure-note-section')[0],
                    data: this.data,
                    dataKey: 'ACTIVITY_PROCEDURE_NOTE.E62',
                    singleEdit: true,
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#status-section')[0],
                    data: this.data,
                    dataKey: 'ACTION_STATUS_ASSIGNMENT.E13',
                    singleEdit: true
                }));
            }
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#agent-section')[0],
                data: this.data,
                dataKey: 'ACTION_AGENT.E39',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#review-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_REVIEW_TYPE.E55',
                validateBranch: function(nodes){
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#review-note-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_REVIEW_NOTE.E62',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#milestone-section')[0],
                data: this.data,
                dataKey: 'ACTIVITY_MILESTONE_ACHIEVEMENT.E5',
                validateBranch: function(nodes){
                    if (resourcetypeid == 'ACTIVITY_A.E7') {
                        var typenode = 'ACTIVITY_A_MILESTONE.E55';
                    }
                    if (resourcetypeid == 'ACTIVITY_B.E7') {
                        var typenode = 'ACTIVITY_B_MILESTONE.E55';
                    }
                    var ck1 = vt.nodesHaveValues(nodes,[typenode,'ACTIVITY_MILESTONE_DATE.E49'])
                    var ck2 = vt.isValidDate(nodes,'ACTIVITY_MILESTONE_DATE.E49')
                    return ck1 == true && ck2 == true;
                }
            }));

        }
    });
});