# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from io import StringIO
import unittest
from gedcom_parser import parse_file
from gedcom_validation import collect_validation_warnings

class US26TestCase(unittest.TestCase):
    def shortDescription(self):
        """Disable printing docstring on verbose."""
        return None
        
    def test_mismatched_family_references(self):
        """Test mismatched references.  The family has husband, wife, child, child, but
        the individual objects think they are child, child, husband, wife."""
        buff = StringIO("""0 @I1@ INDI
1 FAMC @F1@
0 @I2@ INDI
1 FAMC @F1@
0 @I3@ INDI
1 FAMS @F1@
0 @I4@ INDI
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
1 CHIL @I4@""")
        (ind,  fam,  unused_warns) = parse_file(buff)
        fam_warns = fam['@F1@']._Check_References()
        self.assertTrue(len([x for x in fam_warns if x.story == "US26"]) == 4) # all four individuals mismatched.
        self.assertTrue(len([x for x in fam_warns if "@I1@" in x.message and "husband" in x.message]) == 1) # mismatch of husband
        self.assertTrue(len([x for x in fam_warns if "@I2@" in x.message and "wife" in x.message]) == 1) # mismatch of wife
        self.assertTrue(len([x for x in fam_warns if "@I3@" in x.message and "child" in x.message]) == 1) # mismatch of child
        self.assertTrue(len([x for x in fam_warns if "@I4@" in x.message and "child" in x.message]) == 1) # mismatch of other child
        
    def test_mismatched_individual_references(self):
        """Test mismatched references.  The individual I1 should be a spouse of the family,
        and I2 should be a child of the family, but the family has them in opposite roles."""
        buff = StringIO("""0 @I1@ INDI
1 FAMS @F1@
0 @I2@ INDI
1 FAMC @F1@
0 @F1@ FAM
1 WIFE @I2@
1 CHIL @I1@""")
        (ind,  fam,  unused_warns) = parse_file(buff)
        ind1_warns = ind['@I1@']._Check_References()
        self.assertTrue(len([x for x in ind1_warns if x.story == "US26"]) == 1) # ind1 isn't a spouse of fam1
        self.assertTrue(len([x for x in ind1_warns if "@F1@" in x.message and "spouse" in x.message]) == 1) # ind1 isn't a spouse of fam1
        ind2_warns = ind['@I2@']._Check_References()
        self.assertTrue(len([x for x in ind2_warns if x.story == "US26"]) == 1) # ind2 isn't a child of fam1
        self.assertTrue(len([x for x in ind2_warns if "@F1@" in x.message and "child" in x.message]) == 1) # ind2 isn't a spouse of fam1
        
    def test_missing_references(self):
        """Test references which are missing altogether. 
        These are just the parser warnings for missing individuals."""
        buff = StringIO("""0 @I1@ INDI
1 FAMS @FmissingS@
1 FAMC @FmissingC@
0 @F1@ FAM
1 WIFE @ImissingW@
1 HUSB @ImissingH@
1 CHIL @ImissingC@""")
        (ind,  fam,  warns) = parse_file(buff)
        self.assertTrue(len([x for x in warns if x.story == "US26"]) == 5)
        self.assertTrue(ind['@I1@'].spouse_family_ids == [])
        self.assertTrue(ind['@I1@'].spouse_families == [])
        self.assertTrue(ind['@I1@'].child_family_ids == [])
        self.assertTrue(ind['@I1@'].child_families == [])
        self.assertTrue(fam['@F1@'].husband_id == None)
        self.assertTrue(fam['@F1@'].husband == None)
        self.assertTrue(fam['@F1@'].wife_id == None)
        self.assertTrue(fam['@F1@'].wife == None)
        self.assertTrue(fam['@F1@'].children_id_list == [])
        self.assertTrue(fam['@F1@'].children_list == [])
        
    def test_everything_fine(self):
        """Test that an okay GEDCOM file is reported with no warnings."""
        buff = StringIO("""0 @I1@ INDI
1 FAMC @F1@
0 @I2@ INDI
1 FAMC @F1@
0 @I3@ INDI
1 FAMS @F1@
0 @I4@ INDI
1 FAMS @F1@
0 @F1@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I1@
1 CHIL @I2@""")
        (ind,  fam,  warns) = parse_file(buff)
        validation_warns = collect_validation_warnings(ind,  fam)
        us26_warns = [x for x in warns + validation_warns if x.story == "US26"]
        self.assertTrue(len(us26_warns) == 0)
        
        self.assertTrue(fam['@F1@'] in ind['@I1@'].child_families)
        self.assertTrue(fam['@F1@'] in ind['@I2@'].child_families)
        self.assertTrue(fam['@F1@'] in ind['@I3@'].spouse_families)
        self.assertTrue(fam['@F1@'] in ind['@I4@'].spouse_families)
        
        self.assertTrue(ind['@I3@'] == fam['@F1@'].husband)
        self.assertTrue(ind['@I4@'] == fam['@F1@'].wife)
        self.assertTrue(ind['@I1@'] in fam['@F1@'].children_list)
        self.assertTrue(ind['@I2@'] in fam['@F1@'].children_list)
        
