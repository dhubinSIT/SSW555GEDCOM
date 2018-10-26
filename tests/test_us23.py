# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom_validation import _US23_Unique_Individuals
from gedcom_types import Individual,  GedcomDate

class US23TestCase(unittest.TestCase):
    def setUp(self):
        self.Dupe1 = Individual('@dupe1@')
        self.Dupe1.apply_value('NAME', 'Danny /Dupe/')
        self.Dupe1.apply_value('BIRT', GedcomDate("1 JAN 1900"))
        self.Dupe2 = Individual('@dupe2@')
        self.Dupe2.apply_value('NAME', 'Danny /Dupe/')
        self.Dupe2.apply_value('BIRT', GedcomDate("1 JAN 1900"))
        self.OtherName = Individual('@name@')
        self.OtherName.apply_value('NAME', 'Danny /Duplicate/')
        self.OtherName.apply_value('BIRT', GedcomDate("1 JAN 1900"))
        self.OtherBirth = Individual('@birth@')
        self.OtherBirth.apply_value('NAME', 'Danny /Dupe/')
        self.OtherBirth.apply_value('BIRT', GedcomDate("1 JAN 1901"))
        
    def test_duplicates(self):
        """Test US23 Unique name and birth date"""
        warns = _US23_Unique_Individuals({self.Dupe1.id: self.Dupe1, self.Dupe2.id: self.Dupe2,
                                          self.OtherName.id: self.OtherName, self.OtherBirth.id: self.OtherBirth})
        self.assertTrue(len(warns) == 1)
        self.assertTrue(warns[0].story == "US23")
        self.assertTrue(self.Dupe1.id in warns[0].message)
        self.assertTrue(self.Dupe2.id in warns[0].message)
        self.assertTrue(self.OtherName.id not in warns[0].message)
        self.assertTrue(self.OtherBirth.id not in warns[0].message)
        
