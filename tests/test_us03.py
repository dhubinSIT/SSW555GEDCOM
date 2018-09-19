# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from io import StringIO
import unittest
from gedcom_types import Individual
from gedcom_parser import parse_date, parse_file
from gedcom_validation import collect_validation_warnings

class US03TestCase(unittest.TestCase):
    def shortDescription(self):
        '''Disable printing docstring on verbose'''
        return None

    def setUp(self):
        self.OkayIndi = Individual('@okay@')
        self.OkayIndi.apply_value('BIRT', parse_date('1 JUN 1945'))
        self.OkayIndi.apply_value('DEAT', parse_date('6 JAN 1995'))

        self.BadBirth = Individual('@birth@')
        self.BadBirth.apply_value('BIRT', parse_date('7 JAN 1995'))
        self.BadBirth.apply_value('DEAT', parse_date('6 JAN 1995'))

    def test_birth_before_death(self):
        '''Test warnings if date of birth is after date of death'''
        warnings = self.BadBirth._Check_Birth_Before_Death()
        self.assertEqual(len(warnings), 1)
        self.assertTrue('@birth' in warnings[0].message and 'birth date after death date' in warnings[0].message)

    def test_okay_individual(self):
        '''Test warnings if date of birth is after date of death'''
        warnings = self.OkayIndi._Check_Birth_Before_Death()
        self.assertEqual(len(warnings), 0)

    def test_full_path(self):
        '''Integration test for parser->objects->validation'''
        buff = StringIO('''0 @I1@ INDI
1 NAME CrankyFrank /Coffin/
1 SEX M
1 BIRT
2 DATE 3 MAR 1986
1 DEAT
2 DATE 3 MAR 1986
1 FAMS @F1@
0 @I2@ INDI
1 NAME MarvelousMay /Coffin/
1 SEX F
1 BIRT
2 DATE 3 MAR 1986
1 DEAT
2 DATE 2 MAR 1986
1 FAMS @F1@''')
        (ind, fam, unused_warns) = parse_file(buff)
        warnings = collect_validation_warnings(ind, fam)
        count_of_us03_errors = 0
        for warn in warnings:
            if warn.story == "US03": count_of_us03_errors += 1
        self.assertEqual(count_of_us03_errors, 1)