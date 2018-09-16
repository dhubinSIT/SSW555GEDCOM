# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from io import StringIO
import unittest
from gedcom_parser import parse_file

class US01TestCase(unittest.TestCase):
    def shortDescription(self):
        """Disable printing docstring on verbose."""
        return None
        
    def test_invalid_dates(self):
        """Test invalid dates.  First Individual is tested using dates
        that cannot happen (such as day numbers out of range for the month).
        Other Individual and Family are tested using date formats which are
        not correct."""
        buff = StringIO("""0 @I1@ INDI
1 NAME CrankyFrank /Coffin/
1 SEX M
1 BIRT
2 DATE 32 JAN 1940
1 DEAT
2 DATE 29 FEB 1941
1 FAMS @F1@
0 @I2@ INDI
1 NAME MarvelousMay /Coffin/
1 SEX F
1 BIRT
2 DATE 15/MAY/1941
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 15-07-1972
1 DIV
2 DATE July 15, 1973""")
        (ind,  fam,  parse_warns) = parse_file(buff)
        self.assertEqual(len(parse_warns),  5)
        self.assertEqual(ind["@I1@"].birth,  None)
        self.assertEqual(ind["@I1@"].death,  None)
        self.assertEqual(ind["@I2@"].birth,  None)
        self.assertEqual(fam["@F1@"].married,  None)
        self.assertEqual(fam["@F1@"].divorced,  None)
        
    def test_valid_dates(self):
        """Test valid dates.."""
        buff = StringIO("""0 @I1@ INDI
1 NAME CrankyFrank /Coffin/
1 SEX M
1 BIRT
2 DATE 31 JAN 1940
1 DEAT
2 DATE 28 FEB 1941
1 FAMS @F1@
0 @I2@ INDI
1 NAME MarvelousMay /Coffin/
1 SEX F
1 BIRT
2 DATE 15 MAY 1941
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 15 JUL 1972
1 DIV
2 DATE 15 JUL 1973""")
        (ind,  fam,  parse_warns) = parse_file(buff)
        self.assertEqual(len(parse_warns),  0)
        self.assertNotEqual(ind["@I1@"].birth,  None)
        self.assertNotEqual(ind["@I1@"].death,  None)
        self.assertNotEqual(ind["@I2@"].birth,  None)
        self.assertNotEqual(fam["@F1@"].married,  None)
        self.assertNotEqual(fam["@F1@"].divorced,  None)
