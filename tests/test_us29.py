import sys
import unittest
from gedcom import printDeceased
from gedcom_parser import parse_file,  parse_date
from gedcom_validation import collect_validation_warnings
from gedcom_types import Family,  Individual

#US29 - List of Deceased
class printDeceasedTest(unittest.TestCase):     
    def test_printDeceased(self):
        """List of Deceased."""
        self.assertTrue("printDeceased", parse_file("15 AUG 1999"))
        self.assertNotIn("printDeceased",parse_file("29 JUN 2005"))
        self.assertTrue("printDeceased",parse_file("11 Nov 1995"))
        self.assertNotEqual("printDeceased",parse_file("13 Nov 1995"))
        self.assertNotIn("printDeceased",parse_file("7 MAY 2009"))   
   
#UnitTest function 
def main():
    '''main() function'''
          
if __name__ == "__main__":

    unittest.main(exit=False, verbosity=2)
    main() 
