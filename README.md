# afrh
arches v3 package in development for the armed forces retirement home.

currently hosted here: [afrh.legiongis.com](http://afrh.legiongis.com)

# features

The Armed Forces Retirement Home - Washington implementation of Arches is based on the default Arches-HIP app, but has many customizations and add-ons.

## Historic Map Overlays

12 historic maps of the AFRH-W grounds, provided by PRESERVE/scapes as high-resolution scans, have been georeferenced and published as Web Map Services (WMS) through GeoServer. They have been incorporated as a separate type of overlay available in all of the map interfaces in this app. A user can turn on and change the transparency of an number of these layers.  The historic maps always appear between the basemap and any resource geometry layers.

## Permissions

Following requests from the AFRH, an implementation-specific permission system has been created. However, it has been done so in a granular manner that should allow easy conversion to a completely different system.

The main set of permissions is managed on a resource type basis. A standard set of Permission ojects are created per resource type, and then assigned to specific Group objects as necessary. Thus, a new user can be created as part of a preset group, thereby gaining a number of preset individual permissions, but can also have individual permissions added. The creation of all permissions and groups is handled in setup.py (as well as the prior removal of the default Arches-HIP permissions and groups), and the assignment of a resource type's subset permissions to a specific group is defined as a new key/value pair in settings.RESOURCE_TYPE_CONFIGS().

A more specific configuration was added to allow any given Information Resource to be hidden from the public (i.e. any anonymous user). This is based on the value of a single node in the Information Resource graph, in other words, outside of the actual Django admin system.

### Permission Objects

For each resource type, CREATE, EDIT, FULLREPORT, and VIEW. CREATE and EDIT are self-explanatory. FULLREPORT means that the user will view an unfiltered report for resources of a certain type, and VIEW means that the resource type will show up at all on the map view, in search results, and in related resource graphs. Therefore, the list of all available permissions looks something like this:

CREATE | Inventory Resource
CREATE | Actor
..etc

An additional permission object called "AFRH | RDM Access" gives users access to the Reference Data Manager.

### Permission Groups

The app has the following permission groups: Admin 1, Admin 2, AFRH - Staff, AFRH - Volunteer, Development. Each group is automatically assigned specific permissions, as defined in settings.RESOURCE_TYPE_CONFIGS(). For example, 
