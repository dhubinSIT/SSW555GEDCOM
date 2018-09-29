# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual
from gedcom_parser import parse_date

class US29TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi1.apply_value('DEAT', parse_date('1 JUN 1945'))
        self.OkayIndi1.apply_value('NAME', 'Prince William')

    def test_US29_ListOfDeceased(self):
        """List of Deceased."""
        self.assertFalse(US29_ListOfDeceased({'@okay1@': self.OkayIndi1}) != 'Prince William')
        self.assertTrue(US29_ListOfDeceased({'@okay1@': self.OkayIndi1}) == 'Prince William')

#UnitTest function 
def main():
    '''main() function'''
          
if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()
