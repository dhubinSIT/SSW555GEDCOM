# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual
from gedcom_parser import parse_date


class US36TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi1.apply_value('DEAT', parse_date('1 JUN 1995'))
        self.OkayIndi1.apply_value('NAME', 'Sylvester the cat')

    def test_US36_Listrecentdeaths(self):
        """List of recent deaths."""
        recent_deaths = US36_Listrecentdeaths({'@okay1@': self.OkayIndi1})

        self.assertFalse(self.OkayIndi1 in recent_deaths)


# UnitTest function
def main():
    '''main() function'''


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()
