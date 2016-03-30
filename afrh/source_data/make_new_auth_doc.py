import os
import csv

out_dir = 'concepts/authority_files'

def get_info():
    '''collects raw input'''
    name_confirm = False
    while not name_confirm:
        name = raw_input("enter new authority doc name >> ").upper()+"_AUTHORITY_DOCUMENT.csv"
        print name
        yes = raw_input("  confirm name (y/n) ").lower()
        if yes.startswith("y"):
            name_confirm = True

    values = True
    val_con = raw_input("  include .values file? (y/n) >> ").lower()
    if val_con.startswith("y"):
        values = True

    return name, values

def make_files(name, include_values_file, out_dir):
    '''makes simple authority file with optional .values file'''
    authdoc_name = name.replace(".csv","_blank.csv")
    authdoc_path = os.path.join(out_dir,authdoc_name)
    
    if os.path.isfile(authdoc_path):
        print "not going to overwrite anything today"
        return

    with open(authdoc_path, "wb") as authdoc:
        writer = csv.writer(authdoc, delimiter=",")
        writer.writerow(["conceptid","PrefLabel","AltLabels","ParentConceptid","ConceptType","Provider"])
        writer.writerow(["CON:1","VALUE","",authdoc_name.replace("_blank",""),"Index","PRESERVE/scapes"])

    if not include_values_file:
        return

    values_file = authdoc_name.replace(".csv",".values.csv")
    values_path = os.path.join(out_dir,values_file)

    with open(values_path, "wb") as values:
        writer = csv.writer(values, delimiter=",")
        writer.writerow(["conceptid","Value","ValueType","Provider"])
        writer.writerow(["CON:1","1","sortorder","PRESERVE/scapes"])

while True:
    info = get_info()
    make_files(info[0],info[1],out_dir)

    
    
