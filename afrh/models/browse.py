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
from collections import OrderedDict

def get_browse_info():
    domain_nodes = [
        'CHARACTER_AREA.E44',
        'MASTER_PLAN_ZONE.E44',
        'OTHER_AFRH_W_DESIGNATION_TYPE.E55',
        'NRHP_RESOURCE_TYPE.E55',
        'RELATIVE_LEVEL_OF_SIGNIFICANCE.E55',
        'PERIOD_OF_SIGNIFICANCE.E55',
        'AREA_OF_SIGNIFICANCE.E55',
        'STYLE.E55',
        'CURRENT_OPERATIONAL_STATUS.E55',
    ]
    
    browse_dict = {}
    
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
