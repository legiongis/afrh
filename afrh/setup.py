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
    build_auth_system()
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
    '''deprecated on 4/6/16, user creation added to build_auth_system()'''
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

def build_auth_system():
    '''builds all default AFRH-specific permissions, groups, and users'''
    
    print "\nBUILDING AFRH AUTH SYSTEM\n-----------------------"

    ## using blank model for the content type, as described in this post
    ## http://stackoverflow.com/questions/13932774/how-can-i-use-django-permissions-without-defining-a-content-type-or-model
    ## not a good long-term solution
    
    print "  creating groups...",
    group_dict = {
        'admin1':Group.objects.get_or_create(name='Admin 1')[0],
        'admin2':Group.objects.get_or_create(name='Admin 2')[0],
        'afrh_staff':Group.objects.get_or_create(name='AFRH - Staff')[0],
        'development':Group.objects.get_or_create(name='Development')[0],
    }
    print "done."

    print "  creating permissions and adding to groups...",
    # permissions = {
        # 'INVENTORY_RESOURCE':{
            # 'name':'Inventory Resource',
            # 'create':[admin1,admin2],
            # 'edit':[admin1,admin2],
            # 'fullreport':[admin1,admin2,afrh_staff],
            # 'view':[public,admin1,admin2,afrh_staff,development],
            # },
        # 'MASTER_PLAN_ZONE':{
            # 'name':'Master Plan Zone',
            # 'create':[admin1,admin2],
            # 'edit':[admin1,admin2],
            # 'fullreport':[public,admin1,admin2,afrh_staff,development],
            # 'view':[public,admin1,admin2,afrh_staff,development],
            # },
        # 'CHARACTER_AREA':{
            # 'name':'Character Area',
            # 'create':[admin1,admin2],
            # 'edit':[admin1,admin2],
            # 'fullreport':[public,admin1,admin2,afrh_staff,development],
            # 'view':[public,admin1,admin2,afrh_staff,development],
            # },
        # 'ARCHAEOLOGICAL_ZONE':{
            # 'name':'Archaeological Zone',
            # 'create':[admin1,admin2],
            # 'edit':[admin1,admin2],
            # 'fullreport':[admin1,admin2,afrh_staff],
            # 'view':[public,admin1,admin2,afrh_staff,development],
            # },
        # 'DESIGNATION':{
            # 'name':'Designation',
            # 'create':[admin1,admin2],
            # 'edit':[admin1,admin2],
            # 'fullreport':[public,admin1,admin2,afrh_staff,development],
            # 'view':[public,admin1,admin2,afrh_staff,development],
            # },
        # 'MANAGEMENT_ACTIVITY_A':{
            # 'name':'Management Activity A',
            # 'create':[admin1,admin2,afrh_staff],
            # 'edit':[admin1,admin2,afrh_staff],
            # 'fullreport':[admin1,admin2,afrh_staff],
            # 'view':[admin1,admin2,afrh_staff],
            # },
        # 'MANAGEMENT_ACTIVITY_B':{
            # 'name':'Management Activity A',
            # 'create':[admin1,admin2,development],
            # 'edit':[admin1,admin2,development],
            # 'fullreport':[admin1,admin2,afrh_staff,development],
            # 'view':[admin1,admin2,afrh_staff,development],
            # }
        # }
    
    for res, info in settings.RESOURCE_TYPE_CONFIGS().iteritems():
        cd,nm = res.split(".")[0],info['name']
        content_type = ContentType.objects.get_or_create(app_label=nm, model=cd)
        # create = Permission.objects.create(codename='create', name='Create', content_type=content_type[0])
        # edit = Permission.objects.create(codename='edit', name='Edit', content_type=content_type[0])
        # fullreport = Permission.objects.create(codename='fullreport', name='Full Report', content_type=content_type[0])
        # view = Permission.objects.create(codename='view', name='View', content_type=content_type[0])
        
        perm_dict = {
            'create':Permission.objects.create(codename='create', name='Create', content_type=content_type[0]),
            'edit':Permission.objects.create(codename='edit', name='Edit', content_type=content_type[0]),
            'fullreport':Permission.objects.create(codename='fullreport', name='Full Report', content_type=content_type[0]),
            'view':Permission.objects.create(codename='view', name='View', content_type=content_type[0])
        }
        
        for type, groups in info['permissions'].iteritems():
            if groups == 'all':
                for grp in group_dict.values():
                    grp.permissions.add(perm_dict[type])
                continue
            for group in groups:
                group_dict[group].permissions.add(perm_dict[type])
        
    
    # for res,info in permissions.iteritems():
        
        # cd,nm = res, info['name']
        # content_type = ContentType.objects.get_or_create(app_label=nm, model=cd)
        # create = Permission.objects.create(codename='create', name='Create', content_type=content_type[0])
        # edit = Permission.objects.create(codename='edit', name='Edit', content_type=content_type[0])
        # fullreport = Permission.objects.create(codename='fullreport', name='Full Report', content_type=content_type[0])
        # view = Permission.objects.create(codename='view', name='View', content_type=content_type[0])
        # for k,v in info.iteritems():
            # if k == 'create':
                # for grp in v:
                    # grp.permissions.add(create)
            # if k == 'edit':
                # for grp in v:
                    # grp.permissions.add(edit)
            # if k == 'fullreport':
                # for grp in v:
                    # grp.permissions.add(fullreport)
            # if k == 'view':
                # for grp in v:
                    # grp.permissions.add(view)
    
    content_type = ContentType.objects.get_or_create(app_label="AFRH", model="AFRH")
    rdm = Permission.objects.create(codename='rdm_access', name='RDM Access', content_type=content_type[0])
    group_dict['admin1'].permissions.add(rdm)
    print "done."
    
    print "  creating users...",
    admin1_user = User.objects.create_user("admin1","","pw")
    admin1_user.groups.add(group_dict['admin1'])
    admin2_user = User.objects.create_user("admin2","","pw")
    admin2_user.groups.add(group_dict['admin2'])
    afrh_staff_user = User.objects.create_user("afrh_staff","","pw")
    afrh_staff_user.groups.add(group_dict['afrh_staff'])
    development_user = User.objects.create_user("development","","pw")
    development_user.groups.add(group_dict['development'])
    print "done."
    print ""

    
