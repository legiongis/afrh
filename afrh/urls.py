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

from arches_hip import urls as arches_hip_urls
from django.conf.urls import patterns, url, include
from views import resources

uuid_regex = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'

urlpatterns = patterns('',
    url(r'^reports/(?P<resourceid>%s)$' % uuid_regex , 'afrh.views.resources.report', name='report'),
    url(r'^rdm/(?P<conceptid>%s|())$' % uuid_regex , 'afrh.views.concept.rdm', name='rdm'),
    url(r'^concepts/(?P<conceptid>%s|())$' % uuid_regex , 'afrh.views.concept.concept', name="concept"),
    url(r'^resources/layers/(?P<entitytypeid>.*)$', 'afrh.views.resources.map_layers', name="map_layers"),
    url(r'^resources/polygon_layers/(?P<entitytypeid>.*)$', 'afrh.views.resources.polygon_layers', name="polygon_layers"),
    url(r'^resources/arch_layer/', 'afrh.views.resources.arch_layer', name="arch_layer"),
    url(r'^resources/markersHEY/(?P<entitytypeid>.*)$', 'afrh.views.resources.map_layers', {'get_centroids':True}, name="map_markers"),
    url(r'^resources/(?P<resourcetypeid>[0-9a-zA-Z_.]*)/(?P<form_id>[a-zA-Z_-]*)/(?P<resourceid>%s|())$' % uuid_regex, 'afrh.views.resources.resource_manager', name="resource_manager"),
    url(r'^resources/related/(?P<resourceid>%s|())$' % uuid_regex, 'afrh.views.resources.related_resources', name="related_resources"),
    url(r'^resources/history/(?P<resourceid>%s|())$' % uuid_regex, 'afrh.views.resources.edit_history', name="edit_history"),
    url(r'^resources/markers/(?P<entitytypeid>.*)$', 'afrh.views.resources.map_layers', {'get_centroids':True}, name="map_markers"),
    url(r'^search$', 'afrh.views.search.home_page', name="search_home"),
    url(r'^search/resources$', 'afrh.views.search.search_results', name="search_results"),
    url(r'', include(arches_hip_urls)),
    
)
