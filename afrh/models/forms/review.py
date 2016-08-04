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

class NCPCReviewForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'ncpc-review',
            'icon': 'fa-paperclip',
            'name': _('NCPC Review'),
            'class': NCPCReviewForm
        }

    def update(self, data, files):
        self.update_nodes('NCPC_REVIEW_IDENTIFICATION.E15', data)
        self.update_nodes('NCPC_SUBMISSION.E5', data)
        return

    def load(self, lang):

        self.data['NCPC_REVIEW_IDENTIFICATION.E15'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('NCPC_REVIEW_IDENTIFICATION.E15')),
        }
        
        self.data['NCPC_SUBMISSION.E5'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('NCPC_SUBMISSION.E5')),
            'domains': {
                'NCPC_SUBMISSION_TYPE.E55': Concept().get_e55_domain('NCPC_SUBMISSION_TYPE.E55'),
                'NCPC_SUBMISSION_DECISION.E55': Concept().get_e55_domain('NCPC_SUBMISSION_DECISION.E55'),
                'NCPC_SUBMISSION_REVIEW_TYPE.E55': Concept().get_e55_domain('NCPC_SUBMISSION_REVIEW_TYPE.E55'),
                
            }
        }

class HPOHPRBReviewForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'hpo-hprb-review',
            'icon': 'fa-paperclip',
            'name': _('HPO/HPRB Review'),
            'class': HPOHPRBReviewForm
        }

    def update(self, data, files):
        self.update_nodes('HPO-HPRB_REVIEW_IDENTIFICATION.E15', data)
        self.update_nodes('HPO-HPRB_SUBMISSION.E5', data)
        return

    def load(self, lang):

        self.data['HPO-HPRB_REVIEW_IDENTIFICATION.E15'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('HPO-HPRB_REVIEW_IDENTIFICATION.E15')),
        }
        
        self.data['HPO-HPRB_SUBMISSION.E5'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('HPO-HPRB_SUBMISSION.E5')),
            'domains': {
                'HPO-HPRB_SUBMISSION_TYPE.E55': Concept().get_e55_domain('HPO-HPRB_SUBMISSION_TYPE.E55'),
                'HPO-HPRB_SUBMISSION_DECISION.E55': Concept().get_e55_domain('HPO-HPRB_SUBMISSION_DECISION.E55'),
                'HPO-HPRB_SUBMISSION_REVIEW_TYPE.E55': Concept().get_e55_domain('HPO-HPRB_SUBMISSION_REVIEW_TYPE.E55'),
                
            }
        }

class CFAReviewForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'cfa-review',
            'icon': 'fa-paperclip',
            'name': _('CFA Review'),
            'class': CFAReviewForm
        }

    def update(self, data, files):
        self.update_nodes('CFA_REVIEW_IDENTIFICATION.E15', data)
        self.update_nodes('CFA_SUBMISSION.E5', data)
        return

    def load(self, lang):

        self.data['CFA_REVIEW_IDENTIFICATION.E15'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('CFA_REVIEW_IDENTIFICATION.E15')),
        }
        
        self.data['CFA_SUBMISSION.E5'] = {
            'branch_lists': datetime_nodes_to_dates(self.get_nodes('CFA_SUBMISSION.E5')),
            'domains': {
                'CFA_SUBMISSION_TYPE.E55': Concept().get_e55_domain('CFA_SUBMISSION_TYPE.E55'),
                'CFA_SUBMISSION_DECISION.E55': Concept().get_e55_domain('CFA_SUBMISSION_DECISION.E55'),
                'CFA_SUBMISSION_REVIEW_TYPE.E55': Concept().get_e55_domain('CFA_SUBMISSION_REVIEW_TYPE.E55'),
                
            }
        }

