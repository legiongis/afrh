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


class InventorySummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'inventory-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': InventorySummaryForm
        }

    def update(self, data, files):
        self.update_nodes('NAME.E41', data)
        self.update_nodes('NRHP_RESOURCE_TYPE.E55', data)
        self.update_nodes('NRHP_RESOURCE_CATEGORY.E55', data)
        self.update_nodes('NRHP_RESOURCE_SUBCATEGORY.E55', data)
        self.update_nodes('WUZIT.E55', data)
        self.update_nodes('BUILDING_NUMBER.E42', data)

        beginning_of_existence_nodes = []
        end_of_existence_nodes = []
        for branch_list in data['important_dates']:
            for node in branch_list['nodes']:
                if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_TYPE.E55':
                    print "BEGINNING_OF_EXISTENCE_TYPE.E55 branchlist:"
                    print branch_list
                    beginning_of_existence_nodes.append(branch_list)
                if node['entitytypeid'] == 'END_OF_EXISTENCE_TYPE.E55':
                    print "END_OF_EXISTENCE_TYPE.E55 branchlist:"
                    print branch_list
                    end_of_existence_nodes.append(branch_list)

        for branch_list in beginning_of_existence_nodes:
            for node in branch_list['nodes']:        
                if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    node['entitytypeid'] = 'START_DATE_OF_EXISTENCE.E49'
                if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_NOTE.E62,END_OF_EXISTENCE_NOTE.E62':
                    node['entitytypeid'] = 'BEGINNING_OF_EXISTENCE_NOTE.E62'

        for branch_list in end_of_existence_nodes:
            for node in branch_list['nodes']:        
                if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    node['entitytypeid'] = 'END_DATE_OF_EXISTENCE.E49'
                if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_NOTE.E62,END_OF_EXISTENCE_NOTE.E62':
                    node['entitytypeid'] = 'END_OF_EXISTENCE_NOTE.E62'

        self.update_nodes('BEGINNING_OF_EXISTENCE.E63', {'BEGINNING_OF_EXISTENCE.E63':beginning_of_existence_nodes})
        self.update_nodes('END_OF_EXISTENCE.E64', {'END_OF_EXISTENCE.E64':end_of_existence_nodes})

    def load(self, lang):
        self.data['important_dates'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('BEGINNING_OF_EXISTENCE.E63') + self.get_nodes('END_OF_EXISTENCE.E64')),
            'domains': {
                'important_dates' : Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_TYPE.E55') + Concept().get_e55_domain('END_OF_EXISTENCE_TYPE.E55'),
                'date_qualifiers': Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_QUALIFIER.E55')
            }
        }

        if self.resource:
            
            self.data['NRHP_RESOURCE_TYPE.E55'] = {
                'branch_lists': self.get_nodes('NRHP_RESOURCE_TYPE.E55'),
                'domains': {'NRHP_RESOURCE_TYPE.E55' : Concept().get_e55_domain('NRHP_RESOURCE_TYPE.E55')}
                }
                
            self.data['NRHP_RESOURCE_CATEGORY.E55'] = {
                'branch_lists': self.get_nodes('NRHP_RESOURCE_CATEGORY.E55'),
                'domains': {'NRHP_RESOURCE_CATEGORY.E55' : Concept().get_e55_domain('NRHP_RESOURCE_CATEGORY.E55')}
                }
                
            self.data['NRHP_RESOURCE_SUBCATEGORY.E55'] = {
                'branch_lists': self.get_nodes('NRHP_RESOURCE_SUBCATEGORY.E55'),
                'domains': {'NRHP_RESOURCE_SUBCATEGORY.E55' : Concept().get_e55_domain('NRHP_RESOURCE_SUBCATEGORY.E55')}
                }
                
            self.data['WUZIT.E55'] = {
                'branch_lists': self.get_nodes('WUZIT.E55'),
                'domains': {'WUZIT.E55' : Concept().get_e55_domain('WUZIT.E55')}
                }

            self.data['NAME.E41'] = {
                'branch_lists': self.get_nodes('NAME.E41'),
                'domains': {'NAME_TYPE.E55' : Concept().get_e55_domain('NAME_TYPE.E55')}
                # 'defaults': {
                #     'NAME_TYPE.E55': default_name_type['id'],
                #     'NAME.E41': ''
                # }
                }
            
            self.data['BUILDING_NUMBER.E42'] = {
                'branch_lists': self.get_nodes('BUILDING_NUMBER.E42'),
                'domains': {'BUILDING_NUMBER_TYPE.E55' : Concept().get_e55_domain('BUILDING_NUMBER_TYPE.E55')}
                }

            try:
                self.data['primaryname_conceptid'] = self.data['NAME.E41']['domains']['NAME_TYPE.E55'][0]['id']
            except IndexError:
                pass
                
class CharAreaSummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'char-area-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': CharAreaSummaryForm
        }

    def update(self, data, files):
        self.update_nodes('NAME.E48', data)
        self.update_nodes('RELATIVE_LEVEL_OF_SIGNIFICANCE.E55', data)

    def load(self, lang):
        if self.resource:
            self.data['RELATIVE_LEVEL_OF_SIGNIFICANCE.E55'] = {
                'branch_lists': self.get_nodes('RELATIVE_LEVEL_OF_SIGNIFICANCE.E55'),
                'domains': {'RELATIVE_LEVEL_OF_SIGNIFICANCE.E55' : Concept().get_e55_domain('RELATIVE_LEVEL_OF_SIGNIFICANCE.E55')}
            }

            self.data['NAME.E48'] = {
                'branch_lists': self.get_nodes('NAME.E48'),
            }
            
class ArchZoneSummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'arch-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': ArchZoneSummaryForm
        }

    def update(self, data, files):
        self.update_nodes('ARCHAEOLOGICAL_ZONE_NAME.E48', data)
        self.update_nodes('DESCRIPTION.E62', data)

    def load(self, lang):
        if self.resource:
            self.data['ARCHAEOLOGICAL_ZONE_NAME.E48'] = {
                'branch_lists': self.get_nodes('ARCHAEOLOGICAL_ZONE_NAME.E48'),
            }

            self.data['DESCRIPTION.E62'] = {
                'branch_lists': self.get_nodes('DESCRIPTION.E62'),
            }
            
class DesSummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'des-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': DesSummaryForm
        }

    def update(self, data, files):
        self.update_nodes('HISTORIC_AREA_NAME.E48', data)
        self.update_nodes('HISTORIC_AREA_DESIGNATION.E55', data)
        self.update_nodes('HISTORIC_AREA_TYPE.E55', data)
        self.update_nodes('ADMINISTRATIVE_DATE.E49', data)

    def load(self, lang):
        if self.resource:
            self.data['HISTORIC_AREA_NAME.E48'] = {
                'branch_lists': self.get_nodes('HISTORIC_AREA_NAME.E48'),
            }

            self.data['HISTORIC_AREA_DESIGNATION.E55'] = {
                'branch_lists': self.get_nodes('HISTORIC_AREA_DESIGNATION.E55'),
                'domains':{
                    'HISTORIC_AREA_DESIGNATION.E55' : Concept().get_e55_domain('HISTORIC_AREA_DESIGNATION.E55')
                }
            }
            
            self.data['HISTORIC_AREA_TYPE.E55'] = {
                'branch_lists': self.get_nodes('HISTORIC_AREA_TYPE.E55'),
                'domains':{
                    'HISTORIC_AREA_TYPE.E55' : Concept().get_e55_domain('HISTORIC_AREA_TYPE.E55')
                }
            }
            
            self.data['ADMINISTRATIVE_DATE.E49'] = {
                'branch_lists': self.get_nodes('ADMINISTRATIVE_DATE.E49'),
                'domains':{
                    'ADMINISTRATIVE_DATE_TYPE.E55' : Concept().get_e55_domain('ADMINISTRATIVE_DATE_TYPE.E55')
                }
            }
            
