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
from django.conf import settings
import arches.app.models.models as archesmodels
from arches.app.models.edit_history import EditHistory
from arches.app.models.resource import Resource as ArchesResource
from arches.app.models.entity import Entity
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from forms import summary
from forms import description
from forms import location
from forms import other
from forms import wizard
from forms import review
from arches.app.models.forms import DeleteResourceForm
from django.utils.translation import ugettext as _
import json
import os

class Resource(ArchesResource):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        description_group = {
            'id': 'resource-description',
            'icon':'fa-folder',
            'name': _('Resource Description'),
            'forms': []
        }
        review_group = {
            'id': 'resource-reviews',
            'icon':'fa-clipboard',
            'name': _('Reviews'),
            'forms': []
        }
        manage_group = {
            'id': 'manage-resource',
            'icon': 'fa-wrench',
            'name': _('Manage Resource'),
            'forms': [
                EditHistory.get_info(),
                DeleteResourceForm.get_info()
            ]
        }

        if self.entitytypeid == 'INVENTORY_RESOURCE.E18':
            description_group['forms'] = [
                summary.InventorySummaryForm.get_info(), 
                description.InventoryDescriptionForm.get_info(),
                other.FunctionAndUseForm.get_info(),
                other.FormDimensionForm.get_info(),
                other.ComponentForm.get_info(),
                location.LocationForm.get_info(),
                wizard.ConditionForm.get_info(),
                wizard.RelatedFilesForm.get_info(),
                other.InventoryEvaluationForm.get_info(),
                other.ExternalReferenceForm.get_info(),
            ]

        if self.entitytypeid == 'CHARACTER_AREA.E53':
            description_group['forms'] = [
                summary.CharAreaSummaryForm.get_info(),
                description.CharAreaDescriptionForm.get_info(),
                other.CharAreaGuidelinesForm.get_info(),
                location.SimpleLocationForm.get_info(),
            ]
            
        if self.entitytypeid == 'MASTER_PLAN_ZONE.E53':
            description_group['forms'] = [
                summary.MPZoneSummaryForm.get_info(),
                description.InventoryDescriptionForm.get_info(),
                location.SimpleLocationForm.get_info(),
                wizard.MPZoneGuidelinesForm.get_info(),
            ]
            
        if self.entitytypeid == 'ARCHAEOLOGICAL_ZONE.E53':
            description_group['forms'] = [
                summary.ArchZoneSummaryForm.get_info(),
                location.SimpleLocationForm.get_info(),
                location.ProbabilityAreaForm.get_info(),
                wizard.ArchZoneInvestigationForm.get_info(),
            ]
            
        if self.entitytypeid == 'HISTORIC_AREA.E53':
            description_group['forms'][:0] = [
                summary.DesSummaryForm.get_info(),
                location.SimpleLocationForm.get_info(),
                description.DesDescriptionForm.get_info(),
                other.DesEvaluationForm.get_info(),
            ]

        if self.entitytypeid == 'ACTOR.E39':
            description_group['forms'] = [
                summary.ActorSummaryForm.get_info(), 
                description.InventoryDescriptionForm.get_info(),
                location.LocationForm.get_info(),
                wizard.RelatedFilesForm.get_info(),
                other.ExternalReferenceForm.get_info()
            ]

        if self.entitytypeid == 'INFORMATION_RESOURCE.E73':
            description_group['forms'] = [
                summary.InformationResourceSummaryForm.get_info(), 
                other.PublicationForm.get_info(),
                location.LocationForm.get_info(),
                description.InventoryDescriptionForm.get_info(),
                wizard.FileUploadForm.get_info()
            ]
 
        if self.entitytypeid == 'ACTIVITY_A.E7':
            description_group['forms'] = [
                summary.ActivityForm.get_info(),
                location.ActALocationForm.get_info(),
                description.ActADescriptionForm.get_info(),
                wizard.ActivityConsultationForm.get_info(),
                other.EntitiesForm.get_info(),
            ]
            review_group['forms'] = [
                review.Section106ReviewForm.get_info(),
                review.ARPAReviewForm.get_info(),
                review.NEPAReviewForm.get_info(),
                review.NCPCReviewForm.get_info(),
                review.CFAReviewForm.get_info(),
            ]

        if self.entitytypeid == 'ACTIVITY_B.E7':
            description_group['forms'] = [
                summary.ActivityForm.get_info(),
                location.SimpleLocationForm.get_info(),
                description.ActBDescriptionForm.get_info(),
                wizard.ActivityConsultationForm.get_info(),
                other.EntitiesForm.get_info(),
            ]
            review_group['forms'] = [
                review.ARPAReviewForm.get_info(),
                review.NEPAReviewForm.get_info(),
                review.HPOHPRBReviewForm.get_info(),
                review.NCPCReviewForm.get_info(),
                review.CFAReviewForm.get_info(),
            ]
        
        ## all resource types get the related resource form
        description_group['forms'].append(other.RelatedResourcesForm.get_info())
            
        self.form_groups.append(description_group)
        
        if len(review_group['forms']) != 0:
            self.form_groups.append(review_group)

        if self.entityid != '':
            self.form_groups.append(manage_group)
        
        if self.entityid != '':
            se = SearchEngineFactory().create()
            resource = se.search(index='resource', id=self.entityid)
            resource_graph = resource['_source']['graph']
            log_path = os.path.join(settings.PACKAGE_ROOT,'logs','current_graph.json')
            with open(log_path,"w") as log:
                print >> log, json.dumps(resource_graph, sort_keys=True,indent=2, separators=(',', ': '))

    def get_primary_name(self):
        """
        Gets the primary name based on lookup values stored in the resource type configs
        """
        
        displayname = super(Resource, self).get_primary_name()
        
        lookup = settings.RESOURCE_TYPE_CONFIGS()[self.entitytypeid]['primary_name_lookup']['lookup_value']
        names = self.get_names()
        for name in names:
            if lookup:
                if name.find_entities_by_type_id(lookup[0])[0].label == lookup[1]:
                    displayname = name.value
            else:
                displayname = name.value
                break
        return displayname


    def get_names(self):
        """
        Gets the human readable name to display for entity instances
        """
        names = []
        name_nodes = self.find_entities_by_type_id(settings.RESOURCE_TYPE_CONFIGS()[self.entitytypeid]['primary_name_lookup']['entity_type'])
        if len(name_nodes) > 0:
            for name in name_nodes:
                names.append(name)
        return names

    def index(self):
        """
        Indexes all the nessesary documents related to resources to support the map, search, and reports

        """
        se = SearchEngineFactory().create()

        search_documents = self.prepare_documents_for_search_index()
        for document in search_documents:
            se.index_data('entity', self.entitytypeid, document, id=self.entityid)

            report_documents = self.prepare_documents_for_report_index(geom_entities=document['geometries'])
            for report_document in report_documents:
                se.index_data('resource', self.entitytypeid, report_document, id=self.entityid)

            geojson_documents = self.prepare_documents_for_map_index(geom_entities=document['geometries'])
            
            for geojson in geojson_documents:
                se.index_data('maplayers', self.entitytypeid, geojson, idfield='id')

        for term in self.prepare_terms_for_search_index():
           se.index_term(term['term'], term['entityid'], term['context'], term['options'])
        
    def prepare_documents_for_search_index(self):
        """
        Generates a list of specialized resource based documents to support resource search
        """

        documents = super(Resource, self).prepare_documents_for_search_index()

        for document in documents:
            document['date_groups'] = []
            for nodes in self.get_nodes('BEGINNING_OF_EXISTENCE.E63', keys=['value']):
                document['date_groups'].append({
                    'conceptid': nodes['BEGINNING_OF_EXISTENCE_TYPE_E55__value'],
                    'value': nodes['START_DATE_OF_EXISTENCE_E49__value']
                })

            for nodes in self.get_nodes('END_OF_EXISTENCE.E64', keys=['value']):
                document['date_groups'].append({
                    'conceptid': nodes['END_OF_EXISTENCE_TYPE_E55__value'],
                    'value': nodes['END_DATE_OF_EXISTENCE_E49__value']
                })

        return documents

    def prepare_documents_for_map_index(self, geom_entities=[]):
        """
        Generates a list of geojson documents to support the display of resources on a map
        """
        documents = super(Resource, self).prepare_documents_for_map_index(geom_entities=geom_entities)
        
        
        
        def get_entity_data(entitytypeid, get_label=False):
            entity_data = _('None specified')
            entity_nodes = self.find_entities_by_type_id(entitytypeid)
            if len(entity_nodes) > 0:
                entity_data = []
                for node in entity_nodes:
                    if get_label:
                        ret = node.label
                    else:
                        ret = str(node.value)
                    if node.businesstablename == "dates":
                        return ret[:10]
                    entity_data.append(ret)
                entity_data = ', '.join(entity_data)
            return entity_data
        
        # NOT USED
        def get_entity_data2(eid, get_label=False):
            if get_label:
                entity_data = [i.label for i in self.child_entities if i.entitytypeid == eid]
            else:
                entity_data = [i.value for i in self.child_entities if i.entitytypeid == eid]
            ret = ', '.join(entity_data)
            return ret

        document_data = {}
        
        if self.entitytypeid == 'INVENTORY_RESOURCE.E18':

            document_data['resource_type'] = get_entity_data('NRHP_RESOURCE_TYPE.E55', get_label=True)
            document_data['address'] = _('None specified')
            address_nodes = self.find_entities_by_type_id('PLACE_ADDRESS.E45')
            for node in address_nodes:
                if node.find_entities_by_type_id('ADDRESS_TYPE.E55')[0].label == 'Primary':
                    document_data['address'] = node.value

        if self.entitytypeid == 'HERITAGE_RESOURCE_GROUP.E27':
            document_data['resource_type'] = get_entity_data('HERITAGE_RESOURCE_GROUP_TYPE.E55', get_label=True)

        if self.entitytypeid == 'ACTIVITY.E7':
            document_data['resource_type'] = get_entity_data('ACTIVITY_TYPE.E55', get_label=True)

        if self.entitytypeid == 'HISTORICAL_EVENT.E5':
            document_data['resource_type'] = get_entity_data('HISTORICAL_EVENT_TYPE.E55', get_label=True)

        if self.entitytypeid == 'ACTOR.E39':
            document_data['resource_type'] = get_entity_data('ACTOR_TYPE.E55', get_label=True)

        if self.entitytypeid == 'INFORMATION_RESOURCE.E73':
            document_data['resource_type'] = get_entity_data('INFORMATION_RESOURCE_TYPE.E55', get_label=True)
            document_data['creation_date'] = get_entity_data('DATE_OF_CREATION.E50')
            document_data['publication_date'] = get_entity_data('DATE_OF_PUBLICATION.E50')
            document_data['file_path'] = get_entity_data('FILE_PATH.E62', get_label=True)
            
        if self.entitytypeid == 'HISTORICAL_EVENT.E5' or self.entitytypeid == 'ACTIVITY.E7' or self.entitytypeid == 'ACTOR.E39':
            document_data['start_date'] = get_entity_data('BEGINNING_OF_EXISTENCE.E63')
            document_data['end_date'] = get_entity_data('END_OF_EXISTENCE.E64')

        for document in documents:
            for key in document_data:
                document['properties'][key] = document_data[key]

        return documents
        
    def prepare_documents_for_report_index(self, geom_entities=[]):
        """
        Generates a list of specialized resource based documents to support resource reports

        """

        geojson_geom = None
        if len(geom_entities) > 0:
            geojson_geom = {
                'type': 'GeometryCollection',
                'geometries': [geom_entity['value'] for geom_entity in geom_entities]
            }

        entity_dict = Entity()
        entity_dict.property = self.property
        entity_dict.entitytypeid = self.entitytypeid
        entity_dict.entityid = self.entityid
        entity_dict.primaryname = self.get_primary_name()
        entity_dict.geometry = geojson_geom
        
        entity_dict.graph = self.dictify(keys=['label', 'value'])
        return [JSONSerializer().serializeToPython(entity_dict)]

    def prepare_search_index(self, resource_type_id, create=False):
        """
        Creates the settings and mappings in Elasticsearch to support resource search
        """

        index_settings = super(Resource, self).prepare_search_index(resource_type_id, create=False)

        index_settings['mappings'][resource_type_id]['properties']['date_groups'] = { 
            'properties' : {
                'conceptid': {'type' : 'string', 'index' : 'not_analyzed'}
            }
        }

        if create:
            se = SearchEngineFactory().create()
            try:
                se.create_index(index='entity', body=index_settings)
            except:
                index_settings = index_settings['mappings']
                se.create_mapping(index='entity', doc_type=resource_type_id, body=index_settings)
        
    @staticmethod
    def get_report(resourceid):
        # get resource data for resource_id from ES, return data
        # with correct id for the given resource type
        return {
            'id': 'heritage-resource',
            'data': {
                'hello_world': 'Hello World!'
            }
        }
