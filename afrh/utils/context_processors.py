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
from arches.app.models.resource import Resource

def livereload(request):
    return {
        'livereload_port': settings.LIVERELOAD_PORT
    }

def map_info(request):
    return {
        'map_info': {
            'x': settings.DEFAULT_MAP_X,
            'y': settings.DEFAULT_MAP_Y,
            'zoom': settings.DEFAULT_MAP_ZOOM,
            'bing_key': settings.BING_KEY,
            'map_min_zoom': settings.MAP_MIN_ZOOM,
            'map_max_zoom': settings.MAP_MAX_ZOOM,
            'extent': settings.MAP_EXTENT,
            'resource_marker_icon': settings.RESOURCE_MARKER_ICON_UNICODE,
            'resource_marker_font': settings.RESOURCE_MARKER_ICON_FONT,
            'resource_marker_color': settings.RESOURCE_MARKER_DEFAULT_COLOR
        }
    }

def resource_types(request):
    sorted_resource_types = sorted(settings.RESOURCE_TYPE_CONFIGS().items(), key=lambda v: v[1]['sort_order'])
    return {
        'resource_types': sorted_resource_types
    }

def app_settings(request):
    return {
        'APP_NAME': settings.APP_NAME,
        'GOOGLE_ANALYTICS_TRACKING_ID': settings.GOOGLE_ANALYTICS_TRACKING_ID
    }

def user_can_edit(request):
    # check for RDM privileges
    group_names = [i.name for i in request.user.groups.all()]
    
    can_rdm = False
    if "RDM ACCESS" in group_names or request.user.is_superuser:
        can_rdm = True
        
    return {
        'user_can_edit': can_rdm
    }

def user_permissions(request):
    '''defines all user permissions'''
    
    # get all group names for user
    group_names = [i.name for i in request.user.groups.all()]
    resource_types = [v['name'] for v in settings.RESOURCE_TYPE_CONFIGS().values()]

    # these are the entities that a user is allowed to edit
    user_can_edit = False
    entities_allowed = [i for i in group_names if i in resource_types]
    if len(entities_allowed) > 0:
        user_can_edit = True
    
    # check whether user can create new resources
    can_create = False
    if "DATA CREATORS" in group_names:
        can_create = True

    # if user is part of the data creators group, they can create new resources
    rdm_access = False
    if "RDM ACCESS" in group_names:
        rdm_access = True

    # give superuser all access
    if request.user.is_superuser:
        rdm_access = True
        user_can_edit = True
        can_create = True
        entities_allowed = resource_types

    return {
        'user_can_edit': user_can_edit,
        'user_permissions': {
            'can_rdm': rdm_access,
            'can_create': can_create,
            'entities_allowed': entities_allowed
        }
    }

def user_groups(request):
    # need to implement proper permissions check here...
    # for now allowing all logged in users to be 'editors'
    return {
        'user_groups': request.user.groups.all()
    }
