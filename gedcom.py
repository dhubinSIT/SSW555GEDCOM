# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadarajur

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

def lookupname(ref):
    """Returns the string representing value, or a blank string if None"""
    return (ref.name if (ref != None) else "")

def printIndividuals(individuals):
    '''Produce and print the table of individuals.'''
    print('Individuals')
    pt = PrettyTable(field_names=['ID','Name','Gender','Birthday','Death','Child','Spouse'])
    for ind in sorted(individuals.values(),  key=lambda x: x.id):
        pt.add_row([ind.id,ind.name,ind.gender,datestring(ind.birth),datestring(ind.death),ind.child_family_ids,ind.spouse_family_ids])
    print(pt)

def printFamilies(individuals, families):
    '''Produce and print the table of families.'''
    print('Families')
    pt = PrettyTable(field_names=['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife Name','Children'])
    for fam in sorted(families.values(),  key=lambda x: x.id):
        husband_name = lookupname(fam.husband)
        wife_name = lookupname(fam.wife)
        pt.add_row([fam.id,datestring(fam.married),datestring(fam.divorced),fam.husband_id,husband_name,fam.wife_id,wife_name,fam.children_id_list])
    print(pt)
    
def US28_SiblingsByAge(siblingslist,indi, fam):
    '''Refactor for unittest '''
    now = datetime.date.today()
    siblings_age = dict()
    for z in siblingslist:
        born = indi[z].birth
        names = indi[z].name
        integeryears = now.year - born.year - ((now.month, now.day) < (born.month, born.day))
        siblings_age[names] = integeryears
    return siblings_age

def US28_SiblingsByAge_pt(indi,fam):
    '''A's User story 28-Order Siblings by Age.'''
    print('US28_Siblings by their ages')
    for x in sorted(fam):
        pt = PrettyTable(field_names=['Siblings_Names','Siblings_Ages'])
        siblings_age = dict()
        siblingslist = fam[x].children_id_list
        siblings_age = US28_SiblingsByAge(siblingslist,indi,fam)
        for y in sorted(siblings_age, key=lambda y: siblings_age[y], reverse=True): 
            age = siblings_age[y]
            pt.add_row([y, age])
        print(pt)

def US29_ListOfDeceased(indi):
    '''AP's User story 29 - List Deceased.'''
    print('US29_List of Deceased')
    pt = PrettyTable(field_names=['Deceased_Names','Deceased_Date'])
    for x in (indi):
        deceased = list()
        if indi[x].death != None:
            died = datestring(indi[x].death)
            names = indi[x].name
            deceased.append(names)
            deceased.append(died)
            pt.add_row(deceased)
    print(pt)
    return names

def US30_ListLivingMarried_pt(indi,fam):
    '''AP's User story 30 - List living married'''  
    print('List living married')
    pt = PrettyTable(field_names=['Husband', 'Wife'])
    marriedFamilies = US30_Listlivingmarried_main(indi,fam)
    for family in marriedFamilies:
        pt.add_row([indi[family.husband_id].name, indi[family.wife_id].name])
    print(pt)    

def US30_Listlivingmarried_main(indi,fam):
    '''AP's User story 30 - List living married'''
    married = list()
    for f in fam:
        if fam[f].divorced == None and fam[f].husband_id != None and indi[fam[f].husband_id].death == None and \
           fam[f].wife_id != None and indi[fam[f].wife_id].death == None:
            married.append(fam[f])
    return married

def US31_Listofliving(indi):
    """ AP User story 31 - List of Living """
    pt = PrettyTable(field_names=['Living Names', 'Birthdays'])
    print('List of Living')
    for i in sorted(indi):
        living = list()
        if indi[i].death == None:
            alive = datestring(indi[i].birth)
            names = indi[i].name
            living.append(names)
            pt.add_row([names,alive])
    print(pt)
    return living


def printWarnings(warnings):
    """Produce and print the table of warnings."""
    if len(warnings) > 0:
        print('Warnings')
        pt = PrettyTable(field_names=['Code', 'Message'])
        for warn in warnings:
            pt.add_row([warn.story,  warn.message])
        pt.sortby = "Code"
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
        US28_SiblingsByAge_pt(indi, fam)
        US29_ListOfDeceased(indi)
        US30_ListLivingMarried_pt(indi,fam)
        US31_Listofliving(indi)
        printWarnings(warnings)

