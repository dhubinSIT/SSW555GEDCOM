
# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual
from gedcom_parser import parse_date


class US32TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi1.apply_value('BIRT', parse_date('1 JUN 1985'))
        self.OkayIndi1.apply_value('DEAT', parse_date('1 AUG 2015'))
        self.OkayIndi1.apply_value('NAME', 'Big Willy Snake')

    def test_US32_Listofmultiplebirths(self):
        """List of multiple births."""
        Listofmultibirths = US32_Listofmultiplebirths({'@okay1@': self.OkayIndi1})
        self.assertFalse(self.OkayIndi1 in Listofmultibirths)

# UnitTest function
def main():
    '''main() function'''

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()

    
