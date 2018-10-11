
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
        self.OkayIndi1.apply_value('BIRT', parse_date('1 JUN 1945'))
        self.OkayIndi2.apply_value('BIRT', parse_date('1 JUN 2011'))
        self.OkayIndi1.apply_value('NAME', 'Prince William')
        self.OkayIndi2.apply_value('NAME', 'Princess Kate')
        self.OkayFam = Family('@okayf@')
        self.OkayFam.apply_value('CHIL', '@okay1@')

    def test_US33_ListOrphans_main(self):
        """List of Orphans."""
        ListofOrphans = US33_ListOrphans_main({'@okay1@': self.OkayIndi1,'@okay2@': self.OkayIndi2}, {'@okayf@': self.OkayFam})
        self.assertTrue(self.OkayFam in ListofOrphans)

#UnitTest function 
def main():
    '''main() function'''
          
if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main() 

    
    
