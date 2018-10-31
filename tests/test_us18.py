# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom_types import Individual, Family

class US18TestCase(unittest.TestCase):
    def setUp(self):
        self.brother = Individual('@brother@')
        self.brother.apply_value('FAMS','@siblingFamily@')
        self.sister = Individual('@sister@')
        self.sister.apply_value('FAMS','@siblingFamily@')
        self.mother = Individual('@mother@')
        self.father = Individual('@father@')
        self.child1 = Individual('@child@')
        self.childSpouse = Individual('@child1spouse@')
        
        self.parentFamily = Family('@parentFamily@')
        self.parentFamily.add_spouse_ref('HUSB',self.father)
        self.parentFamily.add_spouse_ref('WIFE',self.mother)
        self.parentFamily.apply_value('CHIL','@brother@')
        self.parentFamily.add_child_ref(self.brother)
        self.parentFamily.apply_value('CHIL','@sister@')
        self.parentFamily.add_child_ref(self.sister)
        
        self.siblingFamily = Family('@siblingFamily@')
        self.siblingFamily.apply_value('HUSB','@brother@')
        self.siblingFamily.add_spouse_ref('HUSB',self.brother)
        self.siblingFamily.apply_value('HUSB','@sister@')
        self.siblingFamily.add_spouse_ref('WIFE',self.sister)
        self.siblingFamily.apply_value('CHIL','@child@')
        self.siblingFamily.add_child_ref(self.child1)

        self.grandkidsFamily = Family('@grandkids@')
        self.grandkidsFamily.apply_value('HUSB','@child@')
        self.grandkidsFamily.add_spouse_ref('HUSB',self.child1)
        self.grandkidsFamily.apply_value('WIFE','@child1spouse@')
        self.grandkidsFamily.add_spouse_ref('WIFE',self.childSpouse)

    def test_sibling_married(self):
        """Test a family where siblings are married to each other"""
        warns = self.parentFamily._Check_Siblings_Married_to_Each_Other()
        self.assertTrue(len(warns) == 1)
        self.assertTrue(warns[0].story == "US18")
        self.assertTrue('is married to a sibling' in warns[0].message)

    def test_normal_family(self):
        """Test a family where family kids are married normally"""
        warns = self.siblingFamily._Check_Siblings_Married_to_Each_Other()
        self.assertTrue(len(warns) == 0)
