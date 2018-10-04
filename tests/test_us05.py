# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from io import StringIO
import unittest
from gedcom_types import Individual, Family
from gedcom_parser import parse_date, parse_file
from gedcom_validation import _US05_Death_Before_Marriage, collect_validation_warnings

class US05TestCase(unittest.TestCase):
    def shortDescription(self):
        '''Disable printing docstring on verbose'''
        return None

    def setUp(self):
        self.OkayIndi = Individual('@okay@')
        self.OkayFam = Family('@okayf@')
        self.OkayIndi.apply_value('DEAT', parse_date('6 JAN 1995'))
        self.OkayFam.apply_value('MARR', parse_date('1 JUN 1975'))
        self.OkayFam.apply_value('HUSB', '@okay@')
        self.OkayFam.add_spouse_ref('HUSB',self.OkayIndi)

        self.BadDeath = Individual('@death@')
        self.BadFam = Family('@badf@')
        self.BadDeath.apply_value('DEAT', parse_date('5 JAN 1995'))
        self.BadFam.apply_value('MARR', parse_date('6 JAN 1995'))
        self.BadFam.apply_value('HUSB', '@death@')
        self.BadFam.add_spouse_ref('HUSB', self.BadDeath)

        self.MissingDeath = Individual('@nodeath@')
        self.MissingDeathFam = Family('@badfnd@')
        self.MissingDeathFam.apply_value('MARR', parse_date('6 JAN 1995'))
        self.MissingDeathFam.apply_value('HUSB', '@nodeath@')
        self.MissingDeathFam.add_spouse_ref('HUSB', self.MissingDeath)

        self.MissingMarr = Individual('@nomarr@')
        self.MissingMarrFam = Family('@badfnm@')
        self.MissingMarr.apply_value('DEAT', parse_date('6 JAN 1995'))
        self.MissingMarrFam.apply_value('HUSB', '@nomarr@')
        self.MissingMarrFam.add_spouse_ref('HUSB', self.MissingMarr)

    def test_death_before_marr(self):
        '''Test warnings if date of death is before date of marriage'''
        warnings = _US05_Death_Before_Marriage({'@okay@' : self.OkayIndi, '@death@' : self.BadDeath},
                                               {'@okayf@' : self.OkayFam, '@badf@' : self.BadFam})
        self.assertEqual(len(warnings), 1)
        self.assertTrue('@death@' in warnings[0].message and 'death date before marriage date' in warnings[0].message)

    def test_no_death(self):
        '''Test warnings if no date of death'''
        warnings = _US05_Death_Before_Marriage({'@okay@' : self.OkayIndi, '@nodeath@' : self.MissingDeath},
                                               {'@okayf@' : self.OkayFam, '@badfnd@' : self.MissingDeathFam})
        self.assertEqual(len(warnings), 0)
        
    def test_no_marriage(self):
        '''Test warnings if no date of marriage'''
        warnings = _US05_Death_Before_Marriage({'@okay@' : self.OkayIndi, '@nomarr@' : self.MissingMarr},
                                               {'@okayf@' : self.OkayFam, '@badfnm@' : self.MissingMarrFam})
        self.assertEqual(len(warnings), 0)

    def test_okay_individual(self):
        '''Test warnings if date of birth is after date of death'''
        warnings = _US05_Death_Before_Marriage({'@okay@' : self.OkayIndi},
                                               {'@okayf@' : self.OkayFam})
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
1 NAME SomethingSally /Coffin/
1 SEX F
1 BIRT
2 DATE 1 MAR 1986
1 DEAT
2 DATE 1 MAR 1986
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 2 MAR 1986''')
        (ind, fam, unused_warns) = parse_file(buff)
        warnings = collect_validation_warnings(ind, fam)
        count_of_us05_errors = 0
        for warn in warnings:
            if warn.story == "US05": count_of_us05_errors += 1
        self.assertEqual(count_of_us05_errors, 1)