class Section106ReviewForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'section-oneohsix-review',
            'icon': 'fa-paperclip',
            'name': _('Section 106'),
            'class': Section106ReviewForm
        }

    def update(self, data, files):
        update_nodes = [
            'SECTION_106_EXEMPTION.E55',
            'DCSHPO_URR.E42',
            'DCSHPO_SUBMISSION.E5',
            'DCSHPO_RESPONSE.E5',
            'SECTION_106_NOTIFICATION.E5',
            'SECTION_106_DISPUTE_RESOLUTION_NOTES.E62',
            'SECTION_106_AGREEMENT.E5',
        ]
        
        for node in update_nodes:
            self.update_nodes(node, data)

        return

    def load(self, lang):
        
        load_nodes = {
            'SECTION_106_EXEMPTION.E55':[
                'SECTION_106_EXEMPTION_TYPE.E55'
            ],
            'DCSHPO_URR.E42':[],
            'DCSHPO_SUBMISSION.E5':[
                'DCSHPO_SUBMISSION_TYPE.E55',
                'DCSHPO_SUBMISSION_METHOD.E55',
                'AFRH_DETERMINATION_OF_EFFECT.E55',
            ],
            'DCSHPO_RESPONSE.E5':[
                'DCSHPO_RESPONSE_TYPE.E55',
                'DCSHPO_RESPONSE_EVALUATION.E55',
            ],
            'SECTION_106_NOTIFICATION.E5':[
                'SECTION_106_NOTIFICATION_TYPE.E55',
                'SECTION_106_NOTIFICATION_METHOD.E55',
            ],
            'SECTION_106_DISPUTE_RESOLUTION_NOTES.E62':[],
            'SECTION_106_AGREEMENT.E5':[
                'SECTION_106_AGREEMENT_TYPE.E55',
            ]
        }
        
        for node, domains in load_nodes.iteritems():
            self.data[node] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes(node)),
                'domains': dict([(d,Concept().get_e55_domain(d)) for d in domains])
            }
        
        return

class ARPAReviewForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'arpa-review',
            'icon': 'fa-paperclip',
            'name': _('ARPA Review'),
            'class': ARPAReviewForm
        }

    def update(self, data, files):
        update_nodes = [
            'GROUND_DISTURBANCE.E62',
            'GROUND_DISTURBANCE_LOCATION.E27',
            'AFRH_ARPA_ASSESSMENT.E5',
            'DCSHPO_NOTIFICATION.E5',
            'ARPA_DOCUMENTATION.E31',
            'ARPA_FIELD_INVESTIGATION.E5',
            'ARPA_DISCOVERY.E5'
        ]
        
        for node in update_nodes:
            print node
            print data
            self.update_nodes(node, data)

        return

    def load(self, lang):
        
        load_nodes = {
            'GROUND_DISTURBANCE.E62':[],
            'GROUND_DISTURBANCE_LOCATION.E27':[
                'GROUND_DISTURBANCE_LOCATION.E27'
            ],
            'AFRH_ARPA_ASSESSMENT.E5':[
                'AFRH_ARPA_DETERMINATION.E55',
            ],
            'DCSHPO_NOTIFICATION.E5':[
                'DCSHPO_NOTIFICATION_METHOD.E55',
                'DCSHPO_NOTIFICATION_RESPONSE.E55',
            ],
            'ARPA_DOCUMENTATION.E31':[
                'ARPA_DOCUMENTATION_TYPE.E55',
                'ARPA_DOCUMENTATION_STATUS.E55',
                'ARPA_DOCUMENTATION_SUBMISSION_METHOD.E55',
            ],
            'ARPA_FIELD_INVESTIGATION.E5':[
                'ARPA_FIELD_INVESTIGATION_TYPE.E55',
                'ARPA_FIELD_INVESTIGATION_ARTIFACT_STATUS.E55',
            ],
            'ARPA_DISCOVERY.E5':[
                'ARPA_DISCOVERY_ARTIFACT_STATUS.E55',
            ]
        }
        
        for node, domains in load_nodes.iteritems():

            self.data[node] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes(node)),
                'domains': dict([(d,Concept().get_e55_domain(d)) for d in domains])
            }
        
        return

class NEPAReviewForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'nepa-review',
            'icon': 'fa-paperclip',
            'name': _('NEPA Review'),
            'class': NEPAReviewForm
        }

    def update(self, data, files):
        update_nodes = [
            'NEPA_DOCUMENTATION.E31',
            'EA_TYPE.E55',
            'CATEX_TYPE.E55',
            'EIS_TYPE.E55',
            'NEPA_DOCUMENTATION_TYPE.E55',
        ]
        
        for node in update_nodes:
            self.update_nodes(node, data)

        return

    def load(self, lang):
        
        load_nodes = {
            'NEPA_DOCUMENTATION.E31':[
                'NEPA_DOCUMENTATION.E31'
            ],
            'EA_TYPE.E55':[
                'EA_TYPE.E55'
            ],
            'CATEX_TYPE.E55':[
                'CATEX_TYPE.E55',
            ],
            'EIS_TYPE.E55':[
                'EIS_TYPE.E55',
            ],
            'NEPA_DOCUMENTATION_TYPE.E55':[
                'NEPA_DOCUMENTATION_TYPE.E55',
            ]
        }
        
        for node, domains in load_nodes.iteritems():

            self.data[node] = {
                'branch_lists': datetime_nodes_to_dates(self.get_nodes(node)),
                'domains': dict([(d,Concept().get_e55_domain(d)) for d in domains])
            }
        
        return