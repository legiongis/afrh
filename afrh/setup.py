import arches_hip.setup as setup
from arches.app.models.resource import Resource
from django.contrib.auth.models import User, Permission, ContentType, Group
from django.conf import settings

def install(path_to_source_data_dir=None):
    setup.truncate_db()
    setup.delete_index(index='concept_labels')
    setup.delete_index(index='term') 
    Resource().prepare_term_index(create=True)
    setup.load_resource_graphs()
    setup.load_authority_files(path_to_source_data_dir)
    setup.load_map_layers()
    build_permissions_and_groups()
    create_database_users()
    setup.resource_remover.truncate_resources()
    setup.delete_index(index='resource')
    setup.delete_index(index='entity')
    setup.delete_index(index='maplayers')
    setup.delete_index(index='resource_relations') 
    create_indexes()
    setup.load_resources()

def load_resource_graphs():
    setup.resource_graphs.load_graphs(break_on_error=True)

def load_authority_files(path_to_files=None):
    setup.authority_files.load_authority_files(path_to_files, break_on_error=True)

def load_resources(external_file=None):
    setup.load_resources(external_file)

def create_indexes():
    Resource().prepare_resource_relations_index(create=True)
    
    for res_config in settings.RESOURCE_TYPE_CONFIGS().values():
        Resource().prepare_search_index(res_config['resourcetypeid'], create=True)
    
def create_database_users():

    print "\nCREATING DATABASE USERS\n-----------------------"
    for user, pro in settings.EXAMPLE_USERS.iteritems():
        print user
        
        if not 'email' in pro.keys() or not 'password' in pro.keys():
            print "  user missing email or password, check settings.py"
            continue
        
        newuser = User.objects.create_user(user,pro['email'],pro['password'])
        
        if pro['superuser']:
            newuser.is_staff = True
            newuser.is_superuser = True
        if 'is_staff' in pro.keys():
            newuser.is_staff = pro['is_staff']
        if 'first_name' in pro.keys():
            newuser.first_name = pro['first_name']
        if 'last_name' in pro.keys():
            newuser.last_name = pro['last_name']

        newuser.save()

def build_permissions_and_groups():
    '''builds all AFRH-specific permissions'''
    
    print "\nBUILDING AFRH PERMISSIONS\n-----------------------"

    ## using blank model for the content type, as described in this post
    ## http://stackoverflow.com/questions/13932774/how-can-i-use-django-permissions-without-defining-a-content-type-or-model
    ## not a good long-term solution
    content_type = ContentType.objects.get_or_create(app_label="AFRH", model="AFRH")

    public = Group.objects.get_or_create(name='Public')[0]
    admin1 = Group.objects.get_or_create(name='Admin 1')[0]
    admin2 = Group.objects.get_or_create(name='Admin 2')[0]
    afrh_staff = Group.objects.get_or_create(name='AFRH - Staff')[0]
    development = Group.objects.get_or_create(name='Development')[0]

    permissions = {
        'INVENTORY_RESOURCE':{
            'name':'Inventory Resource',
            'create':[admin1,admin2],
            'edit':[admin1,admin2],
            'fullreport':[admin1,admin2,afrh_staff],
            'view':[public,admin1,admin2,afrh_staff,development],
            },
        'MASTER_PLAN_ZONE':{
            'name':'Master Plan Zone',
            'create':[admin1,admin2],
            'edit':[admin1,admin2],
            'fullreport':[public,admin1,admin2,afrh_staff,development],
            'view':[public,admin1,admin2,afrh_staff,development],
            },
        'CHARACTER_AREA':{
            'name':'Character Area',
            'create':[admin1,admin2],
            'edit':[admin1,admin2],
            'fullreport':[public,admin1,admin2,afrh_staff,development],
            'view':[public,admin1,admin2,afrh_staff,development],
            },
        'ARCHAEOLOGICAL_ZONE':{
            'name':'Archaeological Zone',
            'create':[admin1,admin2],
            'edit':[admin1,admin2],
            'fullreport':[admin1,admin2,afrh_staff],
            'view':[public,admin1,admin2,afrh_staff,development],
            },
        'DESIGNATION':{
            'name':'Designation',
            'create':[admin1,admin2],
            'edit':[admin1,admin2],
            'fullreport':[public,admin1,admin2,afrh_staff,development],
            'view':[public,admin1,admin2,afrh_staff,development],
            },
        'MANAGEMENT_ACTIVITY_A':{
            'name':'Management Activity A',
            'create':[admin1,admin2,afrh_staff],
            'edit':[admin1,admin2,afrh_staff],
            'fullreport':[admin1,admin2,afrh_staff],
            'view':[admin1,admin2,afrh_staff],
            },
        'MANAGEMENT_ACTIVITY_B':{
            'name':'Management Activity A',
            'create':[admin1,admin2,development],
            'edit':[admin1,admin2,development],
            'fullreport':[admin1,admin2,afrh_staff,development],
            'view':[admin1,admin2,afrh_staff,development],
            }
        }

    for res,info in permissions.iteritems():
        cd,nm = res, info['name']
        print nm
        create = Permission.objects.create(codename=cd+'_create', name=nm+' - Create', content_type=content_type[0])
        print "  create,",
        edit = Permission.objects.create(codename=cd+'_edit', name=nm+' - Edit', content_type=content_type[0])
        print "edit,",
        fullreport = Permission.objects.create(codename=cd+'_fullreport', name=nm+' - Full Report', content_type=content_type[0])
        print "fullreport,",
        view = Permission.objects.create(codename=cd+'_view', name=nm+' - View', content_type=content_type[0])
        print "view"
        for k,v in info.iteritems():
            if k == 'create':
                for grp in v:
                    grp.permissions.add(create)
            if k == 'edit':
                for grp in v:
                    grp.permissions.add(edit)
            if k == 'fullreport':
                for grp in v:
                    grp.permissions.add(fullreport)
            if k == 'view':
                for grp in v:
                    grp.permissions.add(view)
                    
    rdm = Permission.objects.create(codename='rdm_access', name='RDM Access', content_type=content_type[0])
    rdm_groups = [admin1,admin2,afrh_staff]
    for g in rdm_groups:
        g.permissions.add(rdm)

    
