import sys
import unittest
from gedcom_parser import parse_file
from gedcom_types import Family,Individual

class US29TestCase(unittest.TestCase):     
    def test_parse_file(self):
        """List deceased relatives."""
        self.assertTrue("DEAT", parse_file("15 AUG 1999"))
        self.assertFalse("DEAT",parse_file("8 OCT 1986"))
        self.assertEquals("DEAT",parse_file("4 JUN 2019"))
        self.assertNotIn("DEAT",parse_file("29 JUN 2005"))
        self.assertNotIsInstance("DEAT",parse_file("7 MAY 2009"))
        
#UnitTest function 
def main():
    '''main() function'''
          
if __name__ == "__main__":

    unittest.main(exit=False, verbosity=2)
    main() 
