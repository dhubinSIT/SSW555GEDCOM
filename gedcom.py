# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import sys

from prettytable import PrettyTable
from gedcom_types import *
from gedcom_parser import parse_file

if __name__ == "__main__":
    with open (sys.argv[1], 'r') as f:
        (indi, fam) = parse_file(f)
        for x in indi:
            print(indi[x])
        print
        print('Families')
        pt = PrettyTable(field_names=['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife Name','Children'])
        for x in fam:
            pt.add_row([fam[x].id,fam[x].married,fam[x].divorced,fam[x].husband_id,indi[fam[x].husband_id].name,fam[x].wife_id,indi[fam[x].wife_id].name,fam[x].children_id_list])
        print(pt)
