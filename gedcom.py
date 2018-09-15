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

def datestring(d):
    """Pretty-print a date for output."""
    if d != None:
        return datetime.datetime.strftime(d, "%d %b %Y")
    else:
        return ""

if __name__ == "__main__":
    '''Begin by opening the file '''
    with open (sys.argv[1], 'r') as f:
        (indi, fam) = parse_file(f)
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
            pt.add_row([fam[x].id,datestring(fam[x].married),datestring(fam[x].divorced),fam[x].husband_id,indi[fam[x].husband_id].name,fam[x].wife_id,indi[fam[x].wife_id].name,fam[x].children_id_list])
        print(pt)
        
         # Check for errors and anomalies
        for x in sorted(indi):
            indi[x].validate_individual()
