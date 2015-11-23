define([
    'jquery',
    'underscore',
    'knockout',
    'knockout-mapping',
    'openlayers',
    'arches',
    'resource-types',
    'views/search/term-filter-actors', 
    'views/search/map-filter',
    'views/search/time-filter',
    'views/search/search-results',
    'views/forms/sections/branch-list',
    'views/forms/base',
    'plugins/bootstrap-slider/bootstrap-slider.min',
    'bootstrap-datetimepicker',
    'plugins/knockout-select2',
    'summernote'
], function ($, _, ko, koMapping, ol, arches, resourceTypes, TermFilter, MapFilter, TimeFilter, SearchResults, BranchList, BaseForm) {
    var wkt = new ol.format.WKT();

    return BaseForm.extend({

        updateRequest: '',

        initialize: function() {
            var mapFilterText, timeFilterText;
            var self = this;

            ko.bindingHandlers.datePicker = {
                init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext){          
                    var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});

                    date_picker.on('dp.change', function(evt){
                        $(this).find('input').trigger('change'); 
                    });
                }
            };

            ko.bindingHandlers.relationshipTypeSelect = {
                update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext){
                    var branch = viewModel.getEditedBranch();
                    if (!branch.relationship.relationshiptype()) {
                        return;
                    }
                    var label = branch.relationship.relationshiptype().label;
                    if (branch.relationshiptypelabel() !== label) {
                        branch.relationshiptypelabel(label);
                    }
                }
            };

            BaseForm.prototype.initialize.apply(this);
            var resourceId = this.data['resource-id'];
            console.log(this.data);
            var defaultRelationshipType = this.data['related-resources']['default_relationship_type'];

            
            this.searchbox = this.$el.select2({
                dropdownCssClass: 'resource_search_widget_dropdown',
                multiple: true,
                minimumInputLength: 2,
                ajax: {
                    url: arches.urls.search_results,
                    dataType: 'json',
                    data: function (term, page) {
                        return {
                            q: term, // search term
                            page_limit: 30
                        };
                    },
                    results: function (data, page) {
                        var value = $('div.resource_search_widget').find('.select2-input').val();

                        // this result is being hidden by a style in arches.css 
                        // .select2-results li:first-child{
                        //     display:none;
                        // } 
                        var results = [{
                            inverted: false,
                            type: 'string',
                            context: '',
                            context_label: '',
                            id: value,
                            text: value,
                            value: value
                        }];
                        $.each(data.hits.hits, function(){
                            results.push({
                                inverted: false,
                                type: this._source.options.conceptid ? 'concept' : 'term',
                                context: this._source.context,
                                context_label: this._source.options.context_label,
                                id: this._source.term + this._source.context,
                                text: this._source.term,
                                value: this._source.options.conceptid ? this._source.options.conceptid : this._source.term
                            });
                        }, this);
                        return {results: results};
                    }
                },
                formatResult:function(result, container, query, escapeMarkup){
                    var markup=[];
                    window.Select2.util.markMatch(result.text, query.term, markup, escapeMarkup);
                    var context = result.context_label != '' ? '<i class="concept_result_schemaname">(' + result.context_label + ')</i>' : '';
                    var formatedresult = '<span class="concept_result">' + markup.join("")  + '</span>' + context;
                    return formatedresult;
                },
                formatSelection: function(result){
                    var context = result.context_label != '' ? '<i class="concept_result_schemaname">(' + result.context_label + ')</i>' : '';
                    var markup = '<span data-filter="external-filter"><i class="fa fa-minus" style="margin-right: 7px;display:none;"></i>' + result.text + '</span>' + context;
                    if(result.inverted){
                        markup = '<span data-filter="external-filter"><i class="fa fa-minus inverted" style="margin-right: 7px;"></i>' + result.text + '</span>' + context;
                    }
                    return markup;
                },
                escapeMarkup: function(m) { return m; }
            })
            
            
            
            var relationBranchList = new BranchList({
                el: this.$el.find('.relation-list')[0],
                data: this.data,
                dataKey: 'related-resources',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                },
                addBlankEditBranch: function(){
                    return null;
                },
                editItem: function(branch, e) {
                    var editingBranch = this.getEditedBranch();
                    if (editingBranch) {
                        editingBranch.editing(false);
                    }
                    this.originalItem = koMapping.toJS(branch);
                    branch.editing(true);
                    
                    this.trigger('change', 'edit', branch);
                },
                deleteItem: function(branch, e) {
                    this.trigger('change', 'delete', branch);   
                    this.viewModel.branch_lists.remove(branch);
                    branch.related(false);
                },
                getData: function(){
                    var data = koMapping.toJS(this.viewModel.branch_lists());
                    _.each(data, function(item){
                        var i = item;
                        delete item.editing;
                    }, this); 
                    return data;
                },
                getEditedBranchTypeInfo: function() {
                    if (!this.getEditedBranch()) {
                        return {};
                    }
                    return resourceTypes[this.getEditedBranch().relatedresourcetype()];
                }
            });

            this.addBranchList(relationBranchList);

            this.termFilter = new TermFilter({
                el: $.find('input.resource_search_widget')[0]
            });
            this.termFilter.on('change', function(){
                if($('#saved-searches').is(":visible")){
                    this.hideSavedSearches();
                }
            }, this);
            this.termFilter.on('filter-removed', function(item){
                console.log(this.termFilter.data);
                if(item.text === mapFilterText){
                    this.mapFilter.clear();
                }
                if(item.text === timeFilterText){
                    this.timeFilter.clear();
                }
            }, this);
            this.termFilter.on('filter-inverted', function(item){
                if(item.text === mapFilterText){
                    this.mapFilter.query.filter.inverted(item.inverted);
                }
                if(item.text === timeFilterText){
                    this.timeFilter.query.filter.inverted(item.inverted);
                }
            }, this);


            this.mapFilter = new MapFilter({
                el: $('#map-filter-container')[0]
            });
            this.mapFilter.on('enabled', function(enabled, inverted){
                if(enabled){
                    this.termFilter.addTag(mapFilterText, inverted);
                }else{
                    this.termFilter.removeTag(mapFilterText);
                }
            }, this);


            this.timeFilter = new TimeFilter({
                el: $('#time-filter-container')[0]
            });
            this.timeFilter.on('enabled', function(enabled, inverted){
                if(enabled){
                    this.termFilter.addTag(timeFilterText, inverted);
                }else{
                    this.termFilter.removeTag(timeFilterText);
                }
            }, this);


            this.searchResults = new SearchResults({
                el: $('#search-results-container')[0],
                updateResults: function(results){
                    var self = this;
                    this.paginator(results);
                    var data = $('div[name="search-result-data"]').data();
                    
                    this.total(data.results.hits.total);
                    self.results.removeAll();
                    
                    $.each(data.results.hits.hits, function(){
                        var description = resourceTypes[this._source.entitytypeid].defaultDescription;
                        var descriptionNode = resourceTypes[this._source.entitytypeid].descriptionNode;
                        $.each(this._source.child_entities, function(i, entity){
                            if (entity.entitytypeid === descriptionNode){
                                description = entity.value;
                            }
                        })

                        var relationBranch = koMapping.fromJS({
                            "relationship": {
                                "notes": "",
                                "entityid2": resourceId,
                                "entityid1": this._source.entityid,
                                "resourcexid": null,
                                "datestarted": null,
                                "dateended": null,
                                "relationshiptype": defaultRelationshipType
                            },
                            "relatedresourcetype": this._source.entitytypeid,
                            "relationshiptypelabel": "",
                            "nodes": [
                                {
                                    "label": "",
                                    "value": "",
                                    "entitytypeid": this._source.entitytypeid,
                                    "parentid": null,
                                    "entityid": this._source.entityid,
                                    "property": "",
                                    "businesstablename": ""
                                }
                            ],
                            "relatedresourcename": this._source.primaryname,
                            "relatedresourceid": this._source.entityid,
                            "editing": false,
                            "related": false
                        });

                        var entityid = this._source.entityid;
                        _.each(relationBranchList.viewModel.branch_lists(), function (branch) {
                            if (branch.relatedresourceid() === entityid) {
                                relationBranch = branch;
                            }
                        });

                        self.results.push({
                            primaryname: this._source.primaryname,
                            resourceid: this._source.entityid,
                            entitytypeid: this._source.entitytypeid,
                            description: description,
                            geometries: ko.observableArray(this._source.geometries),
                            typeIcon: resourceTypes[this._source.entitytypeid].icon,
                            typeName: resourceTypes[this._source.entitytypeid].name,
                            editing: ko.computed(function () {
                                if (relationBranch) {
                                    return relationBranch.editing();
                                }
                                return false;
                            }),
                            relationBranch: relationBranch,
                            relationBranchList: relationBranchList,
                            domains: relationBranchList.viewModel.domains,
                            addClick: function () {
                                relationBranchList.addItem();
                            },
                            discardClick: function () {
                                relationBranchList.undoCurrentEdit();
                            },
                            editClick: function () {
                                if (relationBranch.related()) {
                                    relationBranchList.editItem(relationBranch);
                                } else {
                                    if (relationBranchList.getEditedBranch()) {
                                        relationBranchList.addItem();
                                    }
                                    relationBranch.related(true);
                                    relationBranch.editing(true);
                                    relationBranchList.viewModel.branch_lists.push(relationBranch);
                                }
                            },
                            getEditedBranch: function () {
                                return relationBranchList.getEditedBranch()
                            }
                        });
                    });

                    return data;
                },
            });
            this.searchResults.on('mouseover', function(resourceid){
                this.mapFilter.selectFeatureById(resourceid);
            }, this);
            this.searchResults.on('mouseout', function(){
                this.mapFilter.unselectAllFeatures();
            }, this);
            this.searchResults.on('find_on_map', function(resourceid, data){
                var extent,
                    expand = !this.mapFilter.expanded();
                if (expand) {
                    this.mapFilter.expanded(true);
                }
                
                _.each(data.geometries, function (geometryData) {
                    var geomExtent = wkt.readGeometry(geometryData.label).getExtent();
                    geomExtent = ol.extent.applyTransform(geomExtent, ol.proj.getTransform('EPSG:4326', 'EPSG:3857'));
                    extent = extent ? ol.extent.extend(extent, geomExtent) : geomExtent;
                });
                if (extent) {
                    _.delay(function() {
                        self.mapFilter.zoomToExtent(extent);
                    }, expand ? 700 : 0);
                }
            }, this);


            mapFilterText = this.mapFilter.$el.data().filtertext;
            timeFilterText = this.timeFilter.$el.data().filtertext;

            self.isNewQuery = true;
            this.searchQuery = {
                queryString: function(){
                    var params = {
                        page: self.searchResults.page(),
                        termFilter: ko.toJSON(self.termFilter.query.filter.terms()),
                        temporalFilter: ko.toJSON({
                            year_min_max: self.timeFilter.query.filter.year_min_max(),
                            filters: self.timeFilter.query.filter.filters(),
                            inverted: self.timeFilter.query.filter.inverted()
                        }),
                        spatialFilter: ko.toJSON(self.mapFilter.query.filter),
                        mapExpanded: self.mapFilter.expanded(),
                        timeExpanded: self.timeFilter.expanded()
                    };
                    if (self.termFilter.query.filter.terms().length === 0 &&
                        self.timeFilter.query.filter.year_min_max().length === 0 &&
                        self.timeFilter.query.filter.filters().length === 0 &&
                        self.mapFilter.query.filter.geometry.coordinates().length === 0) {
                        params.no_filters = true;
                    }

                    params.include_ids = self.isNewQuery;
                    return $.param(params).split('+').join('%20');
                },
                changed: ko.pureComputed(function(){
                    var ret = ko.toJSON(this.termFilter.query.changed()) +
                        ko.toJSON(this.timeFilter.query.changed()) +
                        ko.toJSON(this.mapFilter.query.changed());
                    return ret;
                }, this).extend({ rateLimit: 200 })
            };

            this.getSearchQuery();

            this.searchResults.page.subscribe(function(){
                self.doQuery();
            });

            this.searchQuery.changed.subscribe(function(){
                self.isNewQuery = true;
                self.searchResults.page(1);
                self.doQuery();
            });

            this.doQuery();
        },

        toggleForm: function(evt) {
            evt.preventDefault();

            $('.start-workflow-controls').toggle();
            $('.show-relationships-controls').toggle();
            $('.relation-list').toggle();
            $('.relation-form').toggle();
        },

        doQuery: function () {
            var self = this;
            var queryString = this.searchQuery.queryString();
            if (this.updateRequest) {
                this.updateRequest.abort();
            }

            $('.form-load-mask').show();

            this.updateRequest = $.ajax({
                type: "GET",
                url: arches.urls.search_results,
                data: queryString,
                success: function(results){
                    var data = self.searchResults.updateResults(results);
                    self.mapFilter.highlightFeatures(data, $('.search-result-all-ids').data('results'));
                    self.mapFilter.applyBuffer();
                    self.isNewQuery = false;
                    $('.form-load-mask').hide();
                },
                error: function(){}
            });
        },

        showSavedSearches: function(){
            this.clear();
            $('#saved-searches').slideDown('slow');
            $('#search-results').slideUp('slow');
            this.mapFilter.expanded(false);
            this.timeFilter.expanded(false);
        },

        hideSavedSearches: function(){
            $('#saved-searches').slideUp('slow');
            $('#search-results').slideDown('slow');
        },

        toggleMapFilter: function(evt){
            evt.preventDefault();
            if($('#saved-searches').is(":visible")){
                this.doQuery();
                this.hideSavedSearches();
            }
            this.mapFilter.expanded(!this.mapFilter.expanded());
        },

        toggleTimeFilter: function(evt){
            evt.preventDefault();
            if($('#saved-searches').is(":visible")){
                this.doQuery();
                this.hideSavedSearches();
            }
            this.timeFilter.expanded(!this.timeFilter.expanded());
        },

        toggleAttributeFilter: function(evt){
            evt.preventDefault();
            $('#attribute').slideToggle(600);
        },

        getSearchQuery: function(){
            var doQuery = false;
            var query = _.chain(decodeURIComponent(location.search).slice(1).split('&') )
                // Split each array item into [key, value]
                // ignore empty string if search is empty
                .map(function(item) { if (item) return item.split('='); })
                // Remove undefined in the case the search is empty
                .compact()
                // Turn [key, value] arrays into object parameters
                .object()
                // Return the value of the chain operation
                .value();

            if('page' in query){
                query.page = JSON.parse(query.page);
                doQuery = true;
            }
            this.searchResults.restoreState(query.page);


            if('termFilter' in query){
                query.termFilter = JSON.parse(query.termFilter);
                doQuery = true;
            }
            this.termFilter.restoreState(query.termFilter);


            if('temporalFilter' in query){
                query.temporalFilter = JSON.parse(query.temporalFilter);
                doQuery = true;
            }
            if('timeExpanded' in query){
                query.timeExpanded = JSON.parse(query.timeExpanded);
                doQuery = true;
            }
            this.timeFilter.restoreState(query.temporalFilter, query.timeExpanded);


            if('spatialFilter' in query){
                query.spatialFilter = JSON.parse(query.spatialFilter);
                doQuery = true;
            }
            if('mapExpanded' in query){
                query.mapExpanded = JSON.parse(query.mapExpanded);
                doQuery = true;
            }
            this.mapFilter.restoreState(query.spatialFilter, query.mapExpanded);
            

            if(doQuery){
                this.doQuery();
                this.hideSavedSearches();
            }
            
        },

        clear: function(){
            this.mapFilter.clear();
            this.timeFilter.clear();
            this.termFilter.clear();
        },
    });
});