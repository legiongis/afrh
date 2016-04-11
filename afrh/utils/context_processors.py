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

import arches
import arches_hip
from django.conf import settings
from django.contrib.auth.models import Permission
from arches.app.models.resource import Resource
from afrh.models import browse
import json

def local_domain(request):
    return {
        'local_domain': settings.LOCAL_DOMAIN
    }

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

##def user_can_edit(request):
##    # check for RDM privileges
##    group_names = [i.name for i in request.user.groups.all()]
##    
##    can_rdm = False
##    if "RDM ACCESS" in group_names or request.user.is_superuser:
##        can_rdm = True
##        
##    return {
##        'user_can_edit': can_rdm
##    }

def get_versions(request):
    '''returns the currently used arches and arches-HIP versions'''
    return {
        'arches_version': arches.get_version(),
        'hip_version': arches_hip.get_version(),
    }

def user_perms(request):
    '''create a dictionary of user permissions to pass to templates'''

    permissions = request.user.get_all_permissions()

    rdm_access = False
    if "AFRH.rdm_access" in permissions:
        rdm_access = True

    perm_dict = {
        'rdm':rdm_access,
        'create':[],
        'edit':[],
        'fullreport':[],
        'view':[]
    }

    for v in settings.RESOURCE_TYPE_CONFIGS().keys():
        for p in permissions:
            t,res = p.split(".")[:2]
            if v.startswith(res):
                if t == "CREATE":
                    perm_dict['create'].append(v)
                if t == "EDIT":
                    perm_dict['edit'].append(v)
                if t == "FULLREPORT":
                    perm_dict['fullreport'].append(v)
                if t == "VIEW":
                    perm_dict['view'].append(v)

    return perm_dict

def user_groups(request):
    # need to implement proper permissions check here...
    # for now allowing all logged in users to be 'editors'
    return {
        'user_groups': request.user.groups.all()
    }

def browse_info(request):
    info = browse.get_browse_info()
    return {
        'browse_info': info
    }
