# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from io import StringIO
import unittest
from gedcom_types import Individual, Family
from gedcom_parser import parse_date, parse_file
from gedcom_validation import collect_validation_warnings

class US04TestCase(unittest.TestCase):
    def shortDescription(self):
        '''Disable printing docstring on verbose'''
        return None

    def setUp(self):
        self.OkayFam = Family('@okayf@')
        self.OkayFam.apply_value('MARR', parse_date('1 JUN 1975'))
        self.OkayFam.apply_value('DIV', parse_date('1 JUN 1975'))

        self.BadFam = Family('@badf@')
        self.BadFam.apply_value('MARR', parse_date('6 JAN 1995'))
        self.BadFam.apply_value('DIV', parse_date('5 JAN 1995'))

        self.MissingDivFam = Family('@badfnd@')
        self.MissingDivFam.apply_value('MARR', parse_date('6 JAN 1995'))

        self.MissingMarrFam = Family('@badfnm@')
        self.MissingMarrFam.apply_value('DIV', parse_date('6 JAN 1995'))

    def test_divorce_before_marr(self):
        '''Test warnings if date of marriage is after date of divorce'''
        warnings = self.BadFam._Check_Marriage_Before_Divorce()
        self.assertEqual(len(warnings), 1)
        self.assertTrue('@badf@' in warnings[0].message and 'marriage date after divorce date' in warnings[0].message)

    def test_no_divorce(self):
        '''Test warnings if no date of divorce'''
        warnings = self.MissingDivFam._Check_Marriage_Before_Divorce()
        self.assertEqual(len(warnings), 0)
        
    def test_no_marriage(self):
        '''Test warnings if no date of marriage'''
        warnings = self.MissingMarrFam._Check_Marriage_Before_Divorce()
        self.assertEqual(len(warnings), 0)
        
    def test_okay_family(self):
        '''Test warnings if date of marriage is before date of divorce'''
        warnings = self.OkayFam._Check_Marriage_Before_Divorce()
        self.assertEqual(len(warnings), 0)

    def test_full_path(self):
        '''Integration test for parser->objects->validation'''
        buff = StringIO('''0 @F1@ FAM
1 MARR
2 DATE 3 MAR 1986
1 DIV
2 DATE 3 MAR 1986
0 @F2@ FAM
1 MARR
2 DATE 3 MAR 1986
1 DIV
2 DATE 2 MAR 1986''')
        (ind, fam, unused_warns) = parse_file(buff)
        warnings = collect_validation_warnings(ind, fam)
        count_of_us04_errors = 0
        for warn in warnings:
            if warn.story == "US04": count_of_us04_errors += 1
        self.assertEqual(count_of_us04_errors, 1)