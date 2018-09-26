# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from io import StringIO
import unittest
from datetime import datetime
from gedcom_parser import parse_file

class US22TestCase(unittest.TestCase):
    def shortDescription(self):
        """Disable printing docstring on verbose."""
        return None
        
    def test_duplicate_entries(self):
        """Test duplicate identifiers for both individuals and families."""
        buff = StringIO("""0 @I1@ INDI
1 NAME CrankyFrank /Coffin/
1 SEX M
1 BIRT
2 DATE 31 JAN 1940
1 DEAT
2 DATE 28 FEB 1988
1 FAMS @F1@
0 @I1@ INDI
1 NAME MarvelousMay /Coffin/
1 SEX F
1 BIRT
2 DATE 15 MAY 1941
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 7 JUL 1972
1 DIV
2 DATE 15 JUL 1973
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 15 JUL 1973
1 DIV
2 DATE 19 JUL 1974""")
        (ind,  fam,  parse_warns) = parse_file(buff)
        self.assertTrue(len(parse_warns) >=  2)
        countus22 = 0
        for warn in parse_warns:
            countus22 += 1 if (warn.story == "US22") else 0
        self.assertEqual(countus22,  2)
        self.assertEqual(len(ind),  1)
        self.assertEqual(len(fam),  1)
        self.assertEqual(ind["@I1@"].gender,  'F')  # demonstrates we kept the second entry
        self.assertTrue(fam["@F1@"].divorced > datetime(1974, 1, 1)) # demonstrates we kept the second entry

