# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual
from gedcom_parser import parse_date


class US35TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi1.apply_value('BIRT', parse_date('1 JUN 1985'))
        self.OkayIndi1.apply_value('NAME', 'Porky Pig')

    def test_US35_Listrecentbirths(self):
        """List of recent births."""
        recent_births = US35_Listrecentbirths({'@okay1@': self.OkayIndi1})

        self.assertFalse(self.OkayIndi1 in recent_births)


# UnitTest function
def main():
    '''main() function'''


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()

