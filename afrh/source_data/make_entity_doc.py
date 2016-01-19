import os
import csv
import sys

graph_dir = r'source_data\resource_graphs'
auth_dir = r'source_data\authority_files'
out_file = os.path.join(auth_dir,"ENTITY_TYPE_X_ADOC.csv")

def check_for_authdocs(final_dict,auth_dir):
    '''make sure that all of the necessary auth docs exist'''
    missing = []
    for v in final_dict.values():
        target = os.path.join(auth_dir,v)
        if not os.path.isfile(target):
            missing.append(target)
    return missing

def get_node_ids(nodesfile):
    '''make dict of all node ids and names'''
    with open(nodesfile, "rb") as nodecsv:
        read = csv.reader(nodecsv, delimiter=",")
        read.next()
        node_ids = {row[0]:row[1] for row in read}

    return node_ids

def get_edges(edgesfile):
    '''make dict of all edge definitions'''
    with open(edgesfile, "rb") as edgecsv:
        read = csv.reader(edgecsv, delimiter=",")
        read.next()
        edges = [(row[0],row[1]) for row in read]

    return edges

def make_entity_to_adoc_dict(nodes, edges, in_dict, resourceid):
    '''make the dictionary holding all the connections'''
    errors = {}
    for k,v in edges:
        
        name, authdoc = nodes[k], nodes[v]
        if not authdoc.endswith("E32"):
            continue
        authdoc = authdoc.replace("E32","csv")

        if name in in_dict.keys() and not in_dict[name] == authdoc:
            try:
                errors[name].append(authdoc)
            except:
                errors[name] = [authdoc,in_dict[name]]
        else:
            in_dict[name] = authdoc

    # add entry for resource to resource relationship types
    # this is necessary, because it is not present in the graphs
    in_dict["ARCHES_RESOURCE_CROSS-REFERENCE_RELATIONSHIP_TYPES.E55"] = \
        "ARCHES RESOURCE CROSS-REFERENCE RELATIONSHIP TYPES.E32.csv"

    return in_dict, errors

def print_entity_x_adoc_file(authdoc_dir,input_dict):
    '''create the new entity type x adoc file'''
    sortout = input_dict.keys()
    sortout.sort()
    
    out_file = os.path.join(auth_dir,"ENTITY_TYPE_X_ADOC.csv")
    with open(out_file, "wb") as output:
        writer = csv.writer(output, delimiter=",")
        writer.writerow(["entitytype","authoritydoc","authoritydocconceptscheme"])
        
        for s in sortout:
            row = [s,input_dict[s],"PRESERVEscapes"]
            writer.writerow(row)

    return out_file                           

def print_to_log(list_errors,dict_errors):
    '''print the two error outputs to a log'''

    current_dir = os.path.dirname(sys.argv[0])
    logfile = os.path.join(current_dir,"_makeentitydoclog.txt")
    with open(logfile, "w") as log:
        print >> log, "ERROR REPORT"
        found = False
        print >> log, "  entities referencing more than one authdoc:"
        for k, v in dict_errors.iteritems():
            if len(v) > 1:
                found = True
                print >> log, "   ", k
                for i in v:
                    print >> log, "     ", i
        if not found:
            print >> log, "    none"

        print >> log, "  missing authority documents:"
        if len(list_errors) > 0:
            for d in list_errors:
                print >> log, "   ", d 
        else:
            print >> log, "    none"

    print "output stored in log:\n{0}".format(logfile)
    return logfile
        

# process all graph files
final_dict = {}
for f in os.listdir(graph_dir):

    if not f.endswith("nodes.csv"):
        continue
    resourcetype = f[:-10]

    nodesfile = os.path.join(graph_dir,f)
    edgesfile = os.path.join(graph_dir,f.replace("nodes","edges"))

    node_ids = get_node_ids(nodesfile)
    edges = get_edges(edgesfile)

    final_dict, errors = make_entity_to_adoc_dict(node_ids,edges,final_dict,resourcetype)
    
    missing_docs = check_for_authdocs(final_dict,auth_dir)

    print_entity_x_adoc_file(auth_dir,final_dict)

logpath = print_to_log(missing_docs, errors)
os.startfile(logpath)

