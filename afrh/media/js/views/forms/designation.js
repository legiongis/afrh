define(['jquery',
    'underscore',
    'knockout-mapping',
    'views/forms/base',
    'views/forms/sections/branch-list'
    ], function ($, _, koMapping, BaseForm, BranchList) {

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
    }
    
    // custom validate function
    function checkNodes(nodes){
        
        // check to make sure there's actually a listing
        if (nodes[0]['value'] == ""){
            return false;
        }
        
        var from_date_check = isValidDate(nodes[1]['value'])[0];
        var to_date_check = isValidDate(nodes[2]['value'])[0];
        
        if (from_date_check == false || to_date_check == false) {
            return false;
        }
        
        return true
    }
        
    return BaseForm.extend({
        initialize: function() {
            
            BaseForm.prototype.initialize.apply(this);

            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            this.addBranchList(new BranchList({
                el: this.$el.find('#designation-section')[0],
                data: this.data,
                dataKey: 'PROTECTION_EVENT.E65',
                validateBranch: function (nodes) {
                    return checkNodes(nodes);
                }
            }));
        }
    });
});