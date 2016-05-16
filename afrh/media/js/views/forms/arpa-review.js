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
            
            var disturbanceBranch = new BranchList({
                el: this.$el.find('#disturbance-section')[0],
                data: this.data,
                dataKey: 'GROUND_DISTURBANCE.E62',
                singleEdit: true,
            });
            
            this.addBranchList(disturbanceBranch);

            var disBranchlists = disturbanceBranch['data']['GROUND_DISTURBANCE.E62']['branch_lists'];
            if (disBranchlists.length == 0) {
                var display = false
            } else {
                var choice = disBranchlists[0]['nodes'][0].value;
                if (choice == 'Yes') {display = true;} else {display = false;}
            }
            
            if (display){
                $('#everything-else').show();
            }
            
            $('#ground-disturbance-bool').change(function() {
                $('#everything-else').toggle();
            });
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#disturbance-location-section')[0],
                data: this.data,
                dataKey: 'GROUND_DISTURBANCE_LOCATION.E27',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#determination-section')[0],
                data: this.data,
                dataKey: 'AFRH_ARPA_ASSESSMENT.E5',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#notification-section')[0],
                data: this.data,
                dataKey: 'DCSHPO_NOTIFICATION.E5',
                singleEdit: true,
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#documentation-section')[0],
                data: this.data,
                dataKey: 'ARPA_DOCUMENTATION.E31',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#investigation-section')[0],
                data: this.data,
                dataKey: 'ARPA_FIELD_INVESTIGATION.E5',
                validateBranch: function (nodes) {
                    
                    var ck0 = vt.nodesHaveValues(nodes, [
                        'ARPA_FIELD_INVESTIGATION_TYPE.E55',
                        'ARPA_FIELD_INVESTIGATION_START_DATE.E49',
                        'ARPA_FIELD_INVESTIGATION_END_DATE.E49'
                    ]);
                    var ck1 = vt.isValidDate(nodes,'ARPA_FIELD_INVESTIGATION_START_DATE.E49');
                    var ck2 = vt.isValidDate(nodes,'ARPA_FIELD_INVESTIGATION_END_DATE.E49');
                    return ck0 && ck1 && ck2;
                }
            }));
            
            this.addBranchList(new BranchList({
                el: this.$el.find('#discovery-section')[0],
                data: this.data,
                dataKey: 'ARPA_DISCOVERY.E5',
                validateBranch: function (nodes) {
                    var ck0 = vt.nodesHaveValues(nodes, ['ARPA_DISCOVERY_DATE.E49']);
                    var ck1 = vt.isValidDate(nodes,'ARPA_DISCOVERY_DATE.E49');
                    var ck2 = vt.isValidDate(nodes,'ARPA_DISCOVERY_DOCUMENTATION_DATE.E49');
                    var ck3 = vt.isValidDate(nodes,'ARPA_DISCOVERY_DCSHPO_NOTIFICATION_DATE.E49');
                    return ck0 && ck1 && ck2 && ck3;
                }
            }));
            
        }
    });
});