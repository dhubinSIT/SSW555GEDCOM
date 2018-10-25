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

class US09TestCase(unittest.TestCase):
    def shortDescription(self):
        '''Disable printing docstring on verbose'''
        return None

    def setUp(self):
        
        self.Mother = Individual('@okayMom@')
        self.Mother.apply_value('DEAT', parse_date('1 SEP 1995'))
        self.Father = Individual('@okayFather@')
        self.Father.apply_value('DEAT', parse_date('1 JAN 1995'))
        self.childafterMomDeath = Individual('@birthafterMomdeath@')
        self.childafterMomDeath.apply_value('BIRT', parse_date('2 SEP 1995'))
        self.childafterFatherDeath = Individual('@birthafterDaddeath@')
        self.childafterFatherDeath.apply_value('BIRT', parse_date('1 NOV 1995'))
        self.BadFam = Family('@badchildbirth@')
        self.BadFam.add_spouse_ref('HUSB',self.Father)
        self.BadFam.add_spouse_ref('WIFE',self.Mother)
        self.BadFam.add_child_ref(self.childafterMomDeath)
        self.BadFam.add_child_ref(self.childafterFatherDeath)

    def test_birth_after_parents_death(self):
        '''Test warnings if date of birth is after death of parents'''
        warnings = self.BadFam._Check_Children_Birth_Before_Parent_Death()
        self.assertEqual(len(warnings), 3)
        self.assertTrue('@birthafterMomdeath@' in warnings[0].message and 'was born after Mothers death' in warnings[0].message)
        self.assertTrue('@birthafterDaddeath@' in warnings[1].message and 'was born after Mothers death' in warnings[1].message)
        self.assertTrue('@birthafterDaddeath@' in warnings[2].message and 'was born nine months after Fathers death' in warnings[2].message)

    def test_full_path(self):
        '''Integration test for parser->objects->validation'''
        buff = StringIO('''0 @I1@ INDI
1 NAME CrankyFrank /Coffin/
1 DEAT
2 DATE 1 SEP 1995
0 @I2@ INDI
1 NAME SomethingSally /Coffin/
1 DEAT
2 DATE 1 JAN 1995
0 @I3@ INDI
1 NAME Maddye /Simmons/
1 BIRT
2 DATE 2 SEP 1995
0 @I4@ INDI
1 NAME Derek /Simmons/
1 BIRT
2 DATE 1 NOV 1995
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I1@
1 CHIL @I3@
1 CHIL @I4@''')
        (ind, fam, unused_warns) = parse_file(buff)
        warnings = collect_validation_warnings(ind, fam)
        count_of_us09_errors = 0
        for warn in warnings:
            if warn.story == "US09": count_of_us09_errors += 1
        self.assertEqual(count_of_us09_errors, 3)