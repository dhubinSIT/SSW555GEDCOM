# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual, Family,  GedcomDate

class US12TestCase(unittest.TestCase):
    def setUp(self):
        self.OldFamily = Family('@oldfam@')
        self.OldFather = Individual('@oldfart@')
        self.OldFather.apply_value('BIRT', GedcomDate("01 JAN 1900"))
        self.OldMother = Individual('@oldtart@')
        self.OldMother.apply_value('BIRT', GedcomDate("01 JAN 1920"))
        self.ChildOfOld = Individual("@oldchild@")
        self.ChildOfOld.apply_value('BIRT',  GedcomDate("02 JAN 1980"))
        self.OldFamily.add_spouse_ref("HUSB", self.OldFather)
        self.OldFamily.add_spouse_ref("WIFE", self.OldMother)
        self.OldFamily.add_child_ref(self.ChildOfOld)
        
        self.ReasonableFamily = Family('@okayfam@')
        self.YngFather = Individual('@oldfart@')
        self.YngFather.apply_value('BIRT', GedcomDate("01 JAN 1900"))
        self.YngMother = Individual('@oldtart@')
        self.YngMother.apply_value('BIRT', GedcomDate("01 JAN 1920"))
        self.ChildOfYng = Individual("@oldchild@")
        self.ChildOfYng.apply_value('BIRT',  GedcomDate("31 DEC 1979"))
        self.ReasonableFamily.add_spouse_ref("HUSB", self.YngFather)
        self.ReasonableFamily.add_spouse_ref("WIFE", self.YngMother)
        self.ReasonableFamily.add_child_ref(self.ChildOfYng)

    def test_old_family(self):
        """Test a child born when father 80 years and mother 60 years old.
        Note, using 02 JAN because of leap year rounding."""
        warns = self.OldFamily._Check_Parent_Child_Relative_Ages()
        self.assertTrue(len(warns) == 2)
        self.assertTrue(len([x for x in warns if x.story == "US12" and "@oldfart@" in x.message and "@oldchild" in x.message and "Father" in x.message]) == 1)
        self.assertTrue(len([x for x in warns if x.story == "US12" and "@oldtart@" in x.message and "@oldchild" in x.message and "Mother" in x.message]) == 1)

    def test_okay_family(self):
        """Test a child born when father 80 years (less one day) and mother 60 years old (less one day)."""
        warns = self.ReasonableFamily._Check_Parent_Child_Relative_Ages()
        self.assertTrue(len(warns) == 0)
        
