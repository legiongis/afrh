import os
import csv
import sys

graph_dir = r'resource_graphs'
auth_dir = r'concepts\authority_files'
out_file = os.path.join(auth_dir,"ENTITY_TYPE_X_ADOC.csv")
concept_scheme_name = "PRESERVEscapes"

def check_for_authdocs(final_dict,auth_dir):
    '''make sure that all of the necessary auth docs exist, and find any
unnecessary ones.'''
    missing = []
    for v in final_dict.values():
        target = os.path.join(auth_dir,v)
        if not os.path.isfile(target):
            missing.append(target)

    unused = []
    for f in os.listdir(auth_dir):
        if f == "ENTITY_TYPE_X_ADOC.csv":
            continue
        if not f.endswith(".csv"):
            continue
        ## not 100% confident on the .values testing right now.
        if f.endswith(".values.csv"):
            f_auth = os.path.join(auth_dir,f.replace(".values",""))
            if not os.path.isfile(f_auth):
                unused.append(f)
            continue
        if not f in final_dict.values():
            unused.append(f)
            
    missing.sort()
    unused.sort()
    
    return missing, unused

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

def print_entity_x_adoc_file(authdoc_dir,input_dict,scheme_name):
    '''create the new entity type x adoc file'''
    sortout = input_dict.keys()
    sortout.sort()
    
    out_file = os.path.join(auth_dir,"ENTITY_TYPE_X_ADOC.csv")
    with open(out_file, "wb") as output:
        writer = csv.writer(output, delimiter=",")
        writer.writerow(["entitytype","authoritydoc","authoritydocconceptscheme"])
        
        for s in sortout:
            row = [s,input_dict[s],scheme_name]
            writer.writerow(row)

    return out_file                           

def print_to_log(dict_errors,missing=[],extra=[]):
    '''print the two error outputs to a log'''

    current_dir = os.path.dirname(sys.argv[0])
    logfile = os.path.join(current_dir,"_makeentitydoc.log")
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
        if len(missing) > 0:
            for d in missing:
                print >> log, "   ", d 
        else:
            print >> log, "    none"

        print >> log, "  unused authority documents:"
        if len(extra) > 0:
            for d in extra:
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
    
    missing_docs,unused_docs = check_for_authdocs(final_dict,auth_dir)

    print_entity_x_adoc_file(auth_dir,final_dict,concept_scheme_name)

logpath = print_to_log(errors,missing_docs,unused_docs)
os.startfile(logpath)

