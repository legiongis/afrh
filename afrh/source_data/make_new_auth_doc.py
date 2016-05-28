import os
import csv

out_dir = 'concepts/authority_files'

def get_entries():
    '''collects all of the concepts to be entered in the doc'''
    print "enter PrefLabels in order. type 'done' when finished"
    concepts = []
    
    while True:
        label = raw_input("  >>")
        if label == "done":
            break
        else:
            concepts.append(label)

    yes = raw_input("  use these values? (y/n) ").lower()
    if not yes.startswith("y"):
        concepts = []
        
    return concepts

def get_info():
    '''collects raw input'''
    while True:
        name = raw_input("enter new authority doc name >> ").upper()+"_AUTHORITY_DOCUMENT.csv"
        print name
        yes = raw_input("  confirm (y/n) ").lower()
        if yes.startswith("y"):
            break

    values = True
    val_con = raw_input("\ninclude .values file? (y/n) >> ").lower()
    if val_con.startswith("y"):
        values = True

    while True:
        conceptid = raw_input("\nenter concept id code >> ").upper()
        print conceptid
        yes = raw_input("  confirm (y/n) ").lower()
        if yes.startswith("y"):
            break

    concepts = []
    while len(concepts) == 0:
        concepts = get_entries()

    return name, values, conceptid, concepts

def make_files(data, out_dir):
    '''makes simple authority file with optional .values file'''
    authdoc_name, include_values_file, conceptid, concepts = data
    authdoc_path = os.path.join(out_dir,authdoc_name)
    
    if os.path.isfile(authdoc_path):
        print "ERROR: not going to overwrite anything today"
        return

    with open(authdoc_path, "wb") as authdoc:
        writer = csv.writer(authdoc, delimiter=",")
        writer.writerow(["conceptid","PrefLabel","AltLabels","ParentConceptid","ConceptType","Provider"])
        for num,label in enumerate(concepts):
            con = conceptid+":"+str(num+1)
            row = [con,label,"",authdoc_name.replace("_blank",""),"Index","PRESERVE/scapes"]
            writer.writerow(row)

    if not include_values_file:
        return

    values_file = authdoc_name.replace(".csv",".values.csv")
    values_path = os.path.join(out_dir,values_file)

    with open(values_path, "wb") as values:
        writer = csv.writer(values, delimiter=",")
        writer.writerow(["conceptid","Value","ValueType","Provider"])
        for num,label in enumerate(concepts):
            con = conceptid+":"+str(num+1)
            writer.writerow([con,str(num+1),"sortorder","PRESERVE/scapes"])

while True:
    data = get_info()
    make_files(data,out_dir)
    print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

    
    
