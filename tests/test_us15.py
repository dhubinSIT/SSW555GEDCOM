# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual, Family

class US15TestCase(unittest.TestCase):
    def setUp(self):
        self.HugeFamily = Family('@hugefam@')
        for x in range(1, 16):  # loops 15 times
            indi = Individual("@indi%d" % x)
            self.HugeFamily.apply_value("CHIL", "@indi%d")
            self.HugeFamily.add_child_ref(indi)
            
        self.ReasonableFamily = Family('@okayfam@')
        for x in range(1, 15):  # loops 14 times
            indi = Individual("@okayindi%d" % x)
            self.ReasonableFamily.apply_value("CHIL", "@okayindi%d")
            self.ReasonableFamily.add_child_ref(indi)

    def test_huge_family(self):
        """Test a family that is above the limit of reasonableness (15 kids)."""
        warns = self.HugeFamily._Check_Excessive_Siblings()
        self.assertTrue(len(warns) == 1)
        self.assertTrue(warns[0].story == "US15")
        self.assertTrue('15' in warns[0].message)
        self.assertTrue('@hugefam@' in warns[0].message)
        self.assertTrue('large number of children' in warns[0].message)

    def test_reasonable_family(self):
        """Test a family that is below the limit of reasonableness (14 kids)."""
        warns = self.ReasonableFamily._Check_Excessive_Siblings()
        self.assertTrue(len(warns) == 0)
