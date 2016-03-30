define(['jquery', 'views/forms/base', 'views/forms/sections/branch-list', ], function ($, BaseForm, BranchList) {
        return BaseForm.extend({
            initialize: function() {
                BaseForm.prototype.initialize.apply(this);                
                var self = this;
                
                console.log(this.data);

                this.addBranchList(new BranchList({
                    el: this.$el.find('#titles-section')[0],
                    data: this.data,
                    dataKey: 'TITLE.E41',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#identifiers-section')[0],
                    data: this.data,
                    dataKey: 'EXTERNAL_RESOURCE.E1',
                    validateBranch: function (nodes) {
                        console.log(nodes);
                        return this.validateHasValues(nodes);
                    },
                    isUrl: function(value) {
                        console.log(value);
                        return /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/.test(value);
                    },
                    getLink: function(value) {
                        if (/^https?:\/\//.test(value)) {
                            return value;
                        } else {
                            return 'http://' + value;
                        }
                    }
                }));
                
                this.addBranchList(new BranchList({
                    el: this.$el.find('#type-section')[0],
                    data: this.data,
                    dataKey: 'INFORMATION_RESOURCE_TYPE_ASSIGNMENT.E17',
                    validateBranch: function (nodes) {
                        console.log(nodes);
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#languages-section')[0],
                    data: this.data,
                    dataKey: 'LANGUAGE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#keywords-section')[0],
                    data: this.data,
                    dataKey: 'KEYWORD.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
            }
        });
});


