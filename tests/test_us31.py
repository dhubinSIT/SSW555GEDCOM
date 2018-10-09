# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual
from gedcom_parser import parse_date


class US31TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi1.apply_value('BIRT', parse_date('1 JUN 1985'))
        self.OkayIndi1.apply_value('DEAT', parse_date('1 JUN 1985'))
        self.OkayIndi1.apply_value('NAME', 'Princess Kate')


    def test_US31_Listofliving(self):
        """List of Living."""
        self.assertFalse(US31_Listofliving({'@okay1@': self.OkayIndi1}) == 'Princess Kate')
        self.assertFalse(US31_Listofliving({'@okay1@': self.OkayIndi1}) == 'Princess Kate','1 JUN 1985')


# UnitTest function
def main():
    '''main() function'''

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()
