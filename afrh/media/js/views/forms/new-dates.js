define(['jquery', 
    'underscore', 
    'knockout-mapping',
    'views/forms/base',
    'views/forms/sections/validation',
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], 
    function ($, _, koMapping, BaseForm, ValidationTools, BranchList) {
        
        //load all validation functions stored in views/forms/sections/validation.js
        var vt = new ValidationTools;
        
        return BaseForm.extend({
            
            initialize: function() {

                BaseForm.prototype.initialize.apply(this);                
                
                
            }
        });
    }
);