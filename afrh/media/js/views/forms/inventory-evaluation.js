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
        
        function isValidDate(dateString){
            
            console.log("validating: "+dateString);
            justDate = dateString.split("T")[0]
            
            // Change to acceptable db format
            var replaceDate = justDate.replace(/\//g,"-");
            
            // Create output array
            var output = new Array(
                false,
                replaceDate
            );       
            
            // Deal with empty dates (they're ok!)
            if(output[1] == ""){
                output[0] = true;
                console.log("blank date ok");
                return output;
            }
            
            // First check for the pattern
            if(!/^\d{4}\-\d{1,2}\-\d{1,2}$/.test(replaceDate)){
                console.log("pattern fail");
                return output;
            }

            // Parse the date parts, rebuild replaceDate
            var parts = replaceDate.split("-");
            for (i=1; i==2; i++) {
                console.log(i);
                if (parts[i].length == i) {
                    parts[i] = "0"+parts[i];
                }
            }
            replaceDate = parts.join("-");
            
            // make parts into integers for processing
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
            console.log(output);
            return output;
        };
        
        //insert validation functions here

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
