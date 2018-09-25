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
    if d !=None:
        return datetime.datetime.strftime(d, "%d %b %Y")
    else:
        return ""

def lookupname(individuals, key):
    if key == None:
        return ""
    else:
        return individuals[key].name

if __name__ == "__main__":
    '''Begin by opening the file '''
    with open ('C:/Users/Ayana Perry/Documents/StevensInstituteofTechnology/Project01_Varadaraju.ged', 'r') as f:
        (indi, fam,  parse_warns) = parse_file(f)
        warnings = parse_warns + gedcom_validation.collect_validation_warnings(indi,  fam)    
        '''Begin code for arranging the Siblings Ages in order for the PrettyTable '''
        '''US28 Order Siblings by Age '''
        now = datetime.date.today()
        for x in sorted(fam):
            pt = PrettyTable(field_names=['Siblings_Names','Siblings_Ages'])
            siblingslist = fam[x].children_id_list
            siblings_age = dict()
            for z in siblingslist:
                born = indi[z].birth
                names = indi[z].name
                integeryears = now.year - born.year - ((now.month, now.day) < (born.month, born.day))
                siblings_age[names] = integeryears
        
            for y in sorted(siblings_age, key=lambda y: siblings_age[y]): 
                age = siblings_age[y]
                pt.add_row([y, age])
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
            
