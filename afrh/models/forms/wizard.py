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

class ClassificationForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'classification',
            'icon': 'fa-adjust',
            'name': _('Function and Use'),
            'class': ClassificationForm
        }

    def get_nodes(self, entity, entitytypeid):
        ret = []
        entities = entity.find_entities_by_type_id(entitytypeid)
        for entity in entities:
            ret.append({'nodes': entity.flatten()})

        return ret

    def update_nodes(self, entitytypeid, data):
        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)
        for value in data[entitytypeid]:
            for newentity in value['nodes']:
                entity = Entity()
                entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                if self.baseentity == None:
                    self.baseentity = entity
                else:
                    self.baseentity.merge(entity)

    def update(self, data, files):

        self.update_nodes('HERITAGE_RESOURCE_TYPE.E55', data)
        self.update_nodes('TO_DATE.E49', data)
        self.update_nodes('FROM_DATE.E49', data)
        self.update_nodes('HERITAGE_RESOURCE_USE_TYPE.E55', data)
        self.update_nodes('ANCILLARY_FEATURE_TYPE.E55', data)
        production_entities = self.resource.find_entities_by_type_id('PRODUCTION.E12')

        phase_type_node_id = ''
        for value in data['PHASE_TYPE_ASSIGNMENT.E17']:
            for node in value['nodes']:
                if node['entitytypeid'] == 'PHASE_TYPE_ASSIGNMENT.E17' and node['entityid'] != '':
                    #remove the node
                    phase_type_node_id = node['entityid']
                    self.resource.filter(lambda entity: entity.entityid != node['entityid'])

        for entity in self.baseentity.find_entities_by_type_id('PHASE_TYPE_ASSIGNMENT.E17'):
            entity.entityid = phase_type_node_id

        if len(production_entities) > 0:
            self.resource.merge_at(self.baseentity, 'PRODUCTION.E12')
        else:
            self.resource.merge_at(self.baseentity, self.resource.entitytypeid)

        self.resource.trim()
                   
    def load(self, lang):

        self.data = {
            'data': [],
            'domains': {
                'HERITAGE_RESOURCE_TYPE.E55': Concept().get_e55_domain('HERITAGE_RESOURCE_TYPE.E55'),
                'HERITAGE_RESOURCE_USE_TYPE.E55' : Concept().get_e55_domain('HERITAGE_RESOURCE_USE_TYPE.E55'),
                'ANCILLARY_FEATURE_TYPE.E55' : Concept().get_e55_domain('ANCILLARY_FEATURE_TYPE.E55')
            }
        }

        classification_entities = self.resource.find_entities_by_type_id('PHASE_TYPE_ASSIGNMENT.E17')

        for entity in classification_entities:
            to_date_nodes = datetime_nodes_to_dates(self.get_nodes(entity, 'TO_DATE.E49'))
            from_date_nodes = datetime_nodes_to_dates(self.get_nodes(entity, 'FROM_DATE.E49'))

            self.data['data'].append({
                'HERITAGE_RESOURCE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'HERITAGE_RESOURCE_TYPE.E55')
                },
                'HERITAGE_RESOURCE_USE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'HERITAGE_RESOURCE_USE_TYPE.E55')
                },
                'TO_DATE.E49': {
                    'branch_lists': to_date_nodes
                },
                'FROM_DATE.E49': {
                    'branch_lists': from_date_nodes
                },
                'ANCILLARY_FEATURE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'ANCILLARY_FEATURE_TYPE.E55')
                },              
                'PHASE_TYPE_ASSIGNMENT.E17': {
                    'branch_lists': self.get_nodes(entity, 'PHASE_TYPE_ASSIGNMENT.E17')
                }
            })

class MPZoneGuidelinesForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'mpz-guidelines',
            'icon': 'fa-asterisk',
            'name': _('Guidelines'),
            'class': MPZoneGuidelinesForm
        }

    def get_nodes(self, entity, entitytypeid):
        ret = []
        entities = entity.find_entities_by_type_id(entitytypeid)
        for entity in entities:
            ret.append({'nodes': entity.flatten()})
        #print json.dumps(ret, indent=2)
        print entitytypeid
        for i in ret:
            for e in i['nodes']:
                print e
        return ret

    def update_nodes(self, entitytypeid, data):
        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)

        for value in data[entitytypeid]:
            if entitytypeid == 'GUIDELINE_IMAGE.E73':
                temp = None
                for newentity in value['nodes']:
                    if newentity['entitytypeid'] != 'GUIDELINE_IMAGE.E73':
                        entity = Entity()
                        entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                        if temp == None:
                            temp = entity
                        else:
                            temp.merge(entity)

                self.baseentity.merge_at(temp, 'GUIDELINE.E89')
            else:
                for newentity in value['nodes']:
                    entity = Entity()
                    entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                    if self.baseentity == None:
                        self.baseentity = entity
                    else:
                        self.baseentity.merge(entity)

    def update(self, data, files):
        if len(files) > 0:
            for f in files:
                data['GUIDELINE_IMAGE.E73'].append({
                    'nodes':[{
                        'entitytypeid': 'GUIDELINE_IMAGE_FILE_PATH.E62',
                        'entityid': '',
                        'value': files[f]
                    },{
                        'entitytypeid': 'GUIDELINE_IMAGE_THUMBNAIL.E62',
                        'entityid': '',
                        'value': generate_thumbnail(files[f])
                    }]
                })

        for value in data['GUIDELINE.E89']:
            for node in value['nodes']:
                if node['entitytypeid'] == 'GUIDELINE.E89' and node['entityid'] != '':
                    #remove the node
                    self.resource.filter(lambda entity: entity.entityid != node['entityid'])

        self.update_nodes('GUIDELINE_TYPE.E55', data)
        self.update_nodes('GUIDELINE_NOTE.E62', data)
        self.update_nodes('GUIDELINE_IMAGE.E73', data)
        self.update_nodes('GUIDELINE_IMAGE_NOTE.E62', data)
        #self.update_nodes('GUIDELINE_IMAGE_TYPE.E55', data)
        self.resource.merge_at(self.baseentity, self.resource.entitytypeid)
        self.resource.trim()
                   
    def load(self, lang):
        self.data = {
            'data': [],
            'domains': {
                'GUIDELINE_TYPE.E55': Concept().get_e55_domain('GUIDELINE_TYPE.E55'),
                'GUIDELINE_IMAGE_TYPE.E55' : Concept().get_e55_domain('GUIDELINE_IMAGE_TYPE.E55'),
            }
        }
        
        
        condition_assessment_entities = self.resource.find_entities_by_type_id('GUIDELINE.E89')
        print "entities"
        print condition_assessment_entities

        for entity in condition_assessment_entities:
            self.data['data'].append({
                'GUIDELINE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'GUIDELINE_TYPE.E55')
                },
                'GUIDELINE_NOTE.E62': {
                    'branch_lists': self.get_nodes(entity, 'GUIDELINE_NOTE.E62')
                },
                'GUIDELINE_IMAGE_NOTE.E62': {
                    'branch_lists': self.get_nodes(entity, 'GUIDELINE_IMAGE_NOTE.E62')
                },
                'GUIDELINE_IMAGE.E73': {
                    'branch_lists': self.get_nodes(entity, 'GUIDELINE_IMAGE.E73'),
                },
                'GUIDELINE.E89': {
                    'branch_lists': self.get_nodes(entity, 'GUIDELINE.E89')
                }
            })
            
class ConditionForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'condition',
            'icon': 'fa-asterisk',
            'name': _('Condition Assessment'),
            'class': ConditionForm
        }

    def get_nodes(self, entity, entitytypeid):
        ret = []
        entities = entity.find_entities_by_type_id(entitytypeid)
        for entity in entities:
            ret.append({'nodes': entity.flatten()})

        return ret

    def update_nodes(self, entitytypeid, data):
        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)

        for value in data[entitytypeid]:
            if entitytypeid == 'CONDITION_IMAGE.E73':
                temp = None
                for newentity in value['nodes']:
                    if newentity['entitytypeid'] != 'CONDITION_IMAGE.E73':
                        entity = Entity()
                        entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                        if temp == None:
                            temp = entity
                        else:
                            temp.merge(entity)

                self.baseentity.merge_at(temp, 'CONDITION_STATE.E3')
            else:
                for newentity in value['nodes']:
                    entity = Entity()
                    entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                    if self.baseentity == None:
                        self.baseentity = entity
                    else:
                        self.baseentity.merge(entity)

    def update(self, data, files):
        print json.dumps(data, indent=2)
        if len(files) > 0:
            for f in files:
                data['CONDITION_IMAGE.E73'].append({
                    'nodes':[{
                        'entitytypeid': 'CONDITION_IMAGE_FILE_PATH.E62',
                        'entityid': '',
                        'value': files[f]
                    },{
                        'entitytypeid': 'CONDITION_IMAGE_THUMBNAIL.E62',
                        'entityid': '',
                        'value': generate_thumbnail(files[f])
                    }]
                })

        for value in data['CONDITION_ASSESSMENT.E14']:
            for node in value['nodes']:
                if node['entitytypeid'] == 'CONDITION_ASSESSMENT.E14' and node['entityid'] != '':
                    #remove the node
                    self.resource.filter(lambda entity: entity.entityid != node['entityid'])

        self.update_nodes('CONDITION_TYPE.E55', data)
        self.update_nodes('CONDITION_ASSESSMENT_TYPE.E55', data)
        self.update_nodes('THREAT_TYPE.E55', data)
        self.update_nodes('RECOMMENDATION_TYPE.E55', data)
        self.update_nodes('DATE_CONDITION_ASSESSED.E49', data)
        self.update_nodes('CONDITION_DESCRIPTION.E62', data)
        self.update_nodes('DISTURBANCE_TYPE.E55', data)
        self.update_nodes('CONDITION_IMAGE.E73', data)
        self.resource.merge_at(self.baseentity, self.resource.entitytypeid)
        self.resource.trim()
                   
    def load(self, lang):

        self.data = {
            'data': [],
            'domains': {
                'DISTURBANCE_TYPE.E55': Concept().get_e55_domain('DISTURBANCE_TYPE.E55'),
                'CONDITION_TYPE.E55' : Concept().get_e55_domain('CONDITION_TYPE.E55'),
                'CONDITION_ASSESSMENT_TYPE.E55' : Concept().get_e55_domain('CONDITION_ASSESSMENT_TYPE.E55'),
                'THREAT_TYPE.E55' : Concept().get_e55_domain('THREAT_TYPE.E55'),
                'RECOMMENDATION_TYPE.E55' : Concept().get_e55_domain('RECOMMENDATION_TYPE.E55')
            }
        }

        condition_assessment_entities = self.resource.find_entities_by_type_id('CONDITION_ASSESSMENT.E14')

        for entity in condition_assessment_entities:
            self.data['data'].append({
                'DISTURBANCE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'DISTURBANCE_TYPE.E55')
                },
                'CONDITION_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_TYPE.E55')
                },
                'CONDITION_ASSESSMENT_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_ASSESSMENT_TYPE.E55')
                },
                'THREAT_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'THREAT_TYPE.E55')
                },
                'RECOMMENDATION_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'RECOMMENDATION_TYPE.E55')
                },
                'DATE_CONDITION_ASSESSED.E49': {
                    'branch_lists': datetime_nodes_to_dates(self.get_nodes(entity, 'DATE_CONDITION_ASSESSED.E49'))
                },
                'CONDITION_DESCRIPTION.E62': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_DESCRIPTION.E62')
                },
                'CONDITION_IMAGE.E73': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_IMAGE.E73')
                },
                'CONDITION_ASSESSMENT.E14': {
                    'branch_lists': self.get_nodes(entity, 'CONDITION_ASSESSMENT.E14')
                }
            })
            
class ActivityConsultationForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'activity-consultation',
            'icon': 'fa-asterisk',
            'name': _('Consultations'),
            'class': ActivityConsultationForm
        }

    def get_nodes(self, entity, entitytypeid):
        ret = []
        entities = entity.find_entities_by_type_id(entitytypeid)
        for entity in entities:
            ret.append({'nodes': entity.flatten()})

        return ret

    def update_nodes(self, entitytypeid, data):
        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)

        for value in data[entitytypeid]:
            for newentity in value['nodes']:
                entity = Entity()
                entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                if self.baseentity == None:
                    self.baseentity = entity
                else:
                    self.baseentity.merge(entity)

    def update(self, data, files):
        print json.dumps(data, indent=2)

        for value in data['ACTIVITY_CONSULTATION.E5']:
            for node in value['nodes']:
                if node['entitytypeid'] == 'ACTIVITY_CONSULTATION.E5' and node['entityid'] != '':
                    #remove the node
                    self.resource.filter(lambda entity: entity.entityid != node['entityid'])

        #self.update_nodes('ACTIVITY_CONSULTATION.E5', data)
        self.update_nodes('CONSULTATION_METHOD.E55', data)
        self.update_nodes('CONSULTATION_TYPE.E55', data)
        self.update_nodes('CONSULTATION_DATE.E49', data)
        self.update_nodes('CONSULTATION_NOTE.E62', data)
        self.update_nodes('CONSULTATION_DOCUMENTATION_TYPE.E55', data)
        self.update_nodes('CONSULTATION_ATTENDEE.E39', data)
        self.resource.merge_at(self.baseentity, self.resource.entitytypeid)
        self.resource.trim()
                   
    def load(self, lang):

        self.data = {
            'data': [],
            'domains': {
                'CONSULTATION_METHOD.E55': Concept().get_e55_domain('CONSULTATION_METHOD.E55'),
                'CONSULTATION_TYPE.E55' : Concept().get_e55_domain('CONSULTATION_TYPE.E55'),
                'CONSULTATION_DOCUMENTATION_TYPE.E55' : Concept().get_e55_domain('CONSULTATION_DOCUMENTATION_TYPE.E55'),
            }
        }

        print self.resource
        consultation_entities = self.resource.find_entities_by_type_id('ACTIVITY_CONSULTATION.E5')
        print "consultation entities:"
        print consultation_entities

        for entity in consultation_entities:
            print entity
            self.data['data'].append({
                'CONSULTATION_METHOD.E55': {
                    'branch_lists': self.get_nodes(entity, 'CONSULTATION_METHOD.E55')
                },
                'CONSULTATION_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'CONSULTATION_TYPE.E55')
                },
                'CONSULTATION_DOCUMENTATION_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'CONSULTATION_DOCUMENTATION_TYPE.E55')
                },
                'CONSULTATION_ATTENDEE.E39': {
                    'branch_lists': self.get_nodes(entity, 'CONSULTATION_ATTENDEE.E39')
                },
                'CONSULTATION_DATE.E49': {
                    'branch_lists': datetime_nodes_to_dates(self.get_nodes(entity, 'CONSULTATION_DATE.E49'))
                },
                'CONSULTATION_NOTE.E62': {
                    'branch_lists': self.get_nodes(entity, 'CONSULTATION_NOTE.E62')
                },
                'ACTIVITY_CONSULTATION.E5': {
                    'branch_lists': self.get_nodes(entity, 'ACTIVITY_CONSULTATION.E5')
                }
            })

class RelatedFilesForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'related-files',
            'icon': 'fa-file-text-o',
            'name': _('Images and Files'),
            'class': RelatedFilesForm
        }

    def update(self, data, files):
        filedict = {}
        se = SearchEngineFactory().create()

        for name in files:
            for f in files.getlist(name):
                filedict[f.name] = f

        for newfile in data.get('new-files', []):
            resource = Resource()
            resource.entitytypeid = 'INFORMATION_RESOURCE.E73'

            resource.set_entity_value('TITLE_TYPE.E55', newfile['title_type']['value'])
            resource.set_entity_value('TITLE.E41', newfile['title'])
            if newfile.get('description') and len(newfile.get('description')) > 0:
                resource.set_entity_value('DESCRIPTION_TYPE.E55', newfile['description_type']['value'])
                resource.set_entity_value('DESCRIPTION.E62', newfile.get('description'))

            resource.set_entity_value('FILE_PATH.E62', filedict[newfile['id']])
            thumbnail = generate_thumbnail(filedict[newfile['id']])
            if thumbnail != None:
                resource.set_entity_value('THUMBNAIL.E62', thumbnail)
            resource.save()
            resource.index()

            if self.resource.entityid == '':
                self.resource.save()
            relationship = self.resource.create_resource_relationship(resource.entityid, relationship_type_id=newfile['relationshiptype']['value'])
            se.index_data(index='resource_relations', doc_type='all', body=model_to_dict(relationship), idfield='resourcexid')


        edited_file = data.get('current-files', None)
        if edited_file:
            title = ''
            title_type = ''
            description = ''
            description_type = ''
            for node in edited_file.get('nodes'):
                if node['entitytypeid'] == 'TITLE.E41':
                    title = node.get('value')
                elif node['entitytypeid'] == 'TITLE_TYPE.E55':
                    title_type = node.get('value')
                elif node['entitytypeid'] == 'DESCRIPTION.E62':
                    description = node.get('value')
                elif node['entitytypeid'] == 'DESCRIPTION_TYPE.E55':
                    description_type = node.get('value')
                elif node['entitytypeid'] == 'ARCHES_RESOURCE_CROSS-REFERENCE_RELATIONSHIP_TYPES.E55':
                    resourcexid = node.get('resourcexid')            
                    entityid1 = node.get('entityid1')
                    entityid2 = node.get('entityid2')
                    relationship = RelatedResource.objects.get(pk=resourcexid)
                    relationship.relationshiptype = node.get('value')
                    relationship.save()
                    se.delete(index='resource_relations', doc_type='all', id=resourcexid)
                    se.index_data(index='resource_relations', doc_type='all', body=model_to_dict(relationship), idfield='resourcexid')

            relatedresourceid = entityid2 if self.resource.entityid == entityid1 else entityid1
            relatedresource = Resource().get(relatedresourceid)
            relatedresource.set_entity_value('TITLE_TYPE.E55', title_type)
            relatedresource.set_entity_value('TITLE.E41', title)
            if description != '':
                relatedresource.set_entity_value('DESCRIPTION_TYPE.E55', description_type)
                relatedresource.set_entity_value('DESCRIPTION.E62', description)
            relatedresource.save()
            relatedresource.index()

        return

    def load(self, lang):
        data = []
        for relatedentity in self.resource.get_related_resources(entitytypeid='INFORMATION_RESOURCE.E73'):
            nodes = relatedentity['related_entity'].flatten()
            dummy_relationship_entity = model_to_dict(relatedentity['relationship'])
            dummy_relationship_entity['entitytypeid'] = 'ARCHES_RESOURCE_CROSS-REFERENCE_RELATIONSHIP_TYPES.E55'
            dummy_relationship_entity['value'] = dummy_relationship_entity['relationshiptype']
            dummy_relationship_entity['label'] = ''
            nodes.append(dummy_relationship_entity)
            data.append({'nodes': nodes, 'relationshiptypelabel': get_preflabel_from_valueid(relatedentity['relationship'].relationshiptype, lang)['value']})

        self.data['current-files'] = {
            'branch_lists': data,
            'domains': {
                'RELATIONSHIP_TYPES.E32': Concept().get_e55_domain('ARCHES_RESOURCE_CROSS-REFERENCE_RELATIONSHIP_TYPES.E55'),
                'TITLE_TYPE.E55': Concept().get_e55_domain('TITLE_TYPE.E55'),
                'DESCRIPTION_TYPE.E55': Concept().get_e55_domain('DESCRIPTION_TYPE.E55')
            }
        }

        return

class FileUploadForm(ResourceForm):
    @staticmethod
    def get_info():
        return {
            'id': 'file-upload',
            'icon': 'fa-file-text-o',
            'name': _('File Upload'),
            'class': FileUploadForm
        }

    def update(self, data, files):
        self.resource.prune(entitytypes=['FILE_PATH.E62', 'THUMBNAIL.E62'])
        self.resource.trim()

        if files:
            for key, value in files.items():
                self.resource.set_entity_value('FILE_PATH.E62', value)
                
                ## trying to set the file path extension node automatically here
                ext = os.path.splitext(value.name)[1]
                #self.resource.set_entity_value('FILE_PATH_EXTENSION.E62', ext)
                
                thumbnail = generate_thumbnail(value)
                if thumbnail != None:
                    self.resource.set_entity_value('THUMBNAIL.E62', thumbnail)
        return


    def load(self, lang):
    
        image_formats = ['jpg','png','tif']
        
        if self.resource:
            self.data['INFORMATION_RESOURCE.E73'] = {
                'branch_lists': self.get_nodes('INFORMATION_RESOURCE.E73'),
                'is_image': is_image(self.resource)
            }

        return   

