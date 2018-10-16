# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import *
from gedcom_parser import parse_date


class US33TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi2 = Individual('@okay2@')
        self.OkayIndi1.apply_value('NAME', 'Lucy /Simmons/')
        self.OkayIndi2.apply_value('NAME', 'Patrick /Simmons/')
        self.OkayFam = Family('@okayf@')
        self.OkayFam.apply_value('CHIL', '@okay1@')
        self.OkayFam.apply_value('CHIL', '@okay2@')

    def test_US33_ListOrphans_main(self):
        """List of Orphans"""
        Listoforphans = US33_ListOrphans_main({'@okay1@': self.OkayIndi1, '@okay2@': self.OkayIndi2}, \
                                              {'@okayf@': self.OkayFam})
        self.assertFalse(self.OkayFam in Listoforphans)
        self.assertFalse(self.OkayIndi2 in Listoforphans)


# UnitTest function
def main():
    '''main() function'''


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()
 
    
