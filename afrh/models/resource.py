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

class Resource(ArchesResource):
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        description_group = {
            'id': 'resource-description',
            'icon':'fa-folder',
            'name': _('Resource Description'),
            'forms': [
                other.RelatedResourcesForm.get_info(),
            ]   
        }

        self.form_groups.append(description_group)

        if self.entitytypeid == 'INVENTORY_RESOURCE.E18':
            description_group['forms'][:0] = [
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

        elif self.entitytypeid == 'CHARACTER_AREA.E53':
            description_group['forms'][:0] = [
                summary.CharAreaSummaryForm.get_info(),
                description.CharAreaDescriptionForm.get_info(),
                other.CharAreaGuidelinesForm.get_info(),
                location.SimpleLocationForm.get_info(),
            ]
            
        elif self.entitytypeid == 'MASTER_PLAN_ZONE.E53':
            description_group['forms'][:0] = [
                summary.MPZoneSummaryForm.get_info(),
                description.InventoryDescriptionForm.get_info(),
                location.SimpleLocationForm.get_info(),
                wizard.MPZoneGuidelinesForm.get_info(),
            ]
            
        elif self.entitytypeid == 'ARCHAEOLOGICAL_ZONE.E53':
            description_group['forms'][:0] = [
                summary.ArchZoneSummaryForm.get_info(),
                location.SimpleLocationForm.get_info(),
                location.ProbabilityAreaForm.get_info(),
            ]
            
        elif self.entitytypeid == 'HISTORIC_AREA.E53':
            description_group['forms'][:0] = [
                summary.DesSummaryForm.get_info(),
                location.SimpleLocationForm.get_info(),
                description.DesDescriptionForm.get_info(),
                other.DesEvaluationForm.get_info(),
            ]

        elif self.entitytypeid == 'ACTOR.E39':
            description_group['forms'][:0] = [
                summary.ActorSummaryForm.get_info(), 
                description.InventoryDescriptionForm.get_info(),
                location.LocationForm.get_info(),
                wizard.RelatedFilesForm.get_info(),
                #other.RoleForm.get_info(),
                other.ExternalReferenceForm.get_info()
            ]

        elif self.entitytypeid == 'INFORMATION_RESOURCE.E73':
            description_group['forms'][:0] = [
                summary.InformationResourceSummaryForm.get_info(), 
                other.PublicationForm.get_info(),
                location.LocationForm.get_info(),
                description.InventoryDescriptionForm.get_info(),
                wizard.FileUploadForm.get_info()
            ]
            
        elif self.entitytypeid == 'ACTIVITY_A.E7':
            description_group['forms'][:0] = [
                review.Section106ReviewForm.get_info(),
                review.NCPCReviewForm.get_info(),
                review.CFAReviewForm.get_info(),
                other.EntitiesForm.get_info(),
            ]

        elif self.entitytypeid == 'ACTIVITY_B.E7':
            description_group['forms'][:0] = [
                review.NCPCReviewForm.get_info(),
                review.CFAReviewForm.get_info(),
            ]

        if self.entityid != '':
            self.form_groups.append({
                'id': 'manage-resource',
                'icon': 'fa-wrench',
                'name': _('Manage Resource'),
                'forms': [
                    EditHistory.get_info(),
                    DeleteResourceForm.get_info()
                ]
            })

    def get_primary_name(self):
        displayname = super(Resource, self).get_primary_name()
        names = self.get_names()
        if len(names) > 0:
            displayname = names[0].value
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
            print entity_nodes
            if len(entity_nodes) > 0:
                entity_data = []
                for node in entity_nodes:
                    if get_label:
                        entity_data.append(node.label)
                    else:
                        entity_data.append(str(node.value))
                entity_data = ', '.join(entity_data)
            return entity_data

        document_data = {}
        
        if self.entitytypeid == 'INVENTORY_RESOURCE.E18':
            document_data['resource_type'] = get_entity_data('NHRP_RESOURCE_TYPE.E55', get_label=True)

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

        #if self.entitytypeid == 'INVENTORY_RESOURCE.E18' or self.entitytypeid == 'HERITAGE_RESOURCE_GROUP.E27':
        #    document_data['designations'] = get_entity_data('TYPE_OF_DESIGNATION_OR_PROTECTION.E55', get_label=True)

        for document in documents:
            for key in document_data:
                document['properties'][key] = document_data[key]

        return documents

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
