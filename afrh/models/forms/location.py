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

class SimpleLocationForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'simple-location',
            'icon': 'fa-map-marker',
            'name': _('Location'),
            'class': SimpleLocationForm
        }

    def update(self, data, files):
    
        if self.resource.entitytypeid == 'ARCHAEOLOGICAL_ZONE.E53':
            self.update_nodes('ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY.E47', data)
            self.update_nodes('ARCHAEOLOGICAL_ZONE_BOUNDARY_NOTE.E62', data)
        else:
            self.update_nodes('SPATIAL_COORDINATES_GEOMETRY.E47', data)
        if self.resource.entitytypeid == 'CHARACTER_AREA.E53':
            self.update_nodes('CHARACTER_AREA_PLACE_NOTE.E62', data)
        if self.resource.entitytypeid == 'HISTORIC_AREA.E53':
            self.update_nodes('HISTORIC_AREA_LOCATION_NOTE.E62', data)
        if self.resource.entitytypeid == 'MASTER_PLAN_ZONE.E53':
            self.update_nodes('PLACE_DESCRIPTION.E62', data)
    
        return

    def load(self, lang):
        self.data['SPATIAL_COORDINATES_GEOMETRY.E47'] = {
            'branch_lists': self.get_nodes('SPATIAL_COORDINATES_GEOMETRY.E47'),
        }
        
        self.data['ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY.E47'] = {
            'branch_lists': self.get_nodes('ARCHAEOLOGICAL_ZONE_BOUNDARY_GEOMETRY.E47'),
        }
        
        self.data['CHARACTER_AREA_PLACE_NOTE.E62'] = {
            'branch_lists': self.get_nodes('CHARACTER_AREA_PLACE_NOTE.E62'),
        }
        
        self.data['HISTORIC_AREA_LOCATION_NOTE.E62'] = {
            'branch_lists': self.get_nodes('HISTORIC_AREA_LOCATION_NOTE.E62'),
        }
        
        self.data['PLACE_DESCRIPTION.E62'] = {
            'branch_lists': self.get_nodes('PLACE_DESCRIPTION.E62'),
        }
        
        self.data['ARCHAEOLOGICAL_ZONE_BOUNDARY_NOTE.E62'] = {
            'branch_lists': self.get_nodes('ARCHAEOLOGICAL_ZONE_BOUNDARY_NOTE.E62'),
        }
        
        return

class LocationForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'location',
            'icon': 'fa-map-marker',
            'name': _('Location'),
            'class': LocationForm
        }

    def update(self, data, files):
        
        
        self.update_nodes('DESCRIPTION_OF_LOCATION.E62', data)
        if self.resource.entitytypeid in ['INVENTORY_RESOURCE.E18','ACTIVITY.E7']:
            self.update_nodes('SPATIAL_COORDINATES_GEOMETRY.E47', data)
            self.update_nodes('CHARACTER_AREA.E44', data)
            self.update_nodes('MASTER_PLAN_ZONE.E44', data)
            self.update_nodes('ARCHAEOLOGICAL_ZONE.E44', data)
        if self.resource.entitytypeid  == 'INFORMATION_RESOURCE.E73':
            self.update_nodes('SPATIAL_COORDINATES_GEOMETRY.E47', data)
            self.update_nodes('COLLECTION.E78', data)
            #self.update_nodes('TEMPORAL_COVERAGE_TIME-SPAN.E52', data)
        if self.resource.entitytypeid  != 'INFORMATION_RESOURCE.E73':
            self.update_nodes('PLACE_ADDRESS.E45', data)
        
