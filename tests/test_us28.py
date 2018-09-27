import sys
import unittest
from gedcom import printSiblings
from gedcom_parser import parse_file,  parse_date
from gedcom_validation import collect_validation_warnings
from gedcom_types import Family,  Individual

#US28 - Order Siblings by Age
class printSiblingsTest(unittest.TestCase):     
    def test_printSiblings(self):
        """Order Siblings by Age."""
        self.assertTrue("printSiblings", parse_file("45"))
        self.assertNotIn("printSiblings",parse_file("89"))
   
#UnitTest function 
def main():
    '''main() function'''
          
if __name__ == "__main__":

    unittest.main(exit=False, verbosity=2)
    main() 
