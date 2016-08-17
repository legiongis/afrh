# background

Arches v3 package in development by Legion GIS, LLC for PRESERVE/scapes and the Armed Forces Retirement Home - Washington.

currently hosted here: [afrh.legiongis.com](http://afrh.legiongis.com)

# features

The Armed Forces Retirement Home - Washington implementation of Arches is based on the default Arches-HIP app, but has many customizations and extra abilities. These features have been been created in collaboration with [PRESERVE/scapes](http://www.preservescapes.com), the cultural resource management firm that currently manages the AFRH-W historic resources.

## Resource Types

The AFRH database comprises the following ten resource types:

+ *Inventory Resource* The 250 historic resources (buildings, sites, objects) managed by the AFRH-W.
+ *Character Area* The character defining areas throughout the grounds
+ *Historic Area* Designated historic areas of the grounds
+ *Master Plan Zone* Management zones as defined in the AFRH-W master plan
+ *Archaeological Zone* Archaeological Zones as defined in the AFRH-W development plan
+ *Field Investigation* Shovel tests carried out during development projects
+ *Person/Organization* The 32 builders, architects, designers that are related to the Inventory Resources
+ *Information Resource* Photos, documents, architectural drawings
+ *Management Activity A* (see below)
+ *Management Activity B* (see below)

These resource types were designed not only to faithfully reflect the existing resource database, but also to model how the AFRH-W resources will be best managed in the future. The addition of the Management Activities, especially, allows for many former project tracking methods to now be combined into a single system.

## Management Activities

Two resource types - Management Activity A and Management Activity B - were designed to track and manage development projects that take place throughout the grounds. This allows for the creation of a "resource" in the database for a development project, like a golf hole relocation. Records of official reviews (ARPA, NEPA, Section 106...), project boundaries, consultations, points of contact, etc. can all be attached to this Management Activity resource. In turn, the Management Activity can be related to any other database resource.

## General Redesign and Layout

Given that the resource graphs were more or less completely recreated, we took the opportunity to do an overhaul on the forms and reports.

### Forms

All of the input forms have been redesigned with a new standardized layout. Also, new validation functions, isValidDate() and nodesHaveValues() were placed in a centralized location, in order to easily apply them to any branch in any form.

### Reports

The reports have been separated into collapsible sections, which seemed necessary given the potential length of reports for the more complex resources. The related resource graph was also added to the report template.

## Map Vector Display

To better reflect the new resource types, significant expansions were made to the vector display of resources on the map. In the case of the "area" resources, a polygon is now used instead of a centroid. In the case of Archaeological Zones, which have not only a boundary but also up to four different types of "Areas of Probability". These are all displayed with different symbols, and a legend is included in the layer info box.

## Historic Map Overlays

12 historic maps of the AFRH-W grounds, provided by PRESERVE/scapes as high-resolution scans, have been georeferenced and published as Web Map Services (WMS) through GeoServer. They have been incorporated as a separate type of overlay available in all of the map interfaces in this app. A user can turn on and change the transparency of an number of these layers.  The historic maps always appear between the basemap and any resource geometry layers.

## AFRH Permissions System

Following requests from the AFRH, an implementation-specific permission system has been created. However, it has been done so in a granular manner that should allow easy conversion to meet completely different needs.

The main set of permissions is managed on a resource type basis. A standard set of Permission ojects are created per resource type, and then assigned to specific Group objects as necessary. Thus, a new user can be created as part of a preset group, thereby gaining a number of preset individual permissions, but can also have individual permissions added. The creation of all permissions and groups is handled in setup.py (as well as the prior removal of the default Arches-HIP permissions and groups), and the assignment of a resource type's subset permissions to a specific group is defined as a new key/value pair in settings.RESOURCE_TYPE_CONFIGS().

A more specific configuration was added to allow any given Information Resource to be hidden from the public (i.e. any 'anonymous' user). This is based on the value of a single node in the Information Resource graph. In other words, it implemented completely outside of the built-in Django admin framework system.

### Permission Objects

For each resource type, CREATE, EDIT, FULLREPORT, and VIEW. CREATE and EDIT are self-explanatory. FULLREPORT means that the user will view an unfiltered report for resources of a certain type, and if a user lacks VIEW permission, the resource type will be screened from 1. the map view, 2. search results, and 3. related resource graphs.

Therefore, the list of all available permissions looks something like this:

CREATE | Inventory Resource
CREATE | Actor
..etc

An additional permission object called "AFRH | RDM Access" gives users access to the Reference Data Manager.

### Permission Groups

The app has the following permission groups:

+ *admin1*
+ *admin2*
+ *afrh_staff*
+ *afrh_volunteer*
+ *development*

Each group is automatically assigned specific permissions, as defined in settings.RESOURCE_TYPE_CONFIGS(). During the install of this app, a sample user is made for each group, whose name and password are one of the groups listed above.

A full summary of the permissions are shown in the table below.

| Group | RDM | Inventory Resource - CREATE | EDIT | FULLREPORT | VIEW | Character Area - CREATE | EDIT | FULLREPORT | VIEW |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| admin1 | yes | yes | yes | yes | yes | yes | x | *x* | &#10004; |



|Group Name|RDM|Inventory Resources||||Master Plan Zones||||Character Areas||||Archaeological Zones||||Designations||||Management Activities A||||Management Activities B||||Information Resources|
||Add|Edit|Report|See/Search|Add|Edit|Report|See/Search|Add|Edit|Report|See/Search|Add|Edit|Report|See/Search|Add|Edit|Report|See/Search|Add|Edit|Report|See/Search|Add|Edit|Report|See/Search|Add|Edit
Public|No|No|No|Yes - Filtered|Yes|No|No|Yes - All|Yes|No|No|Yes - All|Yes|No|No|Yes - Filtered|Yes|No|No|Yes - All|Yes|No|No|No|No|No|No|No|No|No|No
Admin 1|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes
Admin 2|No|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes|Yes - All|Yes|Yes|Yes
AFRH - STAFF|No|No|No|Yes - All|Yes|No|No|Yes - All|Yes|No|No|Yes - All|Yes|No|No|Yes - All|Yes|No|No|Yes - All|Yes|Yes|Yes|Yes - All|Yes|No|No|Yes - All|Yes|Yes|Yes
AFRH - VOL|No|No|No|Yes - Filtered|Yes|No|No|Yes - All|Yes|No|No|Yes - All|Yes|No|No|Yes - Filtered|Yes|No|No|Yes - All|Yes|No|No|No|No|No|No|No|No|Yes|Yes
Development|No|No|No|Yes - Filtered|Yes|No|No|Yes - All|Yes|No|No|Yes - All|Yes|No|No|Yes - Filtered|Yes|No|No|Yes - All|Yes|No|No|No|No|Yes|Yes|Yes - All|Yes|No|No

## Database Browsing

The original Saved Searches utility was replaced with a basic capacity to "browse" the database. On the main SEARCH page, the user is able view the potential values for nine predefined attributes. For example, you may choose from a list of all possible Areas of Significance in order to use that search term. The motivation for this was to allow people to explore the database without having to know what terms they were looking for ahead of time.

This component of the AFRH-W app is pretty rough, and could certainly be streamlined in the future.