## NOT CURRENTLY USED
class HeritageGroupSummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'heritage-group-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': HeritageGroupSummaryForm
        }

    def update(self, data, files):
        self.update_nodes('NAME.E41', data)
        self.update_nodes('KEYWORD.E55', data)
        self.update_nodes('HERITAGE_RESOURCE_GROUP_TYPE.E55', data)
        
        # production_entities = self.resource.find_entities_by_type_id('PRODUCTION.E12')
        
        # phase_type_node_id = ''
        # for value in data['PHASE_TYPE_ASSIGNMENT.E17']:
            # for node in value['nodes']:
                # if node['entitytypeid'] == 'PHASE_TYPE_ASSIGNMENT.E17' and node['entityid'] != '':
                    # remove the node
                    # phase_type_node_id = node['entityid']
                    # self.resource.filter(lambda entity: entity.entityid != node['entityid'])
                    
        # for entity in self.baseentity.find_entities_by_type_id('PHASE_TYPE_ASSIGNMENT.E17'):
            # entity.entityid = phase_type_node_id

        # if len(production_entities) > 0:
            # self.resource.merge_at(self.baseentity, 'PRODUCTION.E12')
        # else:
            # self.resource.merge_at(self.baseentity, self.resource.entitytypeid)

        # self.resource.trim()

        beginning_of_existence_nodes = []
        end_of_existence_nodes = []
        for branch_list in data['important_dates']:
            for node in branch_list['nodes']:
                if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_TYPE.E55':
                    beginning_of_existence_nodes.append(branch_list)
                if node['entitytypeid'] == 'END_OF_EXISTENCE_TYPE.E55':
                    end_of_existence_nodes.append(branch_list)

        for branch_list in beginning_of_existence_nodes:
            for node in branch_list['nodes']:        
                if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    node['entitytypeid'] = 'START_DATE_OF_EXISTENCE.E49'

        for branch_list in end_of_existence_nodes:
            for node in branch_list['nodes']:        
                if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    node['entitytypeid'] = 'END_DATE_OF_EXISTENCE.E49'

        self.update_nodes('BEGINNING_OF_EXISTENCE.E63', {'BEGINNING_OF_EXISTENCE.E63':beginning_of_existence_nodes})
        self.update_nodes('END_OF_EXISTENCE.E64', {'END_OF_EXISTENCE.E64':end_of_existence_nodes})

    def load(self, lang):

        # self.data['PHASE_TYPE_ASSIGNMENT.E17'] = {
            # 'branch_lists': self.get_nodes('PHASE_TYPE_ASSIGNMENT.E17'),
            # 'domains': {
                # 'HERITAGE_RESOURCE_GROUP_TYPE.E55': Concept().get_e55_domain('HERITAGE_RESOURCE_GROUP_TYPE.E55'),
                # 'HERITAGE_RESOURCE_GROUP_USE_TYPE.E55' : Concept().get_e55_domain('HERITAGE_RESOURCE_GROUP_USE_TYPE.E55')
            # }
        # }
    
        self.data['important_dates'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('BEGINNING_OF_EXISTENCE.E63') + self.get_nodes('END_OF_EXISTENCE.E64')),
            'domains': {'important_dates' : Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_TYPE.E55') + Concept().get_e55_domain('END_OF_EXISTENCE_TYPE.E55')}
        }
        
        

        if self.resource:
            # if self.resource.entitytypeid in ('HERITAGE_RESOURCE.E18', 'HERITAGE_RESOURCE_GROUP.E27'):            
                # self.data['RESOURCE_TYPE_CLASSIFICATION.E55'] = {
                    # 'branch_lists': self.get_nodes('RESOURCE_TYPE_CLASSIFICATION.E55'),
                    # 'domains': {'RESOURCE_TYPE_CLASSIFICATION.E55' : Concept().get_e55_domain('RESOURCE_TYPE_CLASSIFICATION.E55')}
                # }
                
            self.data['HERITAGE_RESOURCE_GROUP_TYPE.E55'] = {
                'branch_lists': self.get_nodes('HERITAGE_RESOURCE_GROUP_TYPE.E55'),
                'domains': {
                    'HERITAGE_RESOURCE_GROUP_TYPE.E55' : Concept().get_e55_domain('HERITAGE_RESOURCE_GROUP_TYPE.E55'),
                    'HERITAGE_RESOURCE_GROUP_USE_TYPE.E55': Concept().get_e55_domain('HERITAGE_RESOURCE_GROUP_USE_TYPE.E55')
                }
            }

            self.data['NAME.E41'] = {
                'branch_lists': self.get_nodes('NAME.E41'),
                'domains': {'NAME_TYPE.E55' : Concept().get_e55_domain('NAME_TYPE.E55')}
                # 'defaults': {
                #     'NAME_TYPE.E55': default_name_type['id'],
                #     'NAME.E41': ''
                # }
            }

            self.data['KEYWORD.E55'] = {
                'branch_lists': self.get_nodes('KEYWORD.E55'),
                'domains': {'KEYWORD.E55' : Concept().get_e55_domain('KEYWORD.E55')}
            }

            try:
                self.data['primaryname_conceptid'] = self.data['NAME.E41']['domains']['NAME_TYPE.E55'][3]['id']
            except IndexError:
                pass

