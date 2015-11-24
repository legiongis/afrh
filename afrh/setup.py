import arches_hip.setup as setup
from arches.app.models.resource import Resource

def install(path_to_source_data_dir=None):
    setup.truncate_db()
    
    setup.delete_index(index='concept_labels')
    setup.delete_index(index='term') 
    Resource().prepare_term_index(create=True)

    setup.load_resource_graphs()
    setup.load_authority_files(path_to_source_data_dir)
    setup.load_map_layers()

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
    Resource().prepare_search_index('HERITAGE_RESOURCE_GROUP.E27', create=True)
    Resource().prepare_search_index('INVENTORY_RESOURCE.E18', create=True)
    Resource().prepare_search_index('INFORMATION_RESOURCE.E73', create=True)
    Resource().prepare_search_index('ACTIVITY.E7', create=True)
    Resource().prepare_search_index('ACTOR.E39', create=True)
    #Resource().prepare_search_index('HISTORICAL_EVENT.E5', create=True)

