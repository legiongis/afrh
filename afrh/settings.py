import os
import inspect
from arches_hip.settings import *
from django.utils.translation import ugettext as _

PACKAGE_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PACKAGE_NAME = PACKAGE_ROOT.split(os.sep)[-1]
DATABASES['default']['NAME'] = 'arches_%s' % (PACKAGE_NAME)

ROOT_URLCONF = '%s.urls' % (PACKAGE_NAME)

INSTALLED_APPS = INSTALLED_APPS + (PACKAGE_NAME,)
STATICFILES_DIRS = (os.path.join(PACKAGE_ROOT, 'media'),) + STATICFILES_DIRS
TEMPLATE_DIRS = (os.path.join(PACKAGE_ROOT, 'templates'),os.path.join(PACKAGE_ROOT, 'templatetags')) + TEMPLATE_DIRS

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT =  os.path.join(PACKAGE_ROOT, 'uploadedfiles')

DEFAULT_MAP_X = -8572820
DEFAULT_MAP_Y = 4712543
DEFAULT_MAP_ZOOM = 15
# MAP_MIN_ZOOM = 9
MAP_MAX_ZOOM = 20
# MAP_EXTENT = '-13228037.69691764,3981296.0184014924,-13123624.71628009,4080358.407059081'

RESOURCE_MODEL = {'default': '{}.models.resource.Resource'.format(PACKAGE_NAME)}

## use the default arches validator so non-Arches-HIP resources can load
PACKAGE_VALIDATOR = "arches.app.utils.mock_package_validator"

LOCAL_DOMAIN = "afrh.adamcfcox.com"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    '{}.utils.context_processors.livereload'.format(PACKAGE_NAME),
    '{}.utils.context_processors.resource_types'.format(PACKAGE_NAME),
    '{}.utils.context_processors.map_info'.format(PACKAGE_NAME),
    '{}.utils.context_processors.app_settings'.format(PACKAGE_NAME),
    '{}.utils.context_processors.user_permissions'.format(PACKAGE_NAME),
    '{}.utils.context_processors.user_groups'.format(PACKAGE_NAME),
    '{}.utils.context_processors.get_versions'.format(PACKAGE_NAME),
    '{}.utils.context_processors.browse_info'.format(PACKAGE_NAME),
    '{}.utils.context_processors.local_domain'.format(PACKAGE_NAME),
)


def RESOURCE_TYPE_CONFIGS():
    return { 
        'INVENTORY_RESOURCE.E18': {
            'resourcetypeid': 'INVENTORY_RESOURCE.E18',
            'name': _('Inventory Resource'),
            'icon_class': 'fa fa-university',
            'default_page': 'inventory-summary',
            'default_description': 'No description available',
            'description_node': _('DESCRIPTION.E62'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#fa6003',
            'stroke_color': '#fb8c49',
            'fill_color': '#ffc29e',
            'primary_name_lookup': {
                'entity_type': 'NAME.E41',
                'lookup_value': 'Current'
            },
            'sort_order': 1
        },
        'HERITAGE_RESOURCE_GROUP.E27': {
            'resourcetypeid': 'HERITAGE_RESOURCE_GROUP.E27',
            'name': _('Historic Area'),
            'icon_class': 'fa fa-th',
            'default_page': 'area-summary',
            'default_description': 'No description available',
            'description_node': _('REASONS.E62'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#FFC53D',
            'stroke_color': '#d9b562',
            'fill_color': '#eedbad',
            'primary_name_lookup': {
                'entity_type': 'NAME.E41',
                'lookup_value': 'Primary'
            },
            'sort_order': 2
        },
        'ACTIVITY.E7': {
            'resourcetypeid': 'ACTIVITY.E7',
            'name': _('Activity'),
            'icon_class': 'fa fa-tasks',
            'default_page': 'activity-summary',
            'default_description': 'No description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#6DC3FC',
            'stroke_color': '#88bde0',
            'fill_color': '#afcce1',
            'primary_name_lookup': {
                'entity_type': 'NAME.E41',
                'lookup_value': 'Primary'
            },
            'sort_order': 3
        },
##        'HISTORICAL_EVENT.E5':{
##            'resourcetypeid': 'HISTORICAL_EVENT.E5',
##            'name': _('Historic Event'),
##            'icon_class': 'fa fa-calendar',
##            'default_page': 'historical-event-summary',
##            'default_description': 'No description available',
##            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
##            'categories': [_('Resource')],
##            'has_layer': True,
##            'on_map': False,
##            'marker_color': '#4EBF41',
##            'stroke_color': '#61a659',
##            'fill_color': '#c2d8bf',
##            'primary_name_lookup': {
##                'entity_type': 'NAME.E41',
##                'lookup_value': 'Primary'
##            },
##            'sort_order': 4
##        },
        'ACTOR.E39': {
            'resourcetypeid': 'ACTOR.E39',
            'name': _('Person/Organization'),
            'icon_class': 'fa fa-group',
            'default_page': 'actor-summary',
            'default_description': 'No description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#a44b0f',
            'stroke_color': '#a7673d',
            'fill_color': '#c8b2a3',
            'primary_name_lookup': {
                'entity_type': 'ACTOR_APPELLATION.E82',
                'lookup_value': 'Primary'
            },
            'sort_order': 5
        },
        'INFORMATION_RESOURCE.E73': {
            'resourcetypeid': 'INFORMATION_RESOURCE.E73',
            'name': _('Information Resource'),
            'icon_class': 'fa fa-file-text-o',
            'default_page': 'information-resource-summary',
            'default_description': 'No description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': False,
            'marker_color': '#8D45F8',
            'stroke_color': '#9367d5',
            'fill_color': '#c3b5d8',
            'primary_name_lookup': {
                'entity_type': 'TITLE.E41',
                'lookup_value': 'Primary'
            },
            'sort_order': 6
        }
    }

#GEOCODING_PROVIDER = ''

RESOURCE_GRAPH_LOCATIONS = (
#     # Put strings here, like "/home/data/resource_graphs" or "C:/data/resource_graphs".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
     os.path.join(PACKAGE_ROOT, 'source_data', 'resource_graphs'),
)

CONCEPT_SCHEME_LOCATIONS = (
    # Put strings here, like "/home/data/authority_files" or "C:/data/authority_files".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
    #'absolute/path/to/authority_files',
    os.path.join(PACKAGE_ROOT, 'source_data', 'concepts', 'authority_files'),
)

BUSISNESS_DATA_FILES = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.normpath(os.path.join(PACKAGE_ROOT, 'source_data', 'business_data', 'sample.arches')),
)

APP_NAME = 'AFRH Arches v3'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PACKAGE_ROOT, 'logs', 'application.txt'),
        },
    },
    'loggers': {
        'arches': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'afrh_app1': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

#EXPORT_CONFIG = os.path.normpath(os.path.join(PACKAGE_ROOT, 'source_data', 'business_data', 'resource_export_mappings.json'))

try:
    from settings_local import *
except ImportError:
    pass