## NOT CURRENTLY USED
class ActivitySummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'activity-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': ActivitySummaryForm
        }

    def update(self, data, files):
        self.update_nodes('NAME.E41', data)
        self.update_nodes('PHASE_TYPE_ASSIGNMENT.E17', data)

    def load(self, lang):
        if self.resource:

            self.data['NAME.E41'] = {
                'branch_lists': self.get_nodes('NAME.E41'),
                'domains': {'ACTIVITY_NAME_TYPE.E55' : Concept().get_e55_domain('ACTIVITY_NAME_TYPE.E55')}
            }

            phase_type_nodes = datetime_nodes_to_dates(self.get_nodes('PHASE_TYPE_ASSIGNMENT.E17'))

            self.data['PHASE_TYPE_ASSIGNMENT.E17'] = {
                'branch_lists': phase_type_nodes,
                'domains': {
                    'ACTIVITY_TYPE.E55': Concept().get_e55_domain('ACTIVITY_TYPE.E55'),
                }
            }
            
            try:
                self.data['primaryname_conceptid'] = self.data['NAME.E41']['domains']['ACTIVITY_NAME_TYPE.E55'][3]['id']
            except IndexError:
                pass

class InformationResourceSummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'information-resource-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': InformationResourceSummaryForm
        }   

    def update(self, data, files):
        print data
        self.update_nodes('TITLE.E41', data)
        self.update_nodes('INFORMATION_RESOURCE_TYPE_ASSIGNMENT.E17', data)
        self.update_nodes('EXTERNAL_RESOURCE.E1', data)
        self.update_nodes('KEYWORD.E55', data)
        self.update_nodes('LANGUAGE.E55', data)

    def load(self, lang):
        if self.resource:

            self.data['TITLE.E41'] = {
                'branch_lists': self.get_nodes('TITLE.E41'),
                'domains': {'TITLE_TYPE.E55' : Concept().get_e55_domain('TITLE_TYPE.E55')}
            }
            
            self.data['INFORMATION_RESOURCE_TYPE_ASSIGNMENT.E17'] = {
                'branch_lists': self.get_nodes('INFORMATION_RESOURCE_TYPE_ASSIGNMENT.E17'),
                'domains': {
                    'INFORMATION_RESOURCE_TYPE.E55' : Concept().get_e55_domain('INFORMATION_RESOURCE_TYPE.E55')
                }
            }

            self.data['EXTERNAL_RESOURCE.E1'] = {
                'branch_lists': self.get_nodes('EXTERNAL_RESOURCE.E1'),
                'domains': {
                    'EXTERNAL_XREF_TYPE.E55' : Concept().get_e55_domain('EXTERNAL_XREF_TYPE.E55')
                }
            }

            self.data['LANGUAGE.E55'] = {
                'branch_lists': self.get_nodes('LANGUAGE.E55'),
                'domains': {'LANGUAGE.E55' : Concept().get_e55_domain('LANGUAGE.E55')}
            }

            self.data['KEYWORD.E55'] = {
                'branch_lists': self.get_nodes('KEYWORD.E55'),
                'domains': {'KEYWORD.E55' : Concept().get_e55_domain('KEYWORD.E55')}
            }

            # self.data['primaryname_conceptid'] = self.data['TITLE.E41']['domains']['TITLE_TYPE.E55'][3]['id']
 
class MPZoneSummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'mpz-summary',
            'icon': 'fa-picture-o',
            'name': _('Summary'),
            'class': MPZoneSummaryForm
        }

    def update(self, data, files):
        self.update_nodes('MASTER_PLAN_ZONE_ACTIVITY.E7', data)
        self.update_nodes('PLANNED_USE.E55', data)
        self.update_nodes('ZONE_TYPE.E55', data)
        self.update_nodes('NAME.E48', data)

    def load(self, lang):
        
        if self.resource:
        
            self.data['MASTER_PLAN_ZONE_ACTIVITY.E7'] = {
                'branch_lists': self.get_nodes('MASTER_PLAN_ZONE_ACTIVITY.E7'),
                'domains': {
                    'MASTER_PLAN_ZONE_ACTIVITY_TYPE.E55' : Concept().get_e55_domain('MASTER_PLAN_ZONE_ACTIVITY_TYPE.E55'),
                }
            }
        
            self.data['PLANNED_USE.E55'] = {
                'branch_lists': self.get_nodes('PLANNED_USE.E55'),
                'domains': {
                    'PLANNED_USE.E55' : Concept().get_e55_domain('PLANNED_USE.E55'),
                }
            }
            
            self.data['ZONE_TYPE.E55'] = {
                'branch_lists': self.get_nodes('ZONE_TYPE.E55'),
                'domains': {
                    'ZONE_TYPE.E55' : Concept().get_e55_domain('ZONE_TYPE.E55'),
                }
            }
            
            self.data['NAME.E48'] = {
                'branch_lists': self.get_nodes('NAME.E48'),
            }

class ActorSummaryForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'actor-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': ActorSummaryForm
        }

    def update(self, data, files):
        self.update_nodes('APPELLATION.E41', data)
        self.update_nodes('EPITHET.E82', data)
        self.update_nodes('BEGINNING_OF_EXISTENCE.E63', data)
        self.update_nodes('END_OF_EXISTENCE.E64', data)

    def load(self, lang):
        if self.resource:
            self.data['APPELLATION.E41'] = {
                'branch_lists': self.get_nodes('APPELLATION.E41'),
                'domains': {
                    'ACTOR_NAME_TYPE.E55' : Concept().get_e55_domain('ACTOR_NAME_TYPE.E55')
                }
            }

            self.data['EPITHET.E82'] = {
                'branch_lists': self.get_nodes('EPITHET.E82'),
            }

            self.data['BEGINNING_OF_EXISTENCE.E63'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('BEGINNING_OF_EXISTENCE.E63')),
                'domains': {
                    'BEGINNING_OF_EXISTENCE_TYPE.E55' : Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_TYPE.E55')
                }
            }

            self.data['END_OF_EXISTENCE.E64'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('END_OF_EXISTENCE.E64')),
                'domains': {
                    'END_OF_EXISTENCE_TYPE.E55' : Concept().get_e55_domain('END_OF_EXISTENCE_TYPE.E55')
                }
            }
            
class ActivityForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'activity-summary',
            'icon': 'fa-tag',
            'name': _('Summary'),
            'class': ActivityForm
        }

    def update(self, data, files):
    
        act_a_nodes = [
            'WORK_ORDER_ASSIGNMENT.E13',
            'ACTIVITY_PROCEDURE_TYPE.E55',
            'ACTIVITY_PROCEDURE_NOTE.E62',
            'ACTION_AGENT_REQUEST_DATE.E49',
            'ACTION_STATUS_ASSIGNMENT.E13',
        ]
        
        act_b_nodes = [
            'BUILDING_PERMIT_NUMBER.E42',
        ]
        
        both_nodes = [
            'ACTIVITY_NAME.E41',
            'ACTION_AGENT.E39',
            'ACTIVITY_REVIEW_TYPE.E55',
            'ACTIVITY_REVIEW_NOTE.E62',
            'ACTIVITY_MILESTONE_ACHIEVEMENT.E5',
        ]
        
        if self.resource.entitytypeid == 'ACTIVITY_A.E7':   
            update_nodes = act_a_nodes + both_nodes
            print update_nodes
        if self.resource.entitytypeid == 'ACTIVITY_B.E7':   
            update_nodes = act_b_nodes + both_nodes
            
        for node in update_nodes:
            print node
            self.update_nodes(node, data)
            
        
        return

    def load(self, lang):

        load_nodes = {
            'ACTIVITY_NAME.E41':[],
            'ACTION_AGENT.E39':[
                'ACTION_AGENT_TYPE.E55',
            ],
            'ACTIVITY_REVIEW_TYPE.E55':[
                'ACTIVITY_REVIEW_TYPE.E55',
            ],
            'ACTIVITY_REVIEW_NOTE.E62':[],
            'ACTIVITY_MILESTONE_ACHIEVEMENT.E5':[]
        }
        
        for node, domains in load_nodes.iteritems():
            self.data[node] = {
                'branch_lists': self.get_nodes(node),
                'domains': dict([(d,Concept().get_e55_domain(d)) for d in domains])
            }
            
        if self.resource.entitytypeid == 'ACTIVITY_A.E7':
            self.data['WORK_ORDER_ASSIGNMENT.E13'] = {
                'branch_lists': self.get_nodes('WORK_ORDER_ASSIGNMENT.E13')
            }
            self.data['ACTION_AGENT_REQUEST_DATE.E49'] = {
                'branch_lists': self.get_nodes('ACTION_AGENT_REQUEST_DATE.E49')
            }
            self.data['ACTIVITY_PROCEDURE_TYPE.E55'] = {
                'branch_lists': self.get_nodes('ACTIVITY_PROCEDURE_TYPE.E55'),
                'domains': {
                    'ACTIVITY_PROCEDURE_TYPE.E55' : Concept().get_e55_domain('ACTIVITY_PROCEDURE_TYPE.E55')
                }
            }
            self.data['ACTIVITY_PROCEDURE_NOTE.E62'] = {
                'branch_lists': self.get_nodes('ACTIVITY_PROCEDURE_NOTE.E62')
            }
            self.data['ACTION_STATUS_ASSIGNMENT.E13'] = {
                'branch_lists': self.get_nodes('ACTION_STATUS_ASSIGNMENT.E13'),
                'domains': {
                    'CURRENT_ACTION_STATUS.E55' : Concept().get_e55_domain('CURRENT_ACTION_STATUS.E55')
                }
            }
            self.data['ACTIVITY_MILESTONE_ACHIEVEMENT.E5']['domains'] = {
                    'ACTIVITY_A_MILESTONE.E55' : Concept().get_e55_domain('ACTIVITY_A_MILESTONE.E55')
                }
                
            
        if self.resource.entitytypeid == 'ACTIVITY_B.E7':
            self.data['BUILDING_PERMIT_NUMBER.E42'] = {
                'branch_lists': self.get_nodes('BUILDING_PERMIT_NUMBER.E42')
            }
            self.data['ACTIVITY_MILESTONE_ACHIEVEMENT.E5']['domains'] = {
                'ACTIVITY_B_MILESTONE.E55' : Concept().get_e55_domain('ACTIVITY_B_MILESTONE.E55')
            }