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
import json, os, urllib
import urllib2

def get_browse_info():
    domain_nodes = [
        'CHARACTER_AREA.E44',
        'MASTER_PLAN_ZONE.E44',
        'OTHER_DESIGNATION_TYPE.E55',
        'NRHP_RESOURCE_TYPE.E55',
        'RELATIVE_LEVEL_OF_SIGNIFICANCE.E55',
        'PERIOD_OF_SIGNIFICANCE.E55',
        'AREA_OF_SIGNIFICANCE.E55',
        'STYLE.E55',
        'CURRENT_OPERATIONAL_STATUS.E55',
    ]
    
    browse_dict = {}
    new_dict = {}
    
    for node in domain_nodes:
        context_node = Concept().get(legacyoid=node)
        entries = Concept().get_e55_domain(node)
        node_name = node.split(".")[0]
        browse_dict[node_name] = {}
        
        for entry in entries:
            
            entry_id = entry['sortorder']
            concept_name = entry['text']

            browse_dict[node_name][entry_id] = {}
            
            e_concept = Concept().get(id=entry['conceptid'])
            string = '[{{"inverted":false,"type":"concept","context":"{0}",'\
            '"context_label":"","id":"{1}{0}","text":"{1}",'\
            '"value":"{2}"}}]'.format(context_node.id,entry['text'],e_concept.id)
            url = urllib.quote(string)

            browse_dict[node_name][entry_id] = {
                "term_filter": url,
                "name": concept_name
            }

    return browse_dict


# class InventorySummaryForm(ResourceForm):
    # @staticmethod
    # def get_info():
        # return {
            # 'id': 'inventory-summary',
            # 'icon': 'fa-tag',
            # 'name': _('Summary'),
            # 'class': InventorySummaryForm
        # }

    # def update(self, data, files):
        # self.update_nodes('NAME.E41', data)
        # self.update_nodes('NHRP_RESOURCE_TYPE.E55', data)
        # self.update_nodes('NHRP_RESOURCE_CATEGORY.E55', data)
        # self.update_nodes('NHRP_RESOURCE_SUBCATEGORY.E55', data)
        # self.update_nodes('WUZIT.E55', data)
        # self.update_nodes('BUILDING_NUMBER.E42', data)
        # if self.resource.entitytypeid in ('INVENTORY_RESOURCE.E18', 'HERITAGE_RESOURCE_GROUP.E27'):   
           # self.update_nodes('NHRP_RESOURCE_TYPE.E55', data)

        # beginning_of_existence_nodes = []
        # end_of_existence_nodes = []
        # for branch_list in data['important_dates']:
            # for node in branch_list['nodes']:
                # if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_TYPE.E55':
                    # print "BEGINNING_OF_EXISTENCE_TYPE.E55 branchlist:"
                    # print branch_list
                    # beginning_of_existence_nodes.append(branch_list)
                # if node['entitytypeid'] == 'END_OF_EXISTENCE_TYPE.E55':
                    # print "END_OF_EXISTENCE_TYPE.E55 branchlist:"
                    # print branch_list
                    # end_of_existence_nodes.append(branch_list)

        # for branch_list in beginning_of_existence_nodes:
            # for node in branch_list['nodes']:        
                # if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    # node['entitytypeid'] = 'START_DATE_OF_EXISTENCE.E49'
                # if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_NOTE.E62,END_OF_EXISTENCE_NOTE.E62':
                    # node['entitytypeid'] = 'BEGINNING_OF_EXISTENCE_NOTE.E62'

        # for branch_list in end_of_existence_nodes:
            # for node in branch_list['nodes']:        
                # if node['entitytypeid'] == 'START_DATE_OF_EXISTENCE.E49,END_DATE_OF_EXISTENCE.E49':
                    # node['entitytypeid'] = 'END_DATE_OF_EXISTENCE.E49'
                # if node['entitytypeid'] == 'BEGINNING_OF_EXISTENCE_NOTE.E62,END_OF_EXISTENCE_NOTE.E62':
                    # node['entitytypeid'] = 'END_OF_EXISTENCE_NOTE.E62'

        # self.update_nodes('BEGINNING_OF_EXISTENCE.E63', {'BEGINNING_OF_EXISTENCE.E63':beginning_of_existence_nodes})
        # self.update_nodes('END_OF_EXISTENCE.E64', {'END_OF_EXISTENCE.E64':end_of_existence_nodes})

    # def load(self, lang):
        # self.data['important_dates'] = {
            # 'branch_lists': datetime_nodes_to_dates(self.get_nodes('BEGINNING_OF_EXISTENCE.E63') + self.get_nodes('END_OF_EXISTENCE.E64')),
            # 'domains': {
                # 'important_dates' : Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_TYPE.E55') + Concept().get_e55_domain('END_OF_EXISTENCE_TYPE.E55'),
                # 'date_qualifiers': Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_QUALIFIER.E55')
            # }
        # }

        # if self.resource:
            # if self.resource.entitytypeid in ('INVENTORY_RESOURCE.E18', 'HERITAGE_RESOURCE_GROUP.E27'):            
               # self.data['NHRP_RESOURCE_TYPE.E55'] = {
                   # 'branch_lists': self.get_nodes('NHRP_RESOURCE_TYPE.E55'),
                   # 'domains': {'NHRP_RESOURCE_TYPE.E55' : Concept().get_e55_domain('NHRP_RESOURCE_TYPE.E55')}
               # }
            
            # self.data['NHRP_RESOURCE_TYPE.E55'] = {
                # 'branch_lists': self.get_nodes('NHRP_RESOURCE_TYPE.E55'),
                # 'domains': {'NHRP_RESOURCE_TYPE.E55' : Concept().get_e55_domain('NHRP_RESOURCE_TYPE.E55')}
                # }
                
            # self.data['NHRP_RESOURCE_CATEGORY.E55'] = {
                # 'branch_lists': self.get_nodes('NHRP_RESOURCE_CATEGORY.E55'),
                # 'domains': {'NHRP_RESOURCE_CATEGORY.E55' : Concept().get_e55_domain('NHRP_RESOURCE_CATEGORY.E55')}
                # }
                
            # self.data['NHRP_RESOURCE_SUBCATEGORY.E55'] = {
                # 'branch_lists': self.get_nodes('NHRP_RESOURCE_SUBCATEGORY.E55'),
                # 'domains': {'NHRP_RESOURCE_SUBCATEGORY.E55' : Concept().get_e55_domain('NHRP_RESOURCE_SUBCATEGORY.E55')}
                # }
                
            # self.data['WUZIT.E55'] = {
                # 'branch_lists': self.get_nodes('WUZIT.E55'),
                # 'domains': {'WUZIT.E55' : Concept().get_e55_domain('WUZIT.E55')}
                # }

            # self.data['NAME.E41'] = {
                # 'branch_lists': self.get_nodes('NAME.E41'),
                # 'domains': {'NAME_TYPE.E55' : Concept().get_e55_domain('NAME_TYPE.E55')}
                # 'defaults': {
                    # 'NAME_TYPE.E55': default_name_type['id'],
                    # 'NAME.E41': ''
                # }
                # }
            
            # self.data['BUILDING_NUMBER.E42'] = {
                # 'branch_lists': self.get_nodes('BUILDING_NUMBER.E42'),
                # 'domains': {'BUILDING_NUMBER_TYPE.E55' : Concept().get_e55_domain('BUILDING_NUMBER_TYPE.E55')}
                # }

            # try:
                # self.data['primaryname_conceptid'] = self.data['NAME.E41']['domains']['NAME_TYPE.E55'][0]['id']
            # except IndexError:
                # pass
