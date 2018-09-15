# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from io import StringIO
import unittest
from gedcom_parser import parse_file,  parse_date
from gedcom_validation import collect_validation_warnings
from gedcom_types import Family,  Individual

class US01TestCase(unittest.TestCase):
    def setUp(self):
        self.OkayIndi = Individual("@okay@")
        self.OkayIndi.apply_value("BIRT", parse_date("1 JUN 1945"))
        self.OkayIndi.apply_value("DEAT", parse_date("6 JAN 1995"))
        
        self.BadBirth = Individual("@birth@")
        self.BadBirth.apply_value("BIRT", parse_date("1 JAN 2525"))
        
        self.BadDeath = Individual("@death@")
        self.BadDeath.apply_value("BIRT", parse_date("1 JUN 1945"))
        self.BadDeath.apply_value("DEAT", parse_date("1 JAN 4545"))
        
        self.OkayFam = Family("@okayf@")
        self.OkayFam.apply_value("MARR", parse_date("15 SEP 1960"))
        self.OkayFam.apply_value("DIV", parse_date("15 SEP 1970"))
        
        self.BadMarr = Family("@badmarr@")
        self.BadMarr.apply_value("MARR", parse_date("15 SEP 2960"))
        
        self.BadDiv = Family("@baddiv@")
        self.BadDiv.apply_value("DIV", parse_date("15 SEP 2970"))
        
        self.DoubleBadIndi = Individual("@doubleIndi@")
        self.DoubleBadIndi.apply_value("BIRT", parse_date("1 JUN 3945"))
        self.DoubleBadIndi.apply_value("DEAT", parse_date("1 JAN 4545"))
        
        self.DoubleBadFam = Family("@doubleFam@")
        self.DoubleBadFam.apply_value("MARR", parse_date("15 SEP 2960"))
        self.DoubleBadFam.apply_value("DIV", parse_date("15 SEP 2970"))
    
    def test_birth(self):
        warnings = self.BadBirth._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  1)
        self.assertTrue('@birth@' in warnings[0].message and "birth date" in warnings[0].message)

    def test_death(self):
        warnings = self.BadDeath._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  1)
        self.assertTrue('@death@' in warnings[0].message and "death date" in warnings[0].message)
        
    def test_okay_individual(self):
        warnings = self.OkayIndi._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  0)
    
    def test_marriage(self):
        warnings = self.BadMarr._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  1)
        self.assertTrue('@badmarr@' in warnings[0].message and "marriage date" in warnings[0].message)

    def test_divorce(self):
        warnings = self.BadDiv._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  1)
        self.assertTrue('@baddiv@' in warnings[0].message and "divorce date" in warnings[0].message)

    def test_double_warnings(self):
        warnings = self.DoubleBadFam._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  2)
        
        warnings = self.DoubleBadIndi._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  2)   
        
    def test_okay_family(self):
        warnings = self.OkayFam._Check_Dates_Before_Today()
        self.assertEqual(len(warnings),  0)
        
    def test_full_path(self):
        buff = StringIO("""0 @I1@ INDI
1 NAME CrankyFrank /Coffin/
1 SEX M
1 BIRT
2 DATE 2 JAN 2940
1 FAMS @F1@
0 @I2@ INDI
1 NAME MarvelousMay /Coffin/
1 SEX F
1 BIRT
2 DATE 15 MAY 2941
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
2 DATE 15 JUL 2972
1 DIV
2 DATE 15 JUL 2973""")
        (ind,  fam) = parse_file(buff)
        warnings = collect_validation_warnings(ind,  fam)
        count_of_us01_errors = 0
        for warn in warnings:
            if warn.story == "US01": count_of_us01_errors += 1
        self.assertEqual(count_of_us01_errors,  4)
        
