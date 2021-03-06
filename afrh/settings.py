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

DEBUG = False
ALLOWED_HOSTS = ['*'] # also acceptable is ['.domain.com']

# Map settings
# settings to focus on Washington DC campus
DEFAULT_MAP_X = -8572925
DEFAULT_MAP_Y = 4712723
DEFAULT_MAP_ZOOM = 15

# settings to include Gulfport campus
# DEFAULT_MAP_X = -9231513
# DEFAULT_MAP_Y = 4101543
# DEFAULT_MAP_ZOOM = 6

MAP_MAX_ZOOM = 20
# MAP_EXTENT = '-13228037.69691764,3981296.0184014924,-13123624.71628009,4080358.407059081'

ANALYSIS_COORDINATE_SYSTEM_SRID = 32618

RESOURCE_MODEL = {'default': '{}.models.resource.Resource'.format(PACKAGE_NAME)}

## change to the default arches validator so non-Arches-HIP resources can load
PACKAGE_VALIDATOR = "arches.app.utils.mock_package_validator"

LOCAL_DOMAIN = "www.afrh-iris.com"

SEARCH_ITEMS_PER_PAGE = 10
SEARCH_EXPORT_ITEMS_PER_PAGE = 1000000

## add setting for system-wide node name that stores the protection level concepts
PROTECTION_LEVEL_NODE = "PROTECTION_LEVEL.E55"

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
    '{}.utils.context_processors.user_perms'.format(PACKAGE_NAME),
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
            'default_description': 'no description available',
            'description_node': _('DESCRIPTION.E62'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#C4171D',
            'stroke_color': '#C4171D',
            'fill_color': '#C4171D',
            'primary_name_lookup': {
                'entity_type': 'NAME.E41',
                'lookup_value': ('NAME_TYPE.E55','Current Primary')
            },
            'sort_order': 1,
            'show_polygons':True,
            'layer_model': 'marker',
            'permissions': {
                'create':['admin1','admin2'],
                'edit':['admin1','admin2'],
                'fullreport':['admin1','admin2','afrh_staff'],
                'view':'all'
                }
        },
        'CHARACTER_AREA.E53': {
            'resourcetypeid': 'CHARACTER_AREA.E53',
            'name': _('Character Area'),
            'icon_class': 'fa fa-th',
            'default_page': 'char-area-summary',
            'default_description': 'no description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#FF2D9D',
            'stroke_color': '#FF2D9D',
            'fill_color': '#FF2D9D',
            'primary_name_lookup': {
                'entity_type': 'NAME.E48',
                'lookup_value': False
            },
            'sort_order': 2,
            'layer_model': 'area',
            'permissions': {
                'create':['admin1','admin2'],
                'edit':['admin1','admin2'],
                'fullreport':'all',
                'view':'all'
                }
        },
        'HISTORIC_AREA.E53': {
            'resourcetypeid': 'HISTORIC_AREA.E53',
            'name': _('Historic Area'),
            'icon_class': 'fa fa-flag',
            'default_page': 'des-summary',
            'default_description': 'no description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#8D45F8',
            'stroke_color': '#9367d5',
            'fill_color': '#c3b5d8',
            'primary_name_lookup': {
                'entity_type': 'HISTORIC_AREA_NAME.E48',
                'lookup_value': False
            },
            'sort_order': 3,
            'layer_model': 'area',
            'permissions': {
                'create':['admin1','admin2'],
                'edit':['admin1','admin2'],
                'fullreport':'all',
                'view':'all'
                }
        },
        'MASTER_PLAN_ZONE.E53': {
            'resourcetypeid': 'MASTER_PLAN_ZONE.E53',
            'name': _('Master Plan Zone'),
            'icon_class': 'fa fa-th-large',
            'default_page': 'mpz-summary',
            'default_description': 'no description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#009DFF',
            'stroke_color': '#009DFF',
            'fill_color': '#009DFF',
            'primary_name_lookup': {
                'entity_type': 'NAME.E48',
                'lookup_value': False
            },
            'sort_order': 4,
            'layer_model': 'area',
            'permissions': {
                'create':['admin1','admin2'],
                'edit':['admin1','admin2'],
                'fullreport':'all',
                'view':'all'
                }
        },
        'ARCHAEOLOGICAL_ZONE.E53': {
            'resourcetypeid': 'ARCHAEOLOGICAL_ZONE.E53',
            'name': _('Archaeological Zone'),
            'icon_class': 'fa fa-list',
            'default_page': 'arch-summary',
            'default_description': 'no description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#00FF00',
            'stroke_color': '#00FF00',
            'fill_color': '#00FF00',
            'primary_name_lookup': {
                'entity_type': 'ARCHAEOLOGICAL_ZONE_NAME.E48',
                'lookup_value': False
            },
            'sort_order': 5,
            'layer_model': 'arch',
            'permissions': {
                'create':['admin1','admin2'],
                'edit':['admin1','admin2'],
                'fullreport':['admin1','admin2','afrh_staff'],
                'view':'all'
                }
        },
        'FIELD_INVESTIGATION.E7': {
            'resourcetypeid': 'FIELD_INVESTIGATION.E7',
            'name': _('Field Investigation'),
            'icon_class': 'fa fa-tag',
            'default_page': 'invest-summary',
            'default_description': 'no description available',
            'description_node': _('INVESTIGATION_DESCRIPTION_E62'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#000000',
            'stroke_color': '#000000',
            'fill_color': '#000000',
            'primary_name_lookup': {
                'entity_type': 'INVESTIGATION_ASSESSMENT.E55',
                'lookup_value': False
            },
            'sort_order': 6,
            'layer_model': 'point',
            'permissions': {
                'create':['admin1','admin2'],
                'edit':['admin1','admin2'],
                'fullreport':['admin1','admin2','afrh_staff'],
                'view':'all'
                }
        },
        'ACTOR.E39': {
            'resourcetypeid': 'ACTOR.E39',
            'name': _('Person/Organization'),
            'icon_class': 'fa fa-user',
            'default_page': 'actor-summary',
            'default_description': 'no description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': False,
            'on_map': True,
            'marker_color': '#a44b0f',
            'stroke_color': '#a7673d',
            'fill_color': '#c8b2a3',
            'primary_name_lookup': {
                'entity_type': 'ACTOR_APPELLATION.E82',
                'lookup_value': ('ACTOR_NAME_TYPE.E55','Primary')
            },
            'sort_order': 7,
            'permissions': {
                'create':['admin1','admin2'],
                'edit':['admin1','admin2'],
                'fullreport':'all',
                'view':'all'
                }
        },
        'INFORMATION_RESOURCE.E73': {
            'resourcetypeid': 'INFORMATION_RESOURCE.E73',
            'name': _('Information Resource'),
            'icon_class': 'fa fa-file-text-o',
            'default_page': 'information-resource-summary',
            'default_description': 'no description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#8D45F8',
            'stroke_color': '#9367d5',
            'fill_color': '#c3b5d8',
            'primary_name_lookup': {
                'entity_type': 'TITLE.E41',
                'lookup_value': ('TITLE_TYPE.E55','Primary')
            },
            'sort_order': 8,
            'layer_model': 'marker',
            'permissions': {
                'create':['admin1','admin2','afrh_volunteer'],
                'edit':['admin1','admin2','afrh_volunteer'],
                'fullreport':'all',
                'view':'all'
                }
        },
        'ACTIVITY_A.E7': {
            'resourcetypeid': 'ACTIVITY_A.E7',
            'name': _('Management Activity (A)'),
            'icon_class': 'fa fa-clipboard',
            'default_page': 'activity-summary',
            'default_description': 'no description available',
            'description_node': _('INSERT RESOURCE DESCRIPTION NODE HERE'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#a44b0f',
            'stroke_color': '#a7673d',
            'fill_color': '#c8b2a3',
            'primary_name_lookup': {
                'entity_type': 'ACTIVITY_NAME.E41',
                'lookup_value': False
            },
            'sort_order': 9,
            'layer_model': 'act-a',
            'restricted': True,
            'permissions': {
                'create':['admin1','admin2','afrh_staff'],
                'edit':['admin1','admin2','afrh_staff'],
                'fullreport':['admin1','admin2','afrh_staff'],
                'view':['admin1','admin2','afrh_staff']
                }
        },
        'ACTIVITY_B.E7': {
            'resourcetypeid': 'ACTIVITY_B.E7',
            'name': _('Management Activity (B)'),
            'icon_class': 'fa fa-clipboard',
            'default_page': 'activity-summary',
            'default_description': 'no description available',
            'description_node': _('ACTIVITY_SCOPE_OF_WORK_DESCRIPTION.E62'),
            'categories': [_('Resource')],
            'has_layer': True,
            'on_map': True,
            'marker_color': '#69310b',
            'stroke_color': '#69310b',
            'fill_color': '#69310b',
            'primary_name_lookup': {
                'entity_type': 'ACTIVITY_NAME.E41',
                'lookup_value': False
            },
            'sort_order': 10,
            'layer_model': 'area',
            'restricted': True,
            'permissions': {
                'create':['admin1','admin2','development'],
                'edit':['admin1','admin2','development'],
                'fullreport':['admin1','admin2','afrh_staff','development'],
                'view':['admin1','admin2','afrh_staff','development']
                }
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

APP_NAME = 'AFRH-IRIS'

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
