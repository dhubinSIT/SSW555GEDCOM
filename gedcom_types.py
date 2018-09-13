# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from collections import namedtuple

# Pass around named fields for ease of use (probably overkill)
Validation_Results = namedtuple("Validation_Results", ['valid', 'level', 'tag', 'args'])

class Individual:
    
    # Map GEDCOM tag into instance fields (currently 1:1)
    TAG_MAP = {
        "NAME": "name",
        "SEX" : "gender",
        "BIRT" : "birth",
        "DEAT" : "death",
        "FAMC" : "child_family_ids",
        "FAMS" : "spouse_family_ids"
    }
    
    def __init__(self, identifier):
        self.id = identifier
        self.name = None
        self.gender = None
        self.birth = None
        self.death = None
        self.child_family_ids = []
        self.spouse_family_ids = []
        
    def __str__(self):
        return self.id + " name=" + self.name + " dob=" + str(self.birth) + \
        " child-of=" + str(self.child_family_ids) + " spouse-of=" + str(self.spouse_family_ids)
     
    # Right now, just push values as strings straight into the fields.
    # Parsing into dates/etc can come later.
    def parse_value(self, gedcomTag,  gedcomValue):
        if gedcomTag == "FAMC":
            self.child_family_ids.append(gedcomValue)
        elif gedcomTag == "FAMS":
            self.spouse_family_ids.append(gedcomValue)
        else:
            setattr(self, Individual.TAG_MAP[gedcomTag], gedcomValue)

class Family:
    
    # Map GEDCOM tag into instance fields (currently 1:1)
    TAG_MAP = {
        "MARR" : "married",
        "DIV"  : "divorced",
        "HUSB" : "husband_id",
        "WIFE" : "wife_id"
    }
    
    def __init__(self, identifier):
        self.id = identifier
        self.married = None
        self.divorced = None
        self.husband_id = None
        self.wife_id = None
        self.children_id_list = []
        
    def __str__(self):
        return self.id + " husb=" + str(self.husband_id) + " wife=" + str(self.wife_id) + " children=" + str(self.children_id_list)
    
    # Right now, just push values as strings straight into the fields.
    # Parsing into dates/etc can come later.
    def parse_value(self, gedcomTag,  gedcomValue):
        if gedcomTag == "CHIL":
            self.children_id_list.append(gedcomValue)
        else:
            setattr(self, Family.TAG_MAP[gedcomTag], gedcomValue)