##        if self.resource.entitytypeid not in ['ACTOR.E39']:
##            self.update_nodes('SPATIAL_COORDINATES_GEOMETRY.E47', data)
##            self.update_nodes('ADMINISTRATIVE_SUBDIVISION_NAME.E55', data)
##        if self.resource.entitytypeid not in ['ACTOR.E39', 'ACTIVITY.E7', 'HISTORICAL_EVENT.E5']:
##            self.update_nodes('PLACE_APPELLATION_CADASTRAL_REFERENCE.E44', data)
##        if self.resource.entitytypeid not in ['ACTOR.E39', 'ACTIVITY.E7', 'HERITAGE_RESOURCE_GROUP.E27', 'HISTORICAL_EVENT.E5']:
##            self.update_nodes('SETTING_TYPE.E55', data)
##        self.update_nodes('PLACE_ADDRESS.E45', data)
##        self.update_nodes('DESCRIPTION_OF_LOCATION.E62', data)
        return

    def load(self, lang):
        self.data['SPATIAL_COORDINATES_GEOMETRY.E47'] = {
            'branch_lists': self.get_nodes('SPATIAL_COORDINATES_GEOMETRY.E47'),
            'domains': {
                'GEOMETRY_QUALIFIER.E55': Concept().get_e55_domain('GEOMETRY_QUALIFIER.E55')
            }
        }

        self.data['PLACE_ADDRESS.E45'] = {
            'branch_lists': self.get_nodes('PLACE_ADDRESS.E45'),
            'domains': {
                'ADDRESS_TYPE.E55': Concept().get_e55_domain('ADDRESS_TYPE.E55')
            }
        }
        
        self.data['DESCRIPTION_OF_LOCATION.E62'] = {
            'branch_lists': self.get_nodes('DESCRIPTION_OF_LOCATION.E62'),
            'domains': {}
        }

        self.data['CHARACTER_AREA.E44'] = {
            'branch_lists': self.get_nodes('CHARACTER_AREA.E44'),
            'domains': {
                'CHARACTER_AREA.E44': Concept().get_e55_domain('CHARACTER_AREA.E44')
            }
        }

        self.data['MASTER_PLAN_ZONE.E44'] = {
            'branch_lists': self.get_nodes('MASTER_PLAN_ZONE.E44'),
            'domains': {
                'MASTER_PLAN_ZONE.E44': Concept().get_e55_domain('MASTER_PLAN_ZONE.E44')
            }
        }
        
        self.data['ARCHAEOLOGICAL_ZONE.E44'] = {
            'branch_lists': self.get_nodes('ARCHAEOLOGICAL_ZONE.E44'),
            'domains': {
                'ARCHAEOLOGICAL_ZONE.E44': Concept().get_e55_domain('ARCHAEOLOGICAL_ZONE.E44')
            }
        }
        
        self.data['TEMPORAL_COVERAGE_TIME-SPAN.E52'] = {
            'branch_lists': self.get_nodes('TEMPORAL_COVERAGE_TIME-SPAN.E52'),
            'domains': {}
        }
        
        self.data['COLLECTION.E78'] = {
            'branch_lists': self.get_nodes('COLLECTION.E78'),
            'domains': {
                'COLLECTION_TYPE.E55': Concept().get_e55_domain('COLLECTION_TYPE.E55')
            }
        }
        
        return
        
class ProbabilityAreaForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'probability-areas',
            'icon': 'fa-map-marker',
            'name': _('Areas of Probability'),
            'class': ProbabilityAreaForm
        }

    def update(self, data, files):
        
        
        self.update_nodes('AREA_OF_PROBABILITY_GEOMETRY.E47', data)
        self.update_nodes('HISTORIC_RESOURCES_AREA_NOTE.E62', data)
        self.update_nodes('NATIVE_AMERICAN_RESOURCES_AREA_NOTE.E62', data)
        self.update_nodes('PALEOSOLS_ZONE_NOTE.E62', data)
        self.update_nodes('DISTURBED_AREA_NOTE.E62', data)

        return

    def load(self, lang):
        self.data['AREA_OF_PROBABILITY_GEOMETRY.E47'] = {
            'branch_lists': self.get_nodes('AREA_OF_PROBABILITY_GEOMETRY.E47'),
            'domains': {
                'AREA_OF_PROBABILITY_GEOMETRY_TYPE.E55': Concept().get_e55_domain('AREA_OF_PROBABILITY_GEOMETRY_TYPE.E55')
            }
        }
        
        self.data['HISTORIC_RESOURCES_AREA_NOTE.E62'] = {
            'branch_lists': self.get_nodes('HISTORIC_RESOURCES_AREA_NOTE.E62'),
        }
        
        self.data['NATIVE_AMERICAN_RESOURCES_AREA_NOTE.E62'] = {
            'branch_lists': self.get_nodes('NATIVE_AMERICAN_RESOURCES_AREA_NOTE.E62'),
        }
        
        self.data['PALEOSOLS_ZONE_NOTE.E62'] = {
            'branch_lists': self.get_nodes('PALEOSOLS_ZONE_NOTE.E62'),
        }
        
        self.data['DISTURBED_AREA_NOTE.E62'] = {
            'branch_lists': self.get_nodes('DISTURBED_AREA_NOTE.E62'),
        }

        return

#not used
class CoverageForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'coverage',
            'icon': 'fa-crosshairs',
            'name': _('Coverage'),
            'class': CoverageForm
        }

    def update(self, data, files):
        self.update_nodes('SPATIAL_COORDINATES_GEOMETRY.E47', data)    
        self.update_nodes('DESCRIPTION_OF_LOCATION.E62', data)
        self.update_nodes('TEMPORAL_COVERAGE_TIME-SPAN.E52', data)
        return

    def load(self, lang):
        self.data['SPATIAL_COORDINATES_GEOMETRY.E47'] = {
            'branch_lists': self.get_nodes('SPATIAL_COORDINATES_GEOMETRY.E47'),
            'domains': {
                'GEOMETRY_QUALIFIER.E55': Concept().get_e55_domain('GEOMETRY_QUALIFIER.E55')
            }
        }
        
        self.data['DESCRIPTION_OF_LOCATION.E62'] = {
            'branch_lists': self.get_nodes('DESCRIPTION_OF_LOCATION.E62'),
            'domains': {}
        }

        self.data['TEMPORAL_COVERAGE_TIME-SPAN.E52'] = {
            'branch_lists': self.get_nodes('TEMPORAL_COVERAGE_TIME-SPAN.E52'),
            'domains': {}
        }

        return
