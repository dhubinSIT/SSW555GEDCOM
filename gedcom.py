# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

'''GEDCOM code to display the Individuals and Families using PrettyTable module'''
import sys
import datetime

from prettytable import PrettyTable
from gedcom_parser import parse_file
import gedcom_validation

def datestring(d):
    """Pretty-print a date for output."""
    if d != None:
        return datetime.datetime.strftime(d, "%d %b %Y")
    else:
        return ""

def lookupname(individuals, key):
    if key == None:
        return ""
    else:
        return individuals[key].name

def printIndividuals(indi):
    '''Produce and print the table of individuals.'''
    print('Individuals')
    pt = PrettyTable(field_names=['ID','Name','Gender','Birthday','Death','Child','Spouse'])
    for x in sorted(indi):
        pt.add_row([indi[x].id,indi[x].name,indi[x].gender,datestring(indi[x].birth),datestring(indi[x].death),indi[x].child_family_ids,indi[x].spouse_family_ids])
    print(pt)

def printFamilies(indi, fam):
    '''Produce and print the table of families.'''
    print('Families')
    pt = PrettyTable(field_names=['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife Name','Children'])
    for x in sorted(fam):
        husband_name = lookupname(indi, fam[x].husband_id)
        wife_name = lookupname(indi,  fam[x].wife_id)
        pt.add_row([fam[x].id,datestring(fam[x].married),datestring(fam[x].divorced),fam[x].husband_id,husband_name,fam[x].wife_id,wife_name,fam[x].children_id_list])
    print(pt)

def printWarnings(warnings):
    """Produce and print the table of warnings."""
    if len(warnings) > 0:
        print('Warnings')
        pt = PrettyTable(field_names=['Code', 'Message'])
        for warn in warnings:
            pt.add_row([warn.story,  warn.message])
        print(pt)
    else:
        print()
        print("GEDCOM database is sane.")

if __name__ == "__main__":
    '''Begin by opening the file '''
    with open (sys.argv[1], 'r') as f:
        (indi, fam,  parse_warns) = parse_file(f)
        warnings = parse_warns + gedcom_validation.collect_validation_warnings(indi,  fam)
        
        printIndividuals(indi)
        printFamilies(indi, fam)
        printWarnings(warnings)
