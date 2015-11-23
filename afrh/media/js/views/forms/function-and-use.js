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
    
        //modified version of code from http://stackoverflow.com/questions/6177975/how-to-validate-date-with-format-mm-dd-yyyy-in-javascript
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

        return BaseForm.extend({

            initialize: function() {
                
                BaseForm.prototype.initialize.apply(this);
                var self = this;
                
                //date picker code
                var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $(this).find('input').trigger('change'); 
                });

                this.addBranchList(new BranchList({
                    el: this.$el.find('#function-section')[0],
                    data: this.data,
                    dataKey: 'PHASE_TYPE_ASSIGNMENT.E17',
                    validateBranch: function (nodes) {
                        var chk1 = vt.isValidDate(nodes, 'FROM_DATE.E49');
                        var chk2 = vt.isValidDate(nodes, 'TO_DATE.E49');
                        var chk3 = vt.nodesHaveValues(nodes, ['FUNCTION.E62','FUNCTION_PERIOD.E55']);
                        return chk1 == true && chk2 == true && chk3 == true;
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#current-use-section')[0],
                    data: this.data,
                    dataKey: 'HERITAGE_ASSET_REPORT.E3',
                    validateBranch: function (nodes) {
                        var chk1 = vt.isValidDate(nodes, 'HERITAGE_ASSET_REPORT_DATE.E49');
                        var chk2 = vt.nodesHaveValues(nodes, ['CURRENT_USER.E55','CURRENT_OPERATION_STATUS.E55','HERITAGE_ASSET_REPORT_DATE.E49']);
                        return chk1 == true && chk2 == true;
                    }
                }));
            }
        });
    }
);
        
