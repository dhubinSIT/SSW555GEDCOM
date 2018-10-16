# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import *
from gedcom_parser import parse_date


class US32TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi2 = Individual('@okay2@')
        self.OkayIndi3 = Individual('@okay3@')
        self.OkayIndi1.apply_value('BIRT', parse_date('1 JUN 2018'))
        self.OkayIndi2.apply_value('BIRT', parse_date('18 SEP 2017'))
        self.OkayIndi3.apply_value('BIRT', parse_date('1 JUN 2018'))
        self.OkayIndi1.apply_value('NAME', 'Prince William')
        self.OkayIndi2.apply_value('NAME', 'CrankyFranky')
        self.OkayIndi1.apply_value('NAME', 'BabyB /Rabbits/')
        self.OkayIndi3.apply_value('NAME', 'BabyC /Rabbits/')

    def test_US32_Listofmultiplebirths(self):
        """List of Multiple Births"""
        Listbirths = US32_Listofmultiplebirths({'@okay1@': self.OkayIndi1, '@okay2@': self.OkayIndi2, '@okay3@': self.OkayIndi3})
        self.assertTrue(self.OkayIndi1 in Listbirths)
        self.assertFalse(self.OkayIndi2 in Listbirths)
        self.assertTrue(self.OkayIndi3 in Listbirths)
        
# UnitTest function
def main():
    '''main() function'''


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()
