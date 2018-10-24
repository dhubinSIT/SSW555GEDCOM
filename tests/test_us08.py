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

class US08TestCase(unittest.TestCase):
    def shortDescription(self):
        '''Disable printing docstring on verbose'''
        return None

    def setUp(self):
        self.OkayIndi = Individual('@okay@')
        self.OkayIndi.apply_value('BIRT', parse_date('1 JAN 2001'))

        self.BadIndiMarr = Individual('@badmarriage@')
        self.BadIndiMarr.apply_value('BIRT', parse_date('30 DEC 2000'))

        self.NoIndiBirth = Individual('@nobirth@')

        self.BadIndiDiv = Individual('@baddivorce@')
        self.BadIndiDiv.apply_value('BIRT', parse_date('5 OCT 2001'))

        self.MarrFam = Family('@marriedf@')
        self.MarrFam.apply_value('MARR', parse_date('1 JAN 2001'))        
        self.MarrFam.add_child_ref(self.OkayIndi)
        self.MarrFam.add_child_ref(self.BadIndiMarr)
        self.MarrFam.add_child_ref(self.NoIndiBirth)

        self.NoMarrFam = Family('@nomarriagef@')
        self.NoMarrFam.add_child_ref(self.OkayIndi)

        self.NoChildBirthFam = Family('@nochildbirthday@')
        self.NoChildBirthFam.add_child_ref(self.NoIndiBirth)

        self.NoDivFam = Family('@nodivorcef@')
        self.NoDivFam.add_child_ref(self.NoIndiBirth)

        self.DivFam = Family('@divorcedf@')
        self.DivFam.apply_value('DIV', parse_date('1 JAN 2001'))
        self.DivFam.add_child_ref(self.BadIndiDiv)


    def test_birth_before_marr(self):
        '''Test warnings if date of birth is before date of parents marriage'''
        warnings = self.MarrFam._Check_Children_Birth_After_Marriage()
        self.assertEqual(len(warnings), 1)
        self.assertTrue('@badmarriage@' in warnings[0].message and 'was born before Parents marriage date' in warnings[0].message)

    def test_no_marr(self):
        '''Test warnings if no date of marriage'''
        warnings = self.NoMarrFam._Check_Children_Birth_After_Marriage()
        self.assertEqual(len(warnings), 0)

    def test_no_birth(self):
        '''Test warnings if no date of birth'''
        warnings = self.NoChildBirthFam._Check_Children_Birth_After_Marriage()
        self.assertEqual(len(warnings), 0)

    def test_no_div(self):
        '''Test warnings if no date of divorce'''
        warnings = self.NoDivFam._Check_Children_Birth_After_Divorce()
        self.assertEqual(len(warnings), 0)

    def test_birth_after_div(self):
        '''Test warnings if date of birth is nine months after date of parents divorce'''
        warnings = self.DivFam._Check_Children_Birth_After_Divorce()
        self.assertEqual(len(warnings), 1)
        self.assertTrue('@baddivorce@' in warnings[0].message and 'was born nine months after Parents divorce date' in warnings[0].message)

    def test_full_path(self):
        '''Integration test for parser->objects->validation'''
        buff = StringIO('''0 @I1@ INDI
1 NAME CrankyFrank /Coffin/
1 SEX M
1 BIRT
2 DATE 6 OCT 1986
1 FAMS @F1@
0 @I2@ INDI
1 NAME SomethingSally /Coffin/
1 SEX F
1 BIRT
2 DATE 30 DEC 1985
1 FAMS @F1@
0 @F1@ FAM
1 MARR
2 DATE 1 JAN 1986
1 DIV
2 DATE 2 JAN 1986
1 CHIL @I1@
1 CHIL @I2@
''')
        (ind, fam, unused_warns) = parse_file(buff)
        warnings = collect_validation_warnings(ind, fam)
        count_of_us08_errors = 0
        for warn in warnings:
            if warn.story == "US08": count_of_us08_errors += 1
        self.assertEqual(count_of_us08_errors, 2)