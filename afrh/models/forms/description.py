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

class CharAreaDescriptionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'char-area-description',
            'icon': 'fa-flash',
            'name': _('Description'),
            'class': CharAreaDescriptionForm
        }

    def update(self, data, files):
        self.update_nodes('DESCRIPTION.E62', data)
        return

    def load(self, lang):
        #if self.resource:
        self.data['DESCRIPTION.E62'] = {
            'branch_lists': self.get_nodes('DESCRIPTION.E62'),
        }
        
class ActADescriptionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'activity-a-description',
            'icon': 'fa-flash',
            'name': _('Description'),
            'class': ActADescriptionForm
        }

    def update(self, data, files):
        
        update_nodes = [
            'ACTIVITY_SCOPE_OF_WORK_TYPE.E55',
            'ACTIVITY_CONDITION.E3'
            'BUILDING_STRUCTURES_RECOMMENDATION_TYPE.E55',
            'OBJECT_RECOMMENDATION_TYPE.E55',
            'LANDSCAPE_RECOMMENDATION_TYPE.E55',
        ]
    
        for node in update_nodes:
            self.update_nodes(node, data)
            
        return

    def load(self, lang):
        
        load_nodes = {
            'ACTIVITY_SCOPE_OF_WORK_TYPE.E55':[
                'ACTIVITY_SCOPE_OF_WORK_TYPE.E55'
            ],
            'ACTIVITY_CONDITION.E3':[
                'ACTIVITY_CONDITION_TYPE.E55'
            ],
            'BUILDING_STRUCTURES_RECOMMENDATION_TYPE.E55':[
                'BUILDING_STRUCTURES_RECOMMENDATION_TYPE.E55',
            ],
            'OBJECT_RECOMMENDATION_TYPE.E55':[
                'OBJECT_RECOMMENDATION_TYPE.E55',
            ],
            'LANDSCAPE_RECOMMENDATION_TYPE.E55':[
                'LANDSCAPE_RECOMMENDATION_TYPE.E55',
            ]
        }
        
        for node, domains in load_nodes.iteritems():
            self.data[node] = {
                'branch_lists': self.get_nodes(node),
                'domains': dict([(d,Concept().get_e55_domain(d)) for d in domains])
            }

class DesDescriptionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'des-description',
            'icon': 'fa-flash',
            'name': _('Description'),
            'class': DesDescriptionForm
        }

    def update(self, data, files):
        self.update_nodes('DESCRIPTION.E62', data)
        self.update_nodes('NUMBER_OF_RESOURCES.E62', data)
        return

    def load(self, lang):
        #if self.resource:
        self.data['DESCRIPTION.E62'] = {
            'branch_lists': self.get_nodes('DESCRIPTION.E62'),
            'domains': {
                    'HISTORIC_AREA_DESCRIPTION_TYPE.E55' : Concept().get_e55_domain('HISTORIC_AREA_DESCRIPTION_TYPE.E55'), 
                },
        }
        
        self.data['NUMBER_OF_RESOURCES.E62'] = {
            'branch_lists': self.get_nodes('NUMBER_OF_RESOURCES.E62'),
            'domains': {
                    'NUMBER_OF_RESOURCES_TYPE.E55' : Concept().get_e55_domain('NUMBER_OF_RESOURCES_TYPE.E55'), 
                },
        }
        
class ActBDescriptionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'activity-b-description',
            'icon': 'fa-flash',
            'name': _('Description'),
            'class': ActBDescriptionForm
        }

    def update(self, data, files):
        self.update_nodes('ACTIVITY_B_USE.E55', data)
        self.update_nodes('ACTIVITY_B_PROJECT_TYPE.E55', data)
        return

    def load(self, lang):

        self.data['ACTIVITY_B_USE.E55'] = {
            'branch_lists': self.get_nodes('ACTIVITY_B_USE.E55'),
            'domains': {
                    'ACTIVITY_B_USE.E55' : Concept().get_e55_domain('ACTIVITY_B_USE.E55'), 
                },
        }
        
        self.data['ACTIVITY_B_PROJECT_TYPE.E55'] = {
            'branch_lists': self.get_nodes('ACTIVITY_B_PROJECT_TYPE.E55'),
            'domains': {
                    'ACTIVITY_B_PROJECT_TYPE.E55' : Concept().get_e55_domain('ACTIVITY_B_PROJECT_TYPE.E55'), 
                },
        }

class InventoryDescriptionForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'inventory-description',
            'icon': 'fa-picture-o',
            'name': _('Description'),
            'class': InventoryDescriptionForm
        }

    def update(self, data, files):

        self.update_nodes('DESCRIPTION.E62', data)

        if self.resource.entitytypeid == 'ACTOR.E39':
            self.update_nodes('PHASE_TYPE_ASSIGNMENT.E17', data)
        if self.resource.entitytypeid == 'INVENTORY_RESOURCE.E18':
            self.update_nodes('STYLE.E55', data)

    def load(self, lang):
        
        if self.resource:
        
            # used only for actors
            self.data['PHASE_TYPE_ASSIGNMENT.E17'] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes('PHASE_TYPE_ASSIGNMENT.E17')),
                'domains': {
                    'ACTOR_TYPE.E55' : Concept().get_e55_domain('ACTOR_TYPE.E55'),
                    'CULTURAL_PERIOD.E55' : Concept().get_e55_domain('CULTURAL_PERIOD.E55')
                }
            }
        
            self.data['DESCRIPTION.E62'] = {
                'branch_lists': self.get_nodes('DESCRIPTION.E62'),
                'domains': {
                    'DESCRIPTION_TYPE.E55' : Concept().get_e55_domain('DESCRIPTION_TYPE.E55'),
                    'ZONE_DESCRIPTION_TYPE.E55' : Concept().get_e55_domain('ZONE_DESCRIPTION_TYPE.E55'),
                },
            }
            
            # used only for inventory resources
            self.data['STYLE.E55'] = {
                'branch_lists': self.get_nodes('STYLE.E55'),
                'domains': {
                    'STYLE.E55' : Concept().get_e55_domain('STYLE.E55'),
                }               
            }