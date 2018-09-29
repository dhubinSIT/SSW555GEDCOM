# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom import *
from gedcom_types import Individual, Family
from gedcom_parser import parse_date

class US28TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi1 = Individual('@okay1@')
        self.OkayIndi2 = Individual('@okay2@')
        self.OkayIndi1.apply_value('BIRT', parse_date('1 JUN 1945'))
        self.OkayIndi2.apply_value('BIRT', parse_date('1 JUN 1945'))
        self.OkayIndi1.apply_value('NAME', 'Prince William')
        self.OkayIndi2.apply_value('NAME', 'Princess Kate')
        self.OkayFam = Family('@okayf@')
        self.OkayFam.apply_value('CHIL', '@okay1@')
        self.OkayFam.apply_value('CHIL', '@okay2@')

    def test_US28_SiblingsByAge_pt(self):
        '''Test warnings if'''
        SiblingsAges = US28_SiblingsByAge(self.OkayFam.children_id_list,{'@okay1@' : self.OkayIndi1,'@okay2@': self.OkayIndi2},
                                         {'@okayf@' : self.OkayFam})
        self.assertEqual(SiblingsAges['Prince William'], 73)
        self.assertTrue(SiblingsAges['Princess Kate'] == 73)

#UnitTest function
def main():
    '''main() function'''
          
if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()
