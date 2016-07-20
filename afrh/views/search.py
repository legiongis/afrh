'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from datetime import datetime
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max, Min
from django.core.paginator import Paginator
from arches.app.models import models
from arches.app.views.search import get_paginator
from arches.app.views.search import build_search_results_dsl as build_base_search_results_dsl
from arches.app.models.concept import Concept
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.search.elasticsearch_dsl_builder import Bool, Match, Query, Nested, Terms, GeoShape, Range
from django.utils.translation import ugettext as _
from resources import get_allowed_types

def home_page(request):
    lang = request.GET.get('lang', settings.LANGUAGE_CODE)
    min_max_dates = models.Dates.objects.aggregate(Min('val'), Max('val'))

    return render_to_response('search.htm', {
            'main_script': 'search',
            'active_page': 'Search',
            'min_date': min_max_dates['val__min'].year if min_max_dates['val__min'] != None else 0,
            'max_date': min_max_dates['val__max'].year if min_max_dates['val__min'] != None else 1,
            'timefilterdata': JSONSerializer().serialize(Concept.get_time_filter_data())
        }, 
        context_instance=RequestContext(request))

def filter_protected(results,doc_type,entitytypeid,value):

    protect_ids = []
    all_entity_ids = all_entity_ids = [hit['_id'] for hit in results['hits']['hits']]
    for item in results['hits']['hits']:
        if item['_type'] == doc_type:
            res_id = item['_id']
            for node in item['_source']['child_entities']:
                if node['entitytypeid'] == entitytypeid:
                    if node['value'] == value:
                        protect_ids.append(res_id)
                    else:
                        all_entity_ids.append(res_id)

    results['hits']['hits'] = [hit for hit in results['hits']['hits'] if not hit['_id'] in protect_ids]
    results['hits']['total'] = results['hits']['total'] - len(protect_ids)

    good_eids = [i for i in all_entity_ids if not i in protect_ids]
    
    return results, good_eids
    
def add_neg_filter(query):
    '''adds a boolfilter that omits any resource that is protected with a certain
conceptid, this is simply a negative test for a specific conceptid'''
    
    # get all the protection level conceptid
    entries = Concept().get_e55_domain('PROTECTION_LEVEL.E55')
    for entry in entries:
        if entry['text'] == 'Protected':
            conceptid = entry['conceptid']

    # create boolfilter
    boolfilter = Bool()
    terms = Terms(field='domains.conceptid', terms=conceptid)
    nested = Nested(path='domains', query=terms)
    boolfilter.must_not(nested)
    
    # add filter to query
    query.add_filter(boolfilter)
    
    return query

def search_results(request):
    
    allowed_types = get_allowed_types(request)
    query = build_search_results_dsl(request)
    
    # filter protected resources for any non-logged in users
    if request.user.username == 'anonymous':
        query = add_neg_filter(query)
    
    results = query.search(index='entity', doc_type=allowed_types, )
    total = results['hits']['total']
    page = 1 if request.GET.get('page') == '' else int(request.GET.get('page', 1))
    all_entity_ids = ['_all']
    if request.GET.get('include_ids', 'false') == 'false':
        all_entity_ids = ['_none']
    elif request.GET.get('no_filters', '') == '':
        full_results = query.search(index='entity', doc_type='', start=0, limit=1000000, fields=[])
        all_entity_ids = [hit['_id'] for hit in full_results['hits']['hits']]

    return get_paginator(results, total, page, settings.SEARCH_ITEMS_PER_PAGE, all_entity_ids)
    
def build_search_results_dsl(request):
    temporal_filters = JSONDeserializer().deserialize(request.GET.get('temporalFilter', None))

    query = build_base_search_results_dsl(request)  
    boolfilter = Bool()

    if 'filters' in temporal_filters:
        for temporal_filter in temporal_filters['filters']:
            date_type = ''
            date = ''
            date_operator = ''
            for node in temporal_filter['nodes']:
                if node['entitytypeid'] == 'DATE_COMPARISON_OPERATOR.E55':
                    date_operator = node['value']
                elif node['entitytypeid'] == 'date':
                    date = node['value']
                else:
                    date_type = node['value']

            terms = Terms(field='date_groups.conceptid', terms=date_type)
            boolfilter.must(terms)

            date_value = datetime.strptime(date, '%Y-%m-%d').isoformat()

            if date_operator == '1': # equals query
                range = Range(field='date_groups.value', gte=date_value, lte=date_value)
            elif date_operator == '0': # greater than query 
                range = Range(field='date_groups.value', lt=date_value)
            elif date_operator == '2': # less than query
                range = Range(field='date_groups.value', gt=date_value)

            if 'inverted' not in temporal_filters:
                temporal_filters['inverted'] = False

            if temporal_filters['inverted']:
                boolfilter.must_not(range)
            else:
                boolfilter.must(range)

            query.add_filter(boolfilter)

    return query