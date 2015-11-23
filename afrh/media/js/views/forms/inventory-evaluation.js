define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',
    'summernote'],
    function ($, _, ko, BaseForm, ValidationTools, BranchList, datetimepicker, summernote) {
        
        var vt = new ValidationTools;

        return BaseForm.extend({

            initialize: function() {
                
                $('.totalscore').change(function() {
                    var sum = 0;
                    $('.totalscore').each(function(){
                        sum += parseFloat(this.value);
                    });
                    var comp = document.getElementById("comp");
                    comp.value = sum;
                    $(comp).trigger('change');
                    //comp.innerHTML = sum;
                });

                BaseForm.prototype.initialize.apply(this);
                
                var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $(this).find('input').trigger('change'); 
                });
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#afrh-hd-status-section')[0],
                    data: this.data,
                    dataKey: 'AFRH_W_HISTORIC_DISTRICT_STATE.E3',
                    validateBranch: function (nodes) {
                        var ck1 = vt.isValidDate(nodes,'AFRH_W_HISTORIC_DISTRICT_STATUS_DATE.E50');
                        var ck2 = this.validateHasValues(nodes);
                        return ck1 == true && ck2 == true;
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#period-of-significance-section')[0],
                    data: this.data,
                    dataKey: 'PERIOD_OF_SIGNIFICANCE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#area-of-significance-section')[0],
                    data: this.data,
                    dataKey: 'AREA_OF_SIGNIFICANCE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#afrh-other-section')[0],
                    data: this.data,
                    dataKey: 'OTHER_AFRH_W_DESIGNATION.E3',
                    validateBranch: function (nodes) {
                        return true;
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#other-designation-section')[0],
                    data: this.data,
                    dataKey: 'OTHER_DESIGNATION.E3',
                    validateBranch: function (nodes) {
                        return true;
                        return this.validateHasValues(nodes);
                    }
                }));
                
                console.log("before score section branchlist");
                this.addBranchList(new BranchList({
                    el: this.$el.find('#score-section')[0],
                    data: this.data,
                    dataKey: 'COMPOSITE_SCORE.E60',
                    //singleEdit: true,
                    // validateBranch: function (nodes) {
                        // var valid = false;
                        // if (nodes[0]["value"] != "") {
                            // console.log(nodes[0]["value"]);
                            // valid = true;
                        // };
                        // console.log(valid);
                        // return valid;
                    // }
                }));
                console.log("added score section branchlist");
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#hpmp-section')[0],
                    data: this.data,
                    dataKey: 'HPMP_STATUS.E55',
                    validateBranch: function (nodes) {
                        return true;
                        return this.validateHasValues(nodes);
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#relative-level-section')[0],
                    data: this.data,
                    dataKey: 'RELATIVE_LEVEL_OF_SIGNIFICANCE.E55',
                    validateBranch: function (nodes) {
                        var goodDate = true;
                        _.each(nodes, function(node){
                            if (node["entitytypeid"] == "RELATIVE_LEVEL_OF_SIGNIFICANCE_DATE.E50") {
                                date_check = isValidDate(node["value"]);
                                if (!date_check[0]){
                                    goodDate = false;
                                }
                                node["value"] = date_check[1];
                                node["label"] = date_check[1];
                            }
                        });
                        return goodDate;
                    }
                }));
                
            }
        });
    }
);
