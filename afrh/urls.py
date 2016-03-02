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
    url(r'', include(arches_hip_urls)),
    url(r'^newmap', 'afrh.views.newmap.get_page', name="newmap"),
    url(r'^resources/layers/(?P<entitytypeid>.*)$', resources.map_layers, name="map_layers"),
    url(r'^resources/markers/(?P<entitytypeid>.*)$', resources.map_layers, name="map_markers"),
)
