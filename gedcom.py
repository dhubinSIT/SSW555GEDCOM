# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import sys

from gedcom_types import *
from gedcom_parser import parse_file

if __name__ == "__main__":
    with open (sys.argv[1], 'r') as f:
        (indi, fam) = parse_file(f)
        for x in indi:
            print(indi[x])
        print
        for x in fam:
            print(fam[x])


