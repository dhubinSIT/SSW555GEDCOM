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

'''def deceasedstring(drel):
    """Pretty-print empty string for non-deceased for output."""
    if drel != None:
        return datestring(indi[x].death)
    else:
        return ""
'''
def lookupname(individuals, key):
    if key == None:
        return ""
    else:
        return individuals[key].name

if __name__ == "__main__":
    '''Begin by opening the file '''
    with open ('C:/Users/Ayana Perry/Documents/StevensInstituteofTechnology/Hubin_fictional_family.ged', 'r') as f:
        (indi, fam,  parse_warns) = parse_file(f)
        warnings = parse_warns + gedcom_validation.collect_validation_warnings(indi,  fam)    
        '''Begin code for arranging the Siblings Ages in order for the PrettyTable '''
        '''US28 Order Siblings by Age '''
        now = datetime.date.today()
        siblings_age = list()
        print('Age of Siblings')
        pt = PrettyTable(field_names=[('Siblings_Age')])
        for x in sorted(indi):
            born = (indi[x].birth) 
            integeryears = now.year - born.year - ((now.month, now.day) < (born.month, born.day))
            siblings_age.append(integeryears)
        pt.add_row([sorted(siblings_age)])
        print(pt)

        '''Begin code for lists of deceased in order for the PrettyTable '''
        '''US29 Lists deceased '''
        deceased = list()
        print('Lists Deceased')
        pt = PrettyTable(field_names=[('Passed Away')])
        for x in (indi):
            passedaway = (datestring(indi[x].death))
            deceasednames = (indi[x].name)
            deceased.append(passedaway)
        pt.add_row([(deceased)])
        print(pt)

        '''Begin code for arranging the Individual PrettyTable '''  
        print('Individuals') 
        pt = PrettyTable(field_names=['ID','Name','Gender','Birthday','Death','Child','Spouse'])
        for x in sorted(indi):
            pt.add_row([indi[x].id,indi[x].name,indi[x].gender,datestring(indi[x].birth),datestring(indi[x].death),indi[x].child_family_ids,indi[x].spouse_family_ids])
        print(pt)
        
        '''Begin code for arranging the Families PrettyTable '''
        print('Families')
        pt = PrettyTable(field_names=['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife Name','Children'])
        for x in sorted(fam):
            husband_name = lookupname(indi, fam[x].husband_id)
            wife_name = lookupname(indi,  fam[x].wife_id)
            pt.add_row([fam[x].id,datestring(fam[x].married),datestring(fam[x].divorced),fam[x].husband_id,husband_name,fam[x].wife_id,wife_name,fam[x].children_id_list])
        print(pt)
        
        if len(warnings) > 0:
            print('Warnings')
            pt = PrettyTable(field_names=['Code', 'Message'])
            for warn in warnings:
                pt.add_row([warn.story,  warn.message])
            print(pt)
        else:
            print()
            print("GEDCOM database is sane.")
