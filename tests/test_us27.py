# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import unittest
from gedcom_types import Individual
from datetime import datetime, timedelta
from gedcom_parser import parse_date

class US27TestCase(unittest.TestCase):
    def shortDescription(self):
        """Disable printing docstring on verbose."""
        return None
    
    def test_missing_birth_and_death(self):
        self.missingDetailsIndi = Individual('@missingDetails')
        self.missingDetailsIndi._update_individual_age()
        self.assertEqual(None, self.missingDetailsIndi.age)

    def test_birth_and_death(self):
        self.birthDeathIndi = Individual('@birthDeathIndi')
        self.birthDeathIndi.apply_value('BIRT', parse_date('1 JAN 2017'))
        self.birthDeathIndi.apply_value('DEAT', parse_date('31 DEC 2017'))
        self.assertEqual(0, self.birthDeathIndi.age)
        self.birthDeathIndi.apply_value('DEAT', parse_date('1 JAN 2018'))
        self.assertEqual(1, self.birthDeathIndi.age)

    def test_birth(self):
        self.birthIndi = Individual('@birthIndi')
        self.birthIndi.apply_value('BIRT', datetime.now() - timedelta(days = 364))
        self.assertEqual(0, self.birthIndi.age)
        self.birthIndi.apply_value('BIRT', datetime.now() - timedelta(days = 365))
        self.assertEqual(1, self.birthIndi.age)