def is_image(resource):
    for format_type in resource.find_entities_by_type_id('INFORMATION_CARRIER_FORMAT_TYPE.E55'):
        concept = Concept().get(id=format_type.value, include=['undefined'])
        for value in concept.values:
            if value.value == 'Y' and value.type == 'ViewableInBrowser':
                return True
    return False

class EvaluationForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'evaluation',
            'icon': 'fa-star-half-o',
            'name': _('Evaluations'),
            'class': EvaluationForm
        }

    def get_nodes(self, entity, entitytypeid):
        ret = []
        entities = entity.find_entities_by_type_id(entitytypeid)
        for entity in entities:
            ret.append({'nodes': entity.flatten()})

        return ret

    def update_nodes(self, entitytypeid, data):
        # self.resource.prune(entitytypes=[entitytypeid])
        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)

        for value in data[entitytypeid]:
            for newentity in value['nodes']:
                entity = Entity()
                entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                if self.baseentity == None:
                    self.baseentity = entity
                else:
                    self.baseentity.merge(entity)
        # self.resource.trim()

    def update(self, data, files):
        for value in data['EVALUATION_CRITERIA_ASSIGNMENT.E13']:
            for node in value['nodes']:
                if node['entitytypeid'] == 'EVALUATION_CRITERIA_ASSIGNMENT.E13' and node['entityid'] != '':
                    #remove the node
                    self.resource.filter(lambda entity: entity.entityid != node['entityid'])

        self.update_nodes('SIGNIFICANCE_TYPE.E55', data)
        self.update_nodes('EVALUATION_CRITERIA_TYPE.E55', data)
        self.update_nodes('ELIGIBILITY_REQUIREMENT_TYPE.E55', data)
        self.update_nodes('INTEGRITY_TYPE.E55', data)
        self.update_nodes('REASONS.E62', data)
        self.update_nodes('DATE_EVALUATED.E49', data)
        
        self.resource.merge_at(self.baseentity, self.resource.entitytypeid)
        self.resource.trim()

    def load(self, lang):

        self.data = {
            'data': [],
            'domains': {
                'SIGNIFICANCE_TYPE.E55': Concept().get_e55_domain('SIGNIFICANCE_TYPE.E55'),
                'EVALUATION_CRITERIA_TYPE.E55' : Concept().get_e55_domain('EVALUATION_CRITERIA_TYPE.E55'),
                'INTEGRITY_TYPE.E55' : Concept().get_e55_domain('INTEGRITY_TYPE.E55'),
                'ELIGIBILITY_REQUIREMENT_TYPE.E55' : Concept().get_e55_domain('ELIGIBILITY_REQUIREMENT_TYPE.E55')
            }
        }

        evaluation_assessment_entities = self.resource.find_entities_by_type_id('EVALUATION_CRITERIA_ASSIGNMENT.E13')

        for entity in evaluation_assessment_entities:
            self.data['data'].append({
                'SIGNIFICANCE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'SIGNIFICANCE_TYPE.E55')
                },
                'EVALUATION_CRITERIA_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'EVALUATION_CRITERIA_TYPE.E55')
                },
                'INTEGRITY_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'INTEGRITY_TYPE.E55')
                },
                'ELIGIBILITY_REQUIREMENT_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'ELIGIBILITY_REQUIREMENT_TYPE.E55')
                },
                'REASONS.E62': {
                    'branch_lists': self.get_nodes(entity, 'REASONS.E62')
                },
                'EVALUATION_CRITERIA_ASSIGNMENT.E13': {
                    'branch_lists': self.get_nodes(entity, 'EVALUATION_CRITERIA_ASSIGNMENT.E13')
                },
                'DATE_EVALUATED.E49': {
                    'branch_lists': self.get_nodes(entity, 'DATE_EVALUATED.E49')
                }
            })

