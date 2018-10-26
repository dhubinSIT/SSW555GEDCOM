# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom_types import Individual, Family

class US21TestCase(unittest.TestCase):
    def setUp(self):
        self.OddFamily = Family('@oddfam@')
        self.MasculineWoman = Individual('@wearspants@')
        self.MasculineWoman.apply_value("SEX",  "F")
        self.FeminineMan = Individual('@wearsskirts@')
        self.FeminineMan.apply_value("SEX",  "M")
        self.OddFamily.add_spouse_ref("HUSB", self.MasculineWoman)
        self.OddFamily.add_spouse_ref("WIFE", self.FeminineMan)
        
        self.ReasonableFamily = Family('@okayfam@')
        self.ManlyMan = Individual('@dude@')
        self.ManlyMan.apply_value('SEX', 'M')
        self.FeminineWoman = Individual('@lady@')
        self.FeminineWoman.apply_value('SEX', 'F')
        self.ReasonableFamily.add_spouse_ref("HUSB", self.ManlyMan)
        self.ReasonableFamily.add_spouse_ref("WIFE", self.FeminineWoman)
        
        self.UnknownFamily = Family('@blankfam@')
        self.OtherMan = Individual('@dude@')
        self.OtherLady = Individual('@lady@')
        self.UnknownFamily.add_spouse_ref("HUSB", self.OtherMan)
        self.UnknownFamily.add_spouse_ref("WIFE", self.OtherLady)

    def test_questionable_family(self):
        """Test a family with a woman as a husband, and a man as a wife."""
        warns = self.OddFamily._Check_Familial_Roles()
        self.assertTrue(len(warns) == 2)
        self.assertTrue(len([x for x in warns if x.story == "US21" and "@wearspants@" in x.message and "Husband" in x.message]) == 1)
        self.assertTrue(len([x for x in warns if x.story == "US21" and "@wearsskirts@" in x.message and "Wife" in x.message]) == 1)

    def test_okay_family(self):
        """Test a family with normal husband/wife gender roles."""
        warns = self.ReasonableFamily._Check_Familial_Roles()
        self.assertTrue(len(warns) == 0)
        
    def test_unknown_family(self):
        """Test a family with blank gender identities (don't warn)."""
        warns = self.UnknownFamily._Check_Familial_Roles()
        self.assertTrue(len(warns) == 0)
