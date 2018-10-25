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


def lookupname(individuals, key):
    if key == None:
        return ""
    else:
        return individuals[key].name


def printIndividuals(indi):
    '''Produce and print the table of individuals.'''
    print('Individuals')
    pt = PrettyTable(field_names=['ID', 'Name', 'Gender', 'Birthday', 'Death', 'Child', 'Spouse'])
    for x in sorted(indi):
        pt.add_row([indi[x].id, indi[x].name, indi[x].gender, datestring(indi[x].birth), datestring(indi[x].death),
                    indi[x].child_family_ids, indi[x].spouse_family_ids])
    print(pt)


def printFamilies(indi, fam):
    '''Produce and print the table of families.'''
    print('Families')
    pt = PrettyTable(
        field_names=['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])
    for x in sorted(fam):
        husband_name = lookupname(indi, fam[x].husband_id)
        wife_name = lookupname(indi, fam[x].wife_id)
        pt.add_row([fam[x].id, datestring(fam[x].married), datestring(fam[x].divorced), fam[x].husband_id, husband_name,
                    fam[x].wife_id, wife_name, fam[x].children_id_list])
    print(pt)


def US28_SiblingsByAge(siblingslist, indi, fam):
    '''Refactor for unittest '''
    now = datetime.date.today()
    siblings_age = dict()
    for z in siblingslist:
        born = indi[z].birth
        names = indi[z].name
        integeryears = now.year - born.year - ((now.month, now.day) < (born.month, born.day))
        siblings_age[names] = integeryears
    return siblings_age


def US28_SiblingsByAge_pt(indi, fam):
    '''A's User story 28-Order Siblings by Age.'''
    print('US28: Siblings by their ages')
    for x in sorted(fam):
        pt = PrettyTable(field_names=['Siblings_Names', 'Siblings_Ages'])
        siblings_age = dict()
        siblingslist = fam[x].children_id_list
        siblings_age = US28_SiblingsByAge(siblingslist, indi, fam)
        for y in sorted(siblings_age, key=lambda y: siblings_age[y], reverse=True):
            age = siblings_age[y]
            pt.add_row([y, age])
        print(pt)


def US29_ListOfDeceased(indi):
    '''AP's User story 29 - List Deceased.'''
    pt = PrettyTable(field_names=['Deceased_Names', 'Deceased_Date'])
    print('US29: List of Deceased')
    for x in sorted(indi):
        deceased = list()
        if indi[x].death is not None:
            died = datestring(indi[x].death)
            names = indi[x].name
            deceased.append(names)
            pt.add_row([names,died])
    print(pt)
    return deceased


def US30_ListLivingMarried_pt(indi, fam):
    '''AP's User story 30 - List living married'''
    print('US30: List living married')
    pt = PrettyTable(field_names=['Husband', 'Wife'])
    marriedFamilies = US30_Listlivingmarried_main(indi, fam)
    for family in marriedFamilies:
        pt.add_row([indi[family.husband_id].name, indi[family.wife_id].name])
    print(pt)


def US30_Listlivingmarried_main(indi, fam):
    '''AP's User story 30 - List living married'''
    married = list()
    for f in fam:
        if fam[f].divorced is None and fam[f].husband_id is not None and indi[fam[f].husband_id].death is None and \
                fam[f].wife_id is not None and indi[fam[f].wife_id].death is None:
            married.append(fam[f])
    return married


def US31_Listofliving(indi):
    """ AP User story 31 - List of Living """
    pt = PrettyTable(field_names=['Living Names', 'Birthdays'])
    print('US31: List of Living')
    for i in sorted(indi):
        living = list()
        if indi[i].death is None:
            alive = datestring(indi[i].birth)
            names = indi[i].name
            living.append(names)
            pt.add_row([names,alive])
    print(pt)
    return living


def US32_Listofmultiplebirths(indi):
    """ AP User story 32 - List of Living """
    pt = PrettyTable(field_names=['Children Names', 'Birthdays'])
    print('US32: List of Multiple Births')
    births = list()
    for index in indi:
        for index1 in indi:
            if indi[index].birth == indi[index1].birth and index != index1 and \
            indi[index].birth is not None:
                pt.add_row([indi[index].name, datestring(indi[index].birth)])
                births.append(indi[index])  
                break
    print(pt)
    return births


def US33_ListOrphans_pt(indi, fam):
    """AP's User Story 33 - List orphans PrettyTable function"""
    print('US33: List of Orphans')
    pt = PrettyTable(field_names=['Orphan_Children'])
    orphans = US33_ListOrphans_main(indi, fam)
    for ofam in orphans:
        for ochildren in ofam.children_list:
            pt.add_row([ochildren.name])  
    print(pt)


def US33_ListOrphans_main(indi, fam):
    """AP's User Story 33 - List orphans Main function"""
    orphanchildren = list()
    for f in fam:
        if fam[f].husband is not None and indi[fam[f].husband_id].death is not None and \
                fam[f].wife is not None and indi[fam[f].wife_id].death is not None:
            orphanchildren.append(fam[f])
    return orphanchildren


def printWarnings(warnings):
    """Produce and print the table of warnings."""
    if len(warnings) > 0:
        print('Warnings')
        pt = PrettyTable(field_names=['Code', 'Message'])
        for warn in warnings:
            pt.add_row([warn.story, warn.message])
        pt.sortby = "Code"
        print(pt)
    else:
        print()
        print("GEDCOM database is sane.")


if __name__ == "__main__":
    '''Begin by opening the file '''
    with open(sys.argv[1], 'r') as f:
        (indi, fam, parse_warns) = parse_file(f)
        warnings = parse_warns + gedcom_validation.collect_validation_warnings(indi, fam)

        printIndividuals(indi)
        printFamilies(indi, fam)
        US28_SiblingsByAge_pt(indi, fam)
        US29_ListOfDeceased(indi)
        US30_ListLivingMarried_pt(indi, fam)
        US31_Listofliving(indi)
        US32_Listofmultiplebirths(indi)
        US33_ListOrphans_pt(indi, fam)
        printWarnings(warnings)
