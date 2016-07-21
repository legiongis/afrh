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

import re
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from arches.app.models import models
from django.db import transaction
from arches.app.models.concept import Concept
from arches.app.models.resource import Resource
from arches.app.models.entity import Entity
from django.http import HttpResponseNotFound
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Max, Min
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.utils.JSONResponse import JSONResponse
from arches.app.views.concept import get_preflabel_from_valueid, get_preflabel_from_conceptid
#from arches.app.views.resources import get_related_resources
from arches.app.views.search import build_search_results_dsl as build_base_search_results_dsl
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.search.elasticsearch_dsl_builder import Query, Terms, Bool, Match
import json
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import os
import geojson
import shapely.wkt

def report(request, resourceid):
    lang = request.GET.get('lang', settings.LANGUAGE_CODE)
    se = SearchEngineFactory().create()
    report_info = se.search(index='resource', id=resourceid)
    report_info['source'] = report_info['_source']
    report_info['type'] = report_info['_type']
    report_info['typename'] = settings.RESOURCE_TYPE_CONFIGS()[report_info['type']]['name']
    report_info['source']['graph'] = report_info['source']['graph']
    del report_info['_source']
    del report_info['_type']

    def get_evaluation_path(valueid):
        value = models.Values.objects.get(pk=valueid)
        concept_graph = Concept().get(id=value.conceptid_id, include_subconcepts=False, 
            include_parentconcepts=True, include_relatedconcepts=False, up_depth_limit=None, lang=lang)
        
        paths = []
        for path in concept_graph.get_paths(lang=lang)[0]:
            if path['label'] != 'Arches' and path['label'] != 'Evaluation Criteria Type':
                paths.append(path['label'])
        return '; '.join(paths)


    concept_label_ids = set()
    uuid_regex = re.compile('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
    # gather together all uuid's referenced in the resource graph
    def crawl(items):
        for item in items:
            for key in item:
                if isinstance(item[key], list):
                    crawl(item[key])
                else:
                    if isinstance(item[key], basestring) and uuid_regex.match(item[key]):
                        if key == 'EVALUATION_CRITERIA_TYPE_E55__value':
                            item[key] = get_evaluation_path(item[key])
                        concept_label_ids.add(item[key])

    crawl([report_info['source']['graph']])

    # get all the concept labels from the uuid's
    concept_labels = se.search(index='concept_labels', id=list(concept_label_ids))

    # convert all labels to their localized prefLabel
    temp = {}
    if concept_labels != None:
        for concept_label in concept_labels['docs']:
            #temp[concept_label['_id']] = concept_label
            if concept_label['found']:
                # the resource graph already referenced the preferred label in the desired language
                if concept_label['_source']['type'] == 'prefLabel' and concept_label['_source']['language'] == lang:
                    temp[concept_label['_id']] = concept_label['_source']
                else: 
                    # the resource graph referenced a non-preferred label or a label not in our target language, so we need to get the right label
                    temp[concept_label['_id']] = get_preflabel_from_conceptid(concept_label['_source']['conceptid'], lang)

    # replace the uuid's in the resource graph with their preferred and localized label                    
    def crawl_again(items):
        for item in items:
            for key in item:
                if isinstance(item[key], list):
                    crawl_again(item[key])
                else:
                    if isinstance(item[key], basestring) and uuid_regex.match(item[key]):
                        try:
                            item[key] = temp[item[key]]['value']
                        except:
                            pass

    crawl_again([report_info['source']['graph']])

    #return JSONResponse(report_info, indent=4)

    related_resource_dict = {
        'INVENTORY_RESOURCE': [],
        'CHARACTER_AREA': [],
        'MASTER_PLAN_ZONE': [],
        'ARCHAEOLOGICAL_ZONE': [],
        'HISTORIC_AREA': [],
        'ACTOR': [],
        'INFORMATION_RESOURCE_DOCUMENT': [],
        'INFORMATION_RESOURCE_IMAGE': [],
        'ACTIVITY_A': [],
        'ACTIVITY_B': []  
    }

    allowedtypes = get_allowed_types(request)
    anon = request.user.username == "anonymous"
    related_resource_info = get_related_resources(resourceid, lang, allowedtypes=allowedtypes,is_anon=anon)

    # parse the related entities into a dictionary by resource type
    for related_resource in related_resource_info['related_resources']:
        information_resource_type = 'DOCUMENT'
        related_resource['relationship'] = []
        if related_resource['entitytypeid'] == 'INVENTORY_RESOURCE.E18':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'RESOURCE_TYPE_CLASSIFICATION.E55':
                    related_resource['relationship'].append(get_preflabel_from_valueid(entity['value'], lang)['value'])
        elif related_resource['entitytypeid'] == 'CHARACTER_AREA.E53':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'RESOURCE_TYPE_CLASSIFICATION.E55':
                    related_resource['relationship'].append(get_preflabel_from_valueid(entity['value'], lang)['value'])
        elif related_resource['entitytypeid'] == 'MASTER_PLAN_ZONE.E53':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'ACTIVITY_TYPE.E55':
                    related_resource['relationship'].append(get_preflabel_from_valueid(entity['value'], lang)['value'])
        elif related_resource['entitytypeid'] == 'ARCHAEOLOGICAL_ZONE.E53':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'ACTOR_TYPE.E55':
                    related_resource['relationship'].append(get_preflabel_from_conceptid(entity['conceptid'], lang)['value'])
                    related_resource['actor_relationshiptype'] = ''
        elif related_resource['entitytypeid'] == 'HISTORIC_AREA.E53':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'HISTORICAL_EVENT_TYPE.E55':
                    related_resource['relationship'].append(get_preflabel_from_conceptid(entity['conceptid'], lang)['value'])
        elif related_resource['entitytypeid'] == 'ACTOR.E39':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'ACTOR_TYPE.E55':
                    related_resource['relationship'].append(get_preflabel_from_conceptid(entity['conceptid'], lang)['value'])
                    related_resource['actor_relationshiptype'] = ''
        elif related_resource['entitytypeid'] == 'ACTIVITY_A.E7':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'HISTORICAL_EVENT_TYPE.E55':
                    related_resource['relationship'].append(get_preflabel_from_conceptid(entity['conceptid'], lang)['value'])
        elif related_resource['entitytypeid'] == 'ACTIVITY_B.E7':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'ACTIVITY_B.E7':
                    related_resource['relationship'].append(get_preflabel_from_conceptid(entity['conceptid'], lang)['value'])
        elif related_resource['entitytypeid'] == 'INFORMATION_RESOURCE.E73':
            for entity in related_resource['domains']:
                if entity['entitytypeid'] == 'INFORMATION_RESOURCE_TYPE.E55':
                    related_resource['relationship'].append(get_preflabel_from_valueid(entity['value'], lang)['value'])
            for entity in related_resource['child_entities']:
                if entity['entitytypeid'] == 'FILE_PATH.E62':
                    related_resource['file_path'] = settings.MEDIA_URL + entity['label']
                if entity['entitytypeid'] == 'THUMBNAIL.E62':
                    related_resource['thumbnail'] = settings.MEDIA_URL + entity['label']
                    information_resource_type = 'IMAGE'
            
        # get the relationship between the two entities
        for relationship in related_resource_info['resource_relationships']:
            if relationship['entityid1'] == related_resource['entityid'] or relationship['entityid2'] == related_resource['entityid']: 
                related_resource['relationship'].append(get_preflabel_from_valueid(relationship['relationshiptype'], lang)['value'])

        entitytypeidkey = related_resource['entitytypeid'].split('.')[0]
        if entitytypeidkey == 'INFORMATION_RESOURCE':
            entitytypeidkey = '%s_%s' % (entitytypeidkey, information_resource_type)
        related_resource_dict[entitytypeidkey].append(related_resource)

    # set boolean to trigger display of related resource graph
    related_resource_flag = False
    for k,v in related_resource_dict.iteritems():
        if len(v) > 0:
            related_resource_flag = True
            break
            
    
    
    # create a few log files to help with debugging
    if settings.DEBUG:
        related_dict_log_path = os.path.join(settings.PACKAGE_ROOT,'logs','current_related_resource_dict.log')
        with open(related_dict_log_path,"w") as log:
            print >> log, json.dumps(related_resource_dict, sort_keys=True,indent=2, separators=(',', ': '))
            
        related_info_log_path = os.path.join(settings.PACKAGE_ROOT,'logs','current_related_resource_info.log')
        with open(related_info_log_path,"w") as log:
            print >> log, json.dumps(related_resource_info, sort_keys=True,indent=2, separators=(',', ': '))
            
        graph_log_path = os.path.join(settings.PACKAGE_ROOT,'logs','current_graph.json')
        with open(graph_log_path,"w") as log:
            print >> log, json.dumps(report_info['source']['graph'], sort_keys=True,indent=2, separators=(',', ': '))
            
    response_dict = {
        'geometry': JSONSerializer().serialize(report_info['source']['geometry']),
        'resourceid': resourceid,
        'report_template': 'views/reports/' + report_info['type'] + '.htm',
        'report_info': report_info,
        'related_resource_dict': related_resource_dict,
        'related_resource_flag': related_resource_flag,
        'main_script': 'resource-report',
        'active_page': 'ResourceReport'
    }
    
    # mine the result for specific geometry in certain cases and add to response dictionary
    if report_info['type'] == "ACTIVITY_A.E7":
        pa_geoms, ape_geoms = [], []
        if "PLACE_E53" in report_info['source']['graph']:
            for place in report_info['source']['graph']['PLACE_E53']:
                if "SPATIAL_COORDINATES_GEOMETRY_E47" in place:
                    wkt = place['SPATIAL_COORDINATES_GEOMETRY_E47'][0]['SPATIAL_COORDINATES_GEOMETRY_E47__value']
                    
                    g1 = shapely.wkt.loads(wkt)
                    g2 = geojson.Feature(geometry=g1, properties={})
                    json_geom = g2.geometry
                    
                    feat_type = place['SPATIAL_COORDINATES_GEOMETRY_E47'][0]['ACTIVITY_GEOMETRY_TYPE_E55__label']
                    if feat_type == "Project Area":
                        pa_geoms.append(json_geom)
                    if feat_type == "Area of Potential Effect":
                        ape_geoms.append(json_geom)
                    
                    
        if len(pa_geoms) > 0:
            pa_dict = {'type':'GeometryCollection','geometries':pa_geoms}
            response_dict['pa_geom'] = JSONSerializer().serialize(pa_dict)
        else:
            response_dict['pa_geom'] = 'null'
        if len(ape_geoms) > 0:
            ape_dict = {'type':'GeometryCollection','geometries':ape_geoms}
            response_dict['ape_geom'] = JSONSerializer().serialize(ape_dict)
        else:
            response_dict['ape_geom'] = 'null'
            
    if report_info['type'] == "ARCHAEOLOGICAL_ZONE.E53":
        bounds = []
        probs = {
            "Historic Resources":[],
            "Native American Resources":[],
            "Paleosols":[],
            "Disturbed Area":[]
        }
        if "PLACE_E53" in report_info['source']['graph']:
            for place in report_info['source']['graph']['PLACE_E53']:
                if "AREA_OF_PROBABILITY_GEOMETRY_E47" in place:
                    wkt = place['AREA_OF_PROBABILITY_GEOMETRY_E47'][0]['AREA_OF_PROBABILITY_GEOMETRY_E47__value']
                    
                    g1 = shapely.wkt.loads(wkt)
                    g2 = geojson.Feature(geometry=g1, properties={})
                    json_geom = g2.geometry
                    
                    feat_type = place['AREA_OF_PROBABILITY_GEOMETRY_E47'][0]['AREA_OF_PROBABILITY_GEOMETRY_TYPE_E55__label']
                    if feat_type in probs.keys():
                        probs[feat_type].append(json_geom)
                        
                if "ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY_E47" in place:
                    wkt = place['ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY_E47'][0]['ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY_E47__value']
                    
                    g1 = shapely.wkt.loads(wkt)
                    g2 = geojson.Feature(geometry=g1, properties={})
                    json_geom = g2.geometry
                    
                    bounds.append(json_geom)
        
        hr_dict = {'type':'GeometryCollection','geometries':probs["Historic Resources"]}
        response_dict['prob_hr'] = JSONSerializer().serialize(hr_dict)
        na_dict = {'type':'GeometryCollection','geometries':probs["Native American Resources"]}
        response_dict['prob_na'] = JSONSerializer().serialize(na_dict)
        p_dict = {'type':'GeometryCollection','geometries':probs["Paleosols"]}
        response_dict['prob_p'] = JSONSerializer().serialize(p_dict)
        da_dict = {'type':'GeometryCollection','geometries':probs["Disturbed Area"]}
        response_dict['prob_da'] = JSONSerializer().serialize(da_dict)
        bounds_dict = {'type':'GeometryCollection','geometries':bounds}
        response_dict['geometry'] = JSONSerializer().serialize(bounds_dict)
    
    ## THIS WAS AN ILL-FATED ATTEMPT TO NAME NAMES TO THE GEOMETRIES, NO WAIT, FEATURES, THAT ARE PASSED TO THE REPORTS
    ## FIX IF STATEMENT TO TRY AGAIN
    if report_info['type'] == "FIELD_INVLESTIGATION.E7":
        # return a FeatureCollection instead of a GeometryCollection for the field investigation report
        features = []
        if "SHOVEL_TEST_E7" in report_info['source']['graph']:
            for place in report_info['source']['graph']['SHOVEL_TEST_E7']:
                if "TEST_PIT_LOCATIONS_GEOMETRY_E47" in place:
                    wkt = place['TEST_PIT_LOCATIONS_GEOMETRY_E47'][0]['TEST_PIT_LOCATIONS_GEOMETRY_E47__value']
                    try:
                        feat_name = place['TEST_PIT_LOCATIONS_GEOMETRY_E47'][0]['SHOVEL_TEST_ID_E42__label']
                    except:
                        feat_name = ""
                    
                    g1 = shapely.wkt.loads(wkt)
                    g2 = geojson.Feature(geometry=g1, properties={"name":feat_name})
                    features.append(g2)
                    # print json.dumps(g2,indent=2)
                    # json_geom = g2.geometry
                    # json_geom['properties'] = {"name":feat_name}

                    # points.append(json_geom)
                    
        # print json.dumps(points[0],indent=2)
        points_dict = {'type':'FeatureCollection','features':features}
        response_dict['geometry'] = JSONSerializer().serialize(points_dict)
    
    return render_to_response('resource-report.htm', response_dict,
        context_instance=RequestContext(request))        

def map_layers(request, entitytypeid='all', get_centroids=False):

    data = []

    geom_param = request.GET.get('geom', None)

    bbox = request.GET.get('bbox', '')
    limit = request.GET.get('limit', settings.MAP_LAYER_FEATURE_LIMIT)
    entityids = request.GET.get('entityid', '')
    geojson_collection = {
      "type": "FeatureCollection",
      "features": []
    }
    
    se = SearchEngineFactory().create()
    query = Query(se, limit=limit)

    args = { 'index': 'maplayers' }
    if entitytypeid != 'all':
        args['doc_type'] = entitytypeid
    if entityids != '':
        for entityid in entityids.split(','):
            geojson_collection['features'].append(se.search(index='maplayers', id=entityid)['_source'])
        return JSONResponse(geojson_collection)

    data = query.search(**args)
    
    # if anonymous user, get list of protected entity ids to be excluded from map
    protected = []
    
    if request.user.username == 'anonymous':
        protected = get_protected_entityids()
        print protected

    for item in data['hits']['hits']:
        if item['_id'] in protected:
            print "hide this one"
            print json.dumps(item,indent=2)
            continue
        if get_centroids:
            item['_source']['geometry'] = item['_source']['properties']['centroid']
            item['_source'].pop('properties', None)
        elif geom_param != None:
            item['_source']['geometry'] = item['_source']['properties'][geom_param]
            item['_source']['properties'].pop('extent', None)
            item['_source']['properties'].pop(geom_param, None)
        else:
            item['_source']['properties'].pop('extent', None)
            item['_source']['properties'].pop('centroid', None)
        geojson_collection['features'].append(item['_source'])

    return JSONResponse(geojson_collection)
    
def polygon_layers(request, entitytypeid='all'):

    data = []
    geom_param = request.GET.get('geom', None)

    bbox = request.GET.get('bbox', '')
    limit = request.GET.get('limit', settings.MAP_LAYER_FEATURE_LIMIT)
    entityids = request.GET.get('entityid', '')
    geojson_collection = {
      "type": "FeatureCollection",
      "features": []
    }
    circ_features = []
    
    se = SearchEngineFactory().create()
    query = Query(se, limit=limit)

    args = { 'index': 'maplayers' }
    if entitytypeid != 'all':
        args['doc_type'] = entitytypeid
    
    data = query.search(**args)
    for item in data['hits']['hits']:
        for shape in item['_source']['geometry']['geometries']:
            feat = {
                "geometry":shape,
                "type":"Feature",
                "id":item['_source']['id']
            }
            if item['_source']['properties']['primaryname'] == "Circulation":
                circ_features.append(feat)
                continue                
            geojson_collection['features'].append(feat)

    for circ_feat in circ_features:
        geojson_collection['features'].append(circ_feat)

    return JSONResponse(geojson_collection)
    
    
    
def arch_layer(request, boundtype=''):

    data = []
    geom_param = request.GET.get('geom', None)

    bbox = request.GET.get('bbox', '')
    limit = request.GET.get('limit', settings.MAP_LAYER_FEATURE_LIMIT)
    geojson_collection = {
      "type": "FeatureCollection",
      "features": []
    }

    se = SearchEngineFactory().create()
    query = Query(se, limit=limit)

    args = {
        'index':'resource',
        '_type':'ARCHAEOLOGICAL_ZONE.E53',
    }

    #data = query.search(**args)
    
    data = se.search(index='resource', doc_type='ARCHAEOLOGICAL_ZONE.E53')
    
    pre_collection = []
    
    for item in data['hits']['hits']:
        if "PLACE_E53" in item['_source']['graph']:
            for geom in item['_source']['graph']['PLACE_E53']:
                
                if "AREA_OF_PROBABILITY_GEOMETRY_E47" in geom:

                    wkt = geom['AREA_OF_PROBABILITY_GEOMETRY_E47'][0]['AREA_OF_PROBABILITY_GEOMETRY_E47__value']
                    g1 = shapely.wkt.loads(wkt)
                    g2 = geojson.Feature(geometry=g1, properties={})
                    
                    feat = {
                        'geometry':g2.geometry,
                        'type':"Feature",
                        'id':item['_source']['entityid'],
                        'properties':{
                            'type':geom['AREA_OF_PROBABILITY_GEOMETRY_E47'][0]['AREA_OF_PROBABILITY_GEOMETRY_TYPE_E55__label']
                        }
                    }

                    geojson_collection['features'].append(feat)

                if "ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY_E47" in geom:
                    # for geom in item['_source']['graph']['PLACE_E53'][0]['ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY_E47']:
                    wkt = geom['ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY_E47'][0]['ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY_E47__value']
                    
                    g1 = shapely.wkt.loads(wkt)
                    g2 = geojson.Feature(geometry=g1, properties={})
                    #json_geom = g2.geometry
                    # feat_type = 'boundary'
                    # pre_collection.append((json_geom,feat_type))
                    feat = {
                        'geometry':g2.geometry,
                        'type':"Feature",
                        'id':item['_source']['entityid'],
                        'properties':{
                            'type':'boundary'
                        }
                    }
                    geojson_collection['features'].append(feat)
                
        if "SHOVEL_TEST_E7" in item['_source']['graph']:
            for st in item['_source']['graph']['SHOVEL_TEST_E7']:
                wkt = st['SHOVEL_TEST_GEOMETRY_E47'][0]['SHOVEL_TEST_GEOMETRY_E47__value']

                g1 = shapely.wkt.loads(wkt)
                g2 = geojson.Feature(geometry=g1, properties={})
                # json_geom = g2.geometry
                # feat_type = "shovel test"
                # pre_collection.append((json_geom,feat_type))
                feat = {
                    'geometry':g2.geometry,
                    'type':"Feature",
                    'id':item['_source']['entityid'],
                    'properties':{
                        'type':"shovel test"
                    }
                }
                geojson_collection['features'].append(feat)
    return JSONResponse(geojson_collection)

def act_a_layer(request, boundtype=''):

    data = []
    geom_param = request.GET.get('geom', None)

    bbox = request.GET.get('bbox', '')
    limit = request.GET.get('limit', settings.MAP_LAYER_FEATURE_LIMIT)
    geojson_collection = {
      "type": "FeatureCollection",
      "features": []
    }

    se = SearchEngineFactory().create()
    query = Query(se, limit=limit)

    data = se.search(index='resource', doc_type='ACTIVITY_A.E7')
    
    pre_collection = []
    
    for item in data['hits']['hits']:
        if "PLACE_E53" in item['_source']['graph']:
            for geom in item['_source']['graph']['PLACE_E53']:
                
                if geom['SPATIAL_COORDINATES_GEOMETRY_E47'][0]["ACTIVITY_GEOMETRY_TYPE_E55__label"] == "Project Area":
                    wkt = geom['SPATIAL_COORDINATES_GEOMETRY_E47'][0]['SPATIAL_COORDINATES_GEOMETRY_E47__value']
                    g1 = shapely.wkt.loads(wkt)
                    feat = geojson.Feature(geometry=g1, properties={})
                    feat['properties']['type'] = "Project Area"
                    feat['id'] = item['_source']['entityid']
                    geojson_collection['features'].append(feat)
                
                if geom['SPATIAL_COORDINATES_GEOMETRY_E47'][0]["ACTIVITY_GEOMETRY_TYPE_E55__label"] == "Area of Potential Effect":
                    wkt = geom['SPATIAL_COORDINATES_GEOMETRY_E47'][0]['SPATIAL_COORDINATES_GEOMETRY_E47__value']
                    g1 = shapely.wkt.loads(wkt)
                    feat = geojson.Feature(geometry=g1, properties={})
                    feat['properties']['type'] = "Area of Potential Effect"
                    feat['id'] = item['_source']['entityid']
                    geojson_collection['features'].append(feat)
    
    print json.dumps(geojson_collection,indent=2)
    return JSONResponse(geojson_collection)
    
def arch_investigation_layer(request, boundtype=''):

    data = []
    geom_param = request.GET.get('geom', None)

    bbox = request.GET.get('bbox', '')
    limit = request.GET.get('limit', settings.MAP_LAYER_FEATURE_LIMIT)
    geojson_collection = {
      "type": "FeatureCollection",
      "features": []
    }

    se = SearchEngineFactory().create()
    query = Query(se, limit=limit)

    args = {
        'index':'entity',
        'doc_type':'ARCHAEOLOGICAL_ZONE.E53',
    }

    data = query.search(**args)
    for item in data['hits']['hits']:
        for geom in item['_source']['geometries']:
            if geom['entitytypeid'] == 'SHOVEL_TEST_GEOMETRY.E47':
                print json.dumps(geom,indent=2)
                feat = {
                    'geometry':geom['value'],
                    'type':"Feature",
                    'id':item['_source']['entityid'],
                    }
                geojson_collection['features'].append(feat)

    return JSONResponse(geojson_collection)

@csrf_exempt
def resource_manager(request, resourcetypeid='', form_id='default', resourceid=''):

    ## get and check all permissions here
    permissions = request.user.get_all_permissions()
    res_perms = {k:[] for k in settings.RESOURCE_TYPE_CONFIGS().keys()}

    for k,v in res_perms.iteritems():
        for p in permissions:
            t,res = p.split(".")[:2]
            if k.startswith(res):
                v.append(t)

    if resourceid == '' and not 'CREATE' in res_perms[resourcetypeid]:
        return redirect(settings.LOGIN_URL)
    if not 'EDIT' in res_perms[resourcetypeid]:
        return redirect(settings.LOGIN_URL)
    ## finish permission testing

    if resourceid != '':
        resource = Resource(resourceid)
    elif resourcetypeid != '':
        resource = Resource({'entitytypeid': resourcetypeid})

    if form_id == 'default':
        form_id = resource.form_groups[0]['forms'][0]['id']

    form = resource.get_form(form_id)

    if request.method == 'DELETE':
        filtertypes = get_filter_types(request)
        resource.delete_index()
        se = SearchEngineFactory().create()
        relationships = resource.get_related_resources(return_entities=False)
        for relationship in relationships:
            se.delete(index='resource_relations', doc_type='all', id=relationship.resourcexid)
            relationship.delete()
        resource.delete()
        return JSONResponse({ 'success': True })

    if request.method == 'POST':
        data = JSONDeserializer().deserialize(request.POST.get('formdata', {}))
        form.update(data, request.FILES)

        with transaction.atomic():
            if resourceid != '':
                resource.delete_index()
            resource.save(user=request.user)
            resource.index()
            resourceid = resource.entityid

            return redirect('resource_manager', resourcetypeid=resourcetypeid, form_id=form_id, resourceid=resourceid)

    min_max_dates = models.Dates.objects.aggregate(Min('val'), Max('val'))
    
    if request.method == 'GET':
        if form != None:
            lang = request.GET.get('lang', settings.LANGUAGE_CODE)
            form.load(lang)
            return render_to_response('resource-manager.htm', {
                    'form': form,
                    'formdata': JSONSerializer().serialize(form.data),
                    'form_template': 'views/forms/' + form_id + '.htm',
                    'form_id': form_id,
                    'resourcetypeid': resourcetypeid,
                    'resourceid': resourceid,
                    'main_script': 'resource-manager',
                    'active_page': 'ResourceManger',
                    'resource': resource,
                    'resource_name': resource.get_primary_name(),
                    'resource_type_name': resource.get_type_name(),
                    'form_groups': resource.form_groups,
                    'min_date': min_max_dates['val__min'].year if min_max_dates['val__min'] != None else 0,
                    'max_date': min_max_dates['val__max'].year if min_max_dates['val__min'] != None else 1,
                    'timefilterdata': JSONSerializer().serialize(Concept.get_time_filter_data()),
                },
                context_instance=RequestContext(request))
        else:
            return HttpResponseNotFound('<h1>Arches form not found.</h1>')

@csrf_exempt
def related_resources(request, resourceid):

    ## get allowed resource types based on permissions
    allowedtypes = get_allowed_types(request)
    is_anon = False
    if request.user.username == "anonymous":
        is_anon = True
    
    if request.method == 'GET':
        lang = request.GET.get('lang', settings.LANGUAGE_CODE)
        start = request.GET.get('start', 0)
        resources = get_related_resources(resourceid, lang, start=start, limit=15, allowedtypes=allowedtypes, is_anon=is_anon)
        return JSONResponse(resources, indent=4)
    
    if 'edit' in request.user.user_groups and request.method == 'DELETE':
        se = SearchEngineFactory().create()
        data = JSONDeserializer().deserialize(request.body) 
        entityid1 = data.get('entityid1')
        entityid2 = data.get('entityid2')
        resourcexid = data.get('resourcexid')
        realtionshiptype = data.get('realtionshiptype')
        resource = Resource(entityid1)
        resource.delete_resource_relationship(entityid2, realtionshiptype)
        se.delete(index='resource_relations', doc_type='all', id=resourcexid)
        return JSONResponse({ 'success': True })

def get_related_resources(resourceid, lang, limit=1000, start=0, allowedtypes=[], is_anon=False):

    ret = {
        'resource_relationships': [],
        'related_resources': []
    }
    se = SearchEngineFactory().create()

    query = Query(se, limit=limit, start=start)
    query.add_filter(Terms(field='entityid1', terms=resourceid).dsl, operator='or')
    query.add_filter(Terms(field='entityid2', terms=resourceid).dsl, operator='or')
    resource_relations = query.search(index='resource_relations', doc_type="all")

    entityids = set()
    for relation in resource_relations['hits']['hits']:
        relation['_source']['preflabel'] = get_preflabel_from_valueid(relation['_source']['relationshiptype'], lang)
        ret['resource_relationships'].append(relation['_source'])
        entityids.add(relation['_source']['entityid1'])
        entityids.add(relation['_source']['entityid2'])
    if len(entityids) > 0:
        entityids.remove(resourceid)

    # can't figure why passing allowed types to doc_type param doesn't work,
    # so filter is carried out later
    related_resources = se.search(index='entity', doc_type='_all', id=list(entityids))

    filtered_ids = []
    if related_resources:
        for resource in related_resources['docs']:
            if not resource['_type'] in allowedtypes:
                filtered_ids.append(resource['_source']['entityid'])
                continue
            
            if is_anon:
                # filter out protected resources if user is anonymous
                # (this is basically a subset of the get_protected_entityids below
                # they should be combined probably)
                from search import get_protection_conceptids
                protect_id = get_protection_conceptids(settings.PROTECTION_LEVEL_NODE)
                conceptids = [d['conceptid'] for d in resource['_source']['domains']]
                if protect_id in conceptids:
                    filtered_ids.append(resource['_source']['entityid'])
                    continue
            ret['related_resources'].append(resource['_source'])
    
    if len(filtered_ids) > 0:
        # remove all relationships in ret that match a filtered id (this lc is yuge but I think concise)
        filtered_relationships = [rel for rel in ret['resource_relationships'] if not rel['entityid1'] in filtered_ids and not rel['entityid2'] in filtered_ids]
        
        # update ret values
        ret['resource_relationships'] = filtered_relationships
        
    ret['total'] = len(ret['resource_relationships'])
    
    return ret
    
def filter_protected(results,doc_type,entitytypeid,value):
    print "a"
    protect_ids = []
    print "b"
    print results
    #all_entity_ids = [hit['_id'] for hit in results['hits']['hits']]
    print "c"
    for item in results['docs']:
        print item
        if item['_type'] == doc_type:
            res_id = item['_id']
            print res_id
            print json.dumps(item,indent=2)
            for node in item['_source']['child_entities']:
                #print json.dumps(node,indent=2)
                if node['entitytypeid'] == entitytypeid:
                    if node['value'] == value:
                        protect_ids.append(res_id)
                    else:
                        all_entity_ids.append(res_id)

    results['hits']['hits'] = [hit for hit in results['hits']['hits'] if not hit['_id'] in protect_ids]
    results['hits']['total'] = results['hits']['total'] - len(protect_ids)

    #good_eids = [i for i in all_entity_ids if not i in protect_ids]
    
    return results, good_eids

def edit_history(request, resourceid=''):
    ret = []
    current = None
    index = -1
    start = request.GET.get('start', 0)
    limit = request.GET.get('limit', 10)
    if resourceid != '':
        dates = models.EditLog.objects.filter(resourceid = resourceid).values_list('timestamp', flat=True).order_by('-timestamp').distinct('timestamp')[start:limit]
        # dates = models.EditLog.objects.datetimes('timestamp', 'second', order='DESC')

        for log in models.EditLog.objects.filter(resourceid = resourceid, timestamp__in = dates).values().order_by('-timestamp', 'attributeentitytypeid'):
            if str(log['timestamp']) != current:
                current = str(log['timestamp']) 
                ret.append({'date':str(log['timestamp'].date()), 'time': str(log['timestamp'].time().replace(microsecond=0).isoformat()), 'log': []})
                index = index + 1

            ret[index]['log'].append(log)
            
    return JSONResponse(ret, indent=4)

def get_admin_areas(request):
    geomString = request.GET.get('geom', '')
    geom = GEOSGeometry(geomString)
    intersection = models.Overlays.objects.filter(geometry__intersects=geom)
    return JSONResponse({'results': intersection}, indent=4)

def get_filter_types(request):
    ''' references the user permissions in the request and returns a list of resource types to filter'''

    if request.user.username == 'anonymous':
        return ['ACTIVITY_A.E7','ACTIVITY_B.E7']
        
    filtertypes = settings.RESOURCE_TYPE_CONFIGS().keys()
    permissions = request.user.get_all_permissions()
    for k in settings.RESOURCE_TYPE_CONFIGS().keys():
        for p in permissions:
            t,res = p.split(".")[:2]
            if not t == "VIEW":
                continue
            if k.startswith(res):
                filtertypes.remove(k)

    return filtertypes
    
def get_allowed_types(request):
    ''' references the user permissions in the request and returns a list of resource types to allow in a search query'''
    allowedtypes = []
    permissions = request.user.get_all_permissions()

    for k in settings.RESOURCE_TYPE_CONFIGS().keys():
        if request.user.username == 'anonymous':
            if not k in ['ACTIVITY_A.E7','ACTIVITY_B.E7']:
                allowedtypes.append(k)
                continue
        for p in permissions:
            t,res = p.split(".")[:2]
            if not t == "VIEW":
                continue
            if k.startswith(res):
                allowedtypes.append(k)

    return allowedtypes
    
def get_protected_entityids():
    '''returns list of entity ids for protected resources'''
    
    from search import get_protection_conceptids
    protect_id = get_protection_conceptids(settings.PROTECTION_LEVEL_NODE)
    filtered_ids = []
    se = SearchEngineFactory().create()
    
    # for some reason doc_type must be speficied with INFORMATION RESOURCE in order for that type
    # to be queried. right now this is ok, because it's the only type with protection levels,
    # but this is very strange.
    all_resources = se.search(index='entity', doc_type="INFORMATION_RESOURCE.E73")['hits']['hits']
    for resource in all_resources:
        conceptids = [d['conceptid'] for d in resource['_source']['domains']]
        if protect_id in conceptids:
            filtered_ids.append(resource['_source']['entityid'])

    return filtered_ids