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
    build_auth_system_2()
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
    
    print "\nREMOVING ARCHES-HIP PERMISSIONS & GROUPS\n-----------------------"
    all_perms = Permission.objects.filter()
    for p in all_perms:
        p.delete()
    print "  {} permissions removed".format(len(all_perms))
    
    all_groups = Group.objects.filter()
    for g in all_groups:
        g.delete()
    print "  {} groups removed".format(len(all_groups))
    
    print "\nBUILDING AFRH AUTH SYSTEM\n-----------------------"

    ## using blank model for the content type, as described in this post, maybe not a good long-term solution
    ## http://stackoverflow.com/questions/13932774/how-can-i-use-django-permissions-without-defining-a-content-type-or-model
    
    print "  creating groups...",
    group_dict = {
        'admin1':Group.objects.get_or_create(name='Admin 1')[0],
        'admin2':Group.objects.get_or_create(name='Admin 2')[0],
        'afrh_staff':Group.objects.get_or_create(name='AFRH - Staff')[0],
        'development':Group.objects.get_or_create(name='Development')[0],
    }
    print "done."

    print "  creating permissions and adding to groups...",
    perm_types = ['create','edit','fullreport','view']
    
    for perm in perm_types:
        content_type = ContentType.objects.get_or_create(app_label=perm.upper(), model=perm)
        for res, info in settings.RESOURCE_TYPE_CONFIGS().iteritems():
            cd,nm = res.split(".")[0],info['name']
            this_perm = Permission.objects.create(codename=cd, name=nm, content_type=content_type[0])
            
            for type, groups in info['permissions'].iteritems():
                if type == perm:
                    if groups == 'all':
                        for grp in group_dict.values():
                            grp.permissions.add(this_perm)
                        continue
                    for group in groups:
                        group_dict[group].permissions.add(this_perm)

    content_type = ContentType.objects.get_or_create(app_label="AFRH", model="afrh")
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
    
