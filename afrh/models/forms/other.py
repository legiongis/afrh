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

from arches.app.models.models import RelatedResource
from arches.app.models.entity import Entity
from arches.app.models.resource import Resource
from arches.app.models.concept import Concept
from arches.app.models.forms import ResourceForm
from arches.app.utils.imageutils import generate_thumbnail
from arches.app.views.concept import get_preflabel_from_valueid
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.search.search_engine_factory import SearchEngineFactory
from django.forms.models import model_to_dict
from django.utils.translation import ugettext as _
from django.forms.models import model_to_dict
from datetime import datetime
from django.conf import settings
import json, os

def datetime_nodes_to_dates(branch_list):
    for branch in branch_list:
        for node in branch['nodes']:
            if isinstance(node.value, datetime):
                node.value = node.value.date()
                node.label = node.value
    return branch_list

class ExternalReferenceForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'external-reference',
            'icon': 'fa-random',
            'name': _('External System References'),
            'class': ExternalReferenceForm
        }

    def update(self, data, files):
        self.update_nodes('EXTERNAL_RESOURCE.E1', data)
        return

    def load(self, lang):

        self.data['EXTERNAL_RESOURCE.E1'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('EXTERNAL_RESOURCE.E1')),
            'domains': {
                'EXTERNAL_XREF_TYPE.E55': Concept().get_e55_domain('EXTERNAL_XREF_TYPE.E55'),
            }
        }

class DesEvaluationForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'des-evaluation',
            'icon': 'fa-tag',
            'name': _('Evaluation'),
            'class': DesEvaluationForm
        }

    def update(self, data, files):
        self.update_nodes('HISTORIC_AREA_STATUS.E55', data)
        self.update_nodes('PERIOD_OF_SIGNIFICANCE.E4', data)
        self.update_nodes('NRHP_CRITERIA.E17', data)
        self.update_nodes('CRITERION_CONSIDERATIONS.E55', data)
        self.update_nodes('AREA_OF_SIGNIFICANCE.E55', data)
        return

    def load(self, lang):

        self.data['HISTORIC_AREA_STATUS.E55'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('HISTORIC_AREA_STATUS.E55')),
            'domains': {
                'HISTORIC_AREA_STATUS.E55': Concept().get_e55_domain('HISTORIC_AREA_STATUS.E55'),
            }
        }
        
        self.data['PERIOD_OF_SIGNIFICANCE.E4'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('PERIOD_OF_SIGNIFICANCE.E4')),
        }
        
        self.data['NRHP_CRITERIA.E17'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('NRHP_CRITERIA.E17')),
        }
        
        self.data['CRITERION_CONSIDERATIONS.E55'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('CRITERION_CONSIDERATIONS.E55')),
            'domains': {
                'CRITERION_CONSIDERATIONS.E55': Concept().get_e55_domain('CRITERION_CONSIDERATIONS.E55'),
            }
        }
        
        self.data['AREA_OF_SIGNIFICANCE.E55'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('AREA_OF_SIGNIFICANCE.E55')),
            'domains': {
                'AREA_OF_SIGNIFICANCE.E55': Concept().get_e55_domain('AREA_OF_SIGNIFICANCE.E55'),
            }
        }
        
class InvestRecForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'invest-recommendations',
            'icon': 'fa-calendar-check-o',
            'name': _('Recommendations'),
            'class': InvestRecForm
        }

    def update(self, data, files):
        self.update_nodes('INVESTIGATION_RECOMMENDATIONS.E62', data)
        return

    def load(self, lang):

        self.data['INVESTIGATION_RECOMMENDATIONS.E62'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('INVESTIGATION_RECOMMENDATIONS.E62')),
        }
        
class InvestAssessmentForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'invest-assessment',
            'icon': 'fa-tags',
            'name': _('Assessments'),
            'class': InvestAssessmentForm
        }

    def update(self, data, files):
        self.update_nodes('NATIVE_AMERICAN_SITE_POTENTIAL_ASSESSMENT.E14', data)
        self.update_nodes('PREHISTORIC_SITE_POTENTIAL_ASSESSMENT.E14', data)
        self.update_nodes('HISTORIC_SITE_POTENTIAL_ASSESSMENT.E14', data)
        return

    def load(self, lang):

        self.data['PREHISTORIC_SITE_POTENTIAL_ASSESSMENT.E14'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('PREHISTORIC_SITE_POTENTIAL_ASSESSMENT.E14')),
        }
        
        self.data['NATIVE_AMERICAN_SITE_POTENTIAL_ASSESSMENT.E14'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('NATIVE_AMERICAN_SITE_POTENTIAL_ASSESSMENT.E14')),
        }
        
        self.data['HISTORIC_SITE_POTENTIAL_ASSESSMENT.E14'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('HISTORIC_SITE_POTENTIAL_ASSESSMENT.E14')),
        }

class CharAreaGuidelinesForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'char-area-guidelines',
            'icon': 'fa-legal',
            'name': _('Guidelines'),
            'class': CharAreaGuidelinesForm
        }

    def update(self, data, files):
        self.update_nodes('GUIDELINES.E62', data)
        return

    def load(self, lang):
        #if self.resource:
        self.data['GUIDELINES.E62'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('GUIDELINES.E62')),
        }

class ComponentForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'component',
            'icon': 'fa fa-sitemap',
            'name': _('Components'),
            'class': ComponentForm
        }
   
    def update(self, data, files):
        self.update_nodes('COMPONENT.E18', data)
        self.update_nodes('MODIFICATION_EVENT.E11', data)
        return

    def update_nodes(self, entitytypeid, data):

        self.resource.prune(entitytypes=[entitytypeid])

        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)
        for value in data[entitytypeid]:
            baseentity = None
            for newentity in value['nodes']:
                entity = Entity()
                if newentity['entitytypeid'] in self.schema:
                    entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                    if baseentity == None:
                        baseentity = entity
                    else:
                        baseentity.merge(entity)
            
            if entitytypeid == 'COMPONENT.E18':
                production_entities = self.resource.find_entities_by_type_id('PRODUCTION.E12')

                if len(production_entities) > 0:
                    self.resource.merge_at(baseentity, 'PRODUCTION.E12')
                else:
                    self.resource.merge_at(baseentity, self.resource.entitytypeid)

            else:
                self.resource.merge_at(baseentity, self.resource.entitytypeid)

        self.resource.trim()

    def load(self, lang):
        if self.resource:
        
            self.data['MODIFICATION_EVENT.E11'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('MODIFICATION_EVENT.E11')),
                'domains': {
                    'MODIFICATION_TYPE.E55' : Concept().get_e55_domain('MODIFICATION_TYPE.E55'),
                }
            }

            self.data['COMPONENT.E18'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('COMPONENT.E18')),
                'domains': {
                    'CONSTRUCTION_TECHNIQUE.E55': Concept().get_e55_domain('CONSTRUCTION_TECHNIQUE.E55'),
                    'MATERIAL.E57' : Concept().get_e55_domain('MATERIAL.E57'),
                    'COMPONENT_TYPE.E55' : Concept().get_e55_domain('COMPONENT_TYPE.E55'),
                    'COMPONENT_CLASSIFICATION.E55' : Concept().get_e55_domain('COMPONENT_CLASSIFICATION.E55'),
                    'COMPONENT_SIGNIFICANCE.E55' : Concept().get_e55_domain('COMPONENT_SIGNIFICANCE.E55'),
                }
            }

class InventoryEvaluationForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'inventory-evaluation',
            'icon': 'fa-tag',
            'name': _('Evaluation'),
            'class': InventoryEvaluationForm
        }
        
    def update(self, data, files):
        self.update_nodes('AFRH_W_HISTORIC_DISTRICT_STATE.E3', data)
        self.update_nodes('PERIOD_OF_SIGNIFICANCE.E55', data)
        self.update_nodes('AREA_OF_SIGNIFICANCE.E55', data)
        self.update_nodes('OTHER_AFRH_W_DESIGNATION.E3', data)
        self.update_nodes('OTHER_DESIGNATION.E3', data)
        self.update_nodes('COMPOSITE_SCORE.E60', data)
        self.update_nodes('HPMP_STATUS.E55',data)
        self.update_nodes('RELATIVE_LEVEL_OF_SIGNIFICANCE.E55',data)

    def load(self, lang):
        if self.resource:

            self.data['AFRH_W_HISTORIC_DISTRICT_STATE.E3'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('AFRH_W_HISTORIC_DISTRICT_STATE.E3')),
                'domains': {
                    'AFRH_W_HISTORIC_DISTRICT_STATUS.E55' : Concept().get_e55_domain('AFRH_W_HISTORIC_DISTRICT_STATUS.E55'),
                }
            }
            
            self.data['PERIOD_OF_SIGNIFICANCE.E55'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('PERIOD_OF_SIGNIFICANCE.E55')),
                'domains': {
                    'PERIOD_OF_SIGNIFICANCE.E55' : Concept().get_e55_domain('PERIOD_OF_SIGNIFICANCE.E55'),
                }
            }
            
            self.data['AREA_OF_SIGNIFICANCE.E55'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('AREA_OF_SIGNIFICANCE.E55')),
                'domains': {
                    'AREA_OF_SIGNIFICANCE.E55' : Concept().get_e55_domain('AREA_OF_SIGNIFICANCE.E55'),
                }
            }
            
            self.data['COMPOSITE_SCORE.E60'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('COMPOSITE_SCORE.E60')),
            }
            
            self.data['RELATIVE_LEVEL_OF_SIGNIFICANCE.E55'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('RELATIVE_LEVEL_OF_SIGNIFICANCE.E55')),
                'domains': {
                    'RELATIVE_LEVEL_OF_SIGNIFICANCE.E55' : Concept().get_e55_domain('RELATIVE_LEVEL_OF_SIGNIFICANCE.E55')
                }
            }
            
            self.data['OTHER_AFRH_W_DESIGNATION.E3'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('OTHER_AFRH_W_DESIGNATION.E3')),
                'domains': {
                    'OTHER_AFRH_W_DESIGNATION_TYPE.E55' : Concept().get_e55_domain('OTHER_AFRH_W_DESIGNATION_TYPE.E55'),
                    'OTHER_AFRH_W_DESIGNATION_STATUS.E55' : Concept().get_e55_domain('OTHER_AFRH_W_DESIGNATION_STATUS.E55'),
                }
            }

            self.data['OTHER_DESIGNATION.E3'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('OTHER_DESIGNATION.E3')),
                'domains': {
                    'OTHER_DESIGNATION_TYPE.E55' : Concept().get_e55_domain('OTHER_DESIGNATION_TYPE.E55'),
                    'OTHER_DESIGNATION_STATUS.E55' : Concept().get_e55_domain('OTHER_DESIGNATION_STATUS.E55'),
                }
            }
            
            self.data['HPMP_STATUS.E55'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('HPMP_STATUS.E55')),
                'domains': {
                    'HPMP_STATUS.E55' : Concept().get_e55_domain('HPMP_STATUS.E55'),
                }
            }

class FunctionAndUseForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'function-and-use',
            'icon': 'fa-magic',
            'name': _('Function and Use'),
            'class': FunctionAndUseForm
        }
        
    def update(self, data, files):
        self.update_nodes('PHASE_TYPE_ASSIGNMENT.E17', data)
        self.update_nodes('HERITAGE_ASSET_REPORT.E3', data)

    def load(self, lang):
        if self.resource:

            self.data['PHASE_TYPE_ASSIGNMENT.E17'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('PHASE_TYPE_ASSIGNMENT.E17')),
                'domains': {
                    'FUNCTION_PERIOD.E55' : Concept().get_e55_domain('FUNCTION_PERIOD.E55'),
                }
            }

            self.data['HERITAGE_ASSET_REPORT.E3'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('HERITAGE_ASSET_REPORT.E3')),
                'domains': {
                    'CURRENT_USER.E39' : Concept().get_e55_domain('CURRENT_USER.E39'),
                    'CURRENT_OPERATIONAL_STATUS.E55' : Concept().get_e55_domain('CURRENT_OPERATIONAL_STATUS.E55'),
                    'HERITAGE_ASSET_CONDITION.E3' : Concept().get_e55_domain('HERITAGE_ASSET_CONDITION.E3'),
                    'HERITAGE_ASSET_CLASSIFICATION.E55': Concept().get_e55_domain('HERITAGE_ASSET_CLASSIFICATION.E55'),
                    'HERITAGE_ASSET_PURPOSE.E55' : Concept().get_e55_domain('HERITAGE_ASSET_PURPOSE.E55'),
                }
            }

class FormDimensionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'form-dimension',
            'icon': 'fa-codepen',
            'name': _('Form and Dimensions'),
            'class': FormDimensionForm
        }

    def update(self, data, files):
        self.update_nodes('MEASUREMENT_TYPE.E55', data)
        self.update_nodes('FORM_TYPE.E55', data)


    def load(self, lang):
        if self.resource:
            self.data['MEASUREMENT_TYPE.E55'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('MEASUREMENT_TYPE.E55')),
                'domains': {
                    'MEASUREMENT_TYPE.E55' : Concept().get_e55_domain('MEASUREMENT_TYPE.E55'),
                    'UNIT_OF_MEASUREMENT.E55': Concept().get_e55_domain('UNIT_OF_MEASUREMENT.E55')
                }
            }
            self.data['FORM_TYPE.E55'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('FORM_TYPE.E55')),
                'domains': {
                    'FORM_TYPE.E55' : Concept().get_e55_domain('FORM_TYPE.E55'),
                }
            }

class EntitiesForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'entities',
            'icon': 'fa-users',
            'name': _('Entities'),
            'class': EntitiesForm
        }

    def update(self, data, files):
        update_nodes = [
            'ACTIVITY_ARCHITECT.E39',
            'ACTIVITY_CONTRACTOR.E39',
            'ACTIVITY_ENGINEER.E39',
            'ACTIVITY_ARCHAEOLOGIST.E39',
            'ACTIVITY_CONSULTANT.E39',
            'ACTIVITY_CONSULTING_PARTY.E39',
            'ACTIVITY_NCPC_CONTACT.E39',
            'ACTIVITY_CFA_CONTACT.E39',
            'ACTIVITY_DCSHPO_CONTACT.E39',
            'ACTIVITY_ENTITIES_NOTE.E62',
        ]
        if self.resource.entitytypeid == 'ACTIVITY_A.E7':
            update_nodes.append('AFRH_PROJECT_CONTACT.E39')
        
        for node in update_nodes:
            self.update_nodes(node, data)
            
        return


    def load(self, lang):
    
        load_nodes = {
            'ACTIVITY_ARCHITECT.E39':[],
            'ACTIVITY_CONTRACTOR.E39':[],
            'ACTIVITY_ENGINEER.E39':[],
            'ACTIVITY_ARCHAEOLOGIST.E39':[],
            'ACTIVITY_CONSULTANT.E39':[],
            'ACTIVITY_CONSULTING_PARTY.E39':[],
            'ACTIVITY_NCPC_CONTACT.E39':[],
            'ACTIVITY_CFA_CONTACT.E39':[],
            'ACTIVITY_DCSHPO_CONTACT.E39':[],
            'ACTIVITY_ENTITIES_NOTE.E62':[],
        }
        if self.resource.entitytypeid == 'ACTIVITY_A.E7':
            load_nodes['AFRH_PROJECT_CONTACT.E39'] = []

        for node, domains in load_nodes.iteritems():
            self.data[node] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes(node)),
                'domains': dict([(d,Concept().get_e55_domain(d)) for d in domains])
            }

        # self.data['AFRH_PROJECT_CONTACT.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('AFRH_PROJECT_CONTACT.E39'),
        # }
        # self.data['ACTIVITY_ARCHITECT.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_ARCHITECT.E39'),
        # }
        # self.data['ACTIVITY_CONTRACTOR.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_CONTRACTOR.E39'),
        # }
        # self.data['ACTIVITY_ENGINEER.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_ENGINEER.E39'),
        # }
        # self.data['ACTIVITY_ARCHAEOLOGIST.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_ARCHAEOLOGIST.E39'),
        # }
        # self.data['ACTIVITY_CONSULTANT.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_CONSULTANT.E39'),
        # }
        # self.data['ACTIVITY_CONSULTING_PARTY.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_CONSULTING_PARTY.E39'),
        # }
        # self.data['ACTIVITY_NCPC_CONTACT.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_NCPC_CONTACT.E39'),
        # }
        # self.data['ACTIVITY_CFA_CONTACT.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_CFA_CONTACT.E39'),
        # }
        # self.data['ACTIVITY_DCSHPO_CONTACT.E39'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_DCSHPO_CONTACT.E39'),
        # }
        # self.data['ACTIVITY_ENTITIES_NOTE.E62'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('ACTIVITY_ENTITIES_NOTE.E62'),
        # }


        return

class PublicationForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'publication',
            'icon': 'fa-pencil',
            'name': _('Creation and Publication'),
            'class': PublicationForm
        }

    def update(self, data, files):
        self.update_nodes('CREATOR.E39', data)
        self.update_nodes('TIME-SPAN_RESOURCE_CREATION_EVENT.E52', data)
        self.update_nodes('PUBLICATION_EVENT.E12', data)
        self.update_nodes('RIGHT_TYPE.E55', data)
        return
 
    def load(self, lang):
        if self.resource:
            self.data['TIME-SPAN_RESOURCE_CREATION_EVENT.E52'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('TIME-SPAN_RESOURCE_CREATION_EVENT.E52')),
                'domains': {
                    'CREATION_FORMAT.E55' : Concept().get_e55_domain('CREATION_FORMAT.E55')
                }
            }
            
            self.data['CREATOR.E39'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('CREATOR.E39')),
                'domains': {
                    'CREATOR_TYPE.E55' : Concept().get_e55_domain('CREATOR_TYPE.E55')
                }
            }

            self.data['PUBLICATION_EVENT.E12'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('PUBLICATION_EVENT.E12')),
                'domains': {}
            }

            self.data['RIGHT_TYPE.E55'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('RIGHT_TYPE.E55')),
                'domains': {
                    'RIGHT_TYPE.E55' : Concept().get_e55_domain('RIGHT_TYPE.E55')
                }
            }
        return
        
class RelatedResourcesForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'related-resources',
            'icon': 'fa-exchange',
            'name': _('Related Resources'),
            'class': RelatedResourcesForm
        }

    def update(self, data, files):
        se = SearchEngineFactory().create()
        related_resources_data = data.get('related-resources', [])
        original_relations = self.resource.get_related_resources()
        if self.resource.entityid == '':
            self.resource.save()
        relationship_ids = []

        for related_resource in related_resources_data:
            relationship_id = related_resource['relationship']['resourcexid']
            relationship_ids.append(relationship_id)
            resource_id = related_resource['relatedresourceid']
            relationship_type_id = related_resource['relationship']['relationshiptype']
            if isinstance(relationship_type_id, dict):
                relationship_type_id = relationship_type_id['value']
            notes = related_resource['relationship']['notes']
            date_started = related_resource['relationship']['datestarted']
            date_ended = related_resource['relationship']['dateended']
            if not relationship_id:
                relationship = self.resource.create_resource_relationship(resource_id,
                    relationship_type_id=relationship_type_id,
                    notes=notes,
                    date_started=date_started,
                    date_ended=date_ended
                    )
                    
            else:
                relationship = RelatedResource.objects.get(pk=relationship_id)
                relationship.relationshiptype = relationship_type_id
                relationship.notes = notes
                relationship.datestarted = date_started
                relationship.dateended = date_ended
                relationship.save()
                se.delete(index='resource_relations', doc_type='all', id=relationship_id)
            se.index_data(index='resource_relations', doc_type='all', body=model_to_dict(relationship), idfield='resourcexid')

        for relatedentity in original_relations:
            if relatedentity['relationship'].resourcexid not in relationship_ids:
                se.delete(index='resource_relations', doc_type='all', id=relatedentity['relationship'].resourcexid)
                relatedentity['relationship'].delete()

    def load(self, lang):
        data = []
        for relatedentity in self.resource.get_related_resources():
            nodes = relatedentity['related_entity'].flatten()

            data.append({
                'nodes': nodes, 
                'relationship': relatedentity['relationship'], 
                'relationshiptypelabel': get_preflabel_from_valueid(relatedentity['relationship'].relationshiptype, lang)['value'],
                'relatedresourcename':relatedentity['related_entity'].get_primary_name(),
                'relatedresourcetype':relatedentity['related_entity'].entitytypeid,
                'relatedresourceid':relatedentity['related_entity'].entityid,
                'related': True,
            })

        relationship_types = Concept().get_e55_domain('ARCHES_RESOURCE_CROSS-REFERENCE_RELATIONSHIP_TYPES.E55')

        try:
            default_relationship_type = relationship_types[0]['id']

            self.data['related-resources'] = {
                'branch_lists': data,
                'domains': {
                    'RELATIONSHIP_TYPES.E32': relationship_types
                },
                'default_relationship_type':  default_relationship_type
            }
            self.data['resource-id'] = self.resource.entityid
        except IndexError:
            pass
            
class InvestImageForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'invest-image',
            'icon': 'fa-image',
            'name': _('Photographs'),
            'class': InvestImageForm
        }

    # def get_nodesOLD(self, entity, entitytypeid):
        # ret = []
        # entities = entity.find_entities_by_type_id(entitytypeid)
        # for entity in entities:
            # ret.append({'nodes': entity.flatten()})
        # return ret

    # def update_nodesOLD(self, entitytypeid, data):
        # if self.schema == None:
            # self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)

        # for value in data[entitytypeid]:
            # if entitytypeid == 'GUIDELINE_IMAGE.E73':
                # temp = None
                # for newentity in value['nodes']:
                    # if newentity['entitytypeid'] != 'GUIDELINE_IMAGE.E73':
                        # entity = Entity()
                        # entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                        # if temp == None:
                            # temp = entity
                        # else:
                            # temp.merge(entity)

                # self.baseentity.merge_at(temp, 'GUIDELINE.E89')
            # else:
                # for newentity in value['nodes']:
                    # entity = Entity()
                    # entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                    # if self.baseentity == None:
                        # self.baseentity = entity
                    # else:
                        # self.baseentity.merge(entity)

    def update(self, data, files):
        if len(files) > 0:
            for f in files:
                data['INVESTIGATION_IMAGE.E73'].append({
                    'nodes':[{
                        'entitytypeid': 'INVESTIGATION_IMAGE_FILE_PATH.E62',
                        'entityid': '',
                        'value': files[f]
                    },{
                        'entitytypeid': 'INVESTIGATION_IMAGE_THUMBNAIL.E62',
                        'entityid': '',
                        'value': generate_thumbnail(files[f])
                    }]
                })

                self.update_nodes('INVESTIGATION_IMAGE.E73', data)
        # self.resource.merge_at(self.baseentity, self.resource.entitytypeid)
        # self.resource.trim()
                   
    def load(self, lang):
    
        self.data['INVESTIGATION_IMAGE.E73'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('INVESTIGATION_IMAGE.E73')),
        }