class DistrictClassificationForm(ResourceForm):
    baseentity = None

    @staticmethod
    def get_info():
        return {
            'id': 'district_classification',
            'icon': 'fa-adjust',
            'name': _('Classifications'),
            'class': DistrictClassificationForm
        }

    def get_nodes(self, entity, entitytypeid):
        ret = []
        entities = entity.find_entities_by_type_id(entitytypeid)
        for entity in entities:
            ret.append({'nodes': entity.flatten()})

        return ret

    def update_nodes(self, entitytypeid, data):
        if self.schema == None:
            self.schema = Entity.get_mapping_schema(self.resource.entitytypeid)
        for value in data[entitytypeid]:
            for newentity in value['nodes']:
                entity = Entity()
                entity.create_from_mapping(self.resource.entitytypeid, self.schema[newentity['entitytypeid']]['steps'], newentity['entitytypeid'], newentity['value'], newentity['entityid'])

                if self.baseentity == None:
                    self.baseentity = entity
                else:
                    self.baseentity.merge(entity)

    def update(self, data, files):

        for value in data['PHASE_TYPE_ASSIGNMENT.E17']:
            for node in value['nodes']:
                if node['entitytypeid'] == 'PHASE_TYPE_ASSIGNMENT.E17' and node['entityid'] != '':
                    #remove the node
                    self.resource.filter(lambda entity: entity.entityid != node['entityid'])

        self.update_nodes('HERITAGE_RESOURCE_GROUP_TYPE.E55', data)
        self.update_nodes('TO_DATE.E49', data)
        self.update_nodes('FROM_DATE.E49', data)
        self.update_nodes('HERITAGE_RESOURCE_GROUP_USE_TYPE.E55', data)
        self.update_nodes('CULTURAL_PERIOD.E55', data)
        self.update_nodes('ANCILLARY_FEATURE_TYPE.E55', data)
        production_entities = self.resource.find_entities_by_type_id('PRODUCTION.E12')

        if len(production_entities) > 0:
            self.resource.merge_at(self.baseentity, 'PRODUCTION.E12')
        else:
            self.resource.merge_at(self.baseentity, self.resource.entitytypeid)
        self.resource.trim()
                   
    def load(self, lang):

        self.data = {
            'data': [],
            'domains': {
                'HERITAGE_RESOURCE_GROUP_TYPE.E55': Concept().get_e55_domain('HERITAGE_RESOURCE_GROUP_TYPE.E55'),
                'HERITAGE_RESOURCE_GROUP_USE_TYPE.E55' : Concept().get_e55_domain('HERITAGE_RESOURCE_GROUP_USE_TYPE.E55'),
                'CULTURAL_PERIOD.E55' : Concept().get_e55_domain('CULTURAL_PERIOD.E55'),
                'ANCILLARY_FEATURE_TYPE.E55' : Concept().get_e55_domain('ANCILLARY_FEATURE_TYPE.E55')
            }
        }

        classification_entities = self.resource.find_entities_by_type_id('PHASE_TYPE_ASSIGNMENT.E17')

        for entity in classification_entities:
            to_date_nodes = datetime_nodes_to_dates(self.get_nodes(entity, 'TO_DATE.E49'))
            from_date_nodes = datetime_nodes_to_dates(self.get_nodes(entity, 'FROM_DATE.E49'))

            self.data['data'].append({
                'HERITAGE_RESOURCE_GROUP_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'HERITAGE_RESOURCE_GROUP_TYPE.E55')
                },
                'HERITAGE_RESOURCE_GROUP_USE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'HERITAGE_RESOURCE_GROUP_USE_TYPE.E55')
                },
                'CULTURAL_PERIOD.E55': {
                    'branch_lists': self.get_nodes(entity, 'CULTURAL_PERIOD.E55')
                },
                'TO_DATE.E49': {
                    'branch_lists': to_date_nodes
                },
                'FROM_DATE.E49': {
                    'branch_lists': from_date_nodes
                },
                'ANCILLARY_FEATURE_TYPE.E55': {
                    'branch_lists': self.get_nodes(entity, 'ANCILLARY_FEATURE_TYPE.E55')
                },
                'PHASE_TYPE_ASSIGNMENT.E17': {
                    'branch_lists': self.get_nodes(entity, 'PHASE_TYPE_ASSIGNMENT.E17')
                }
            })
