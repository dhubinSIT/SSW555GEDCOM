# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from collections import namedtuple

# Pass around named fields for ease of use (probably overkill)
Validation_Results = namedtuple("Validation_Results", ['valid', 'level', 'tag', 'args'])

class Individual:
    '''This is a datastructure that holds information about an individual.
    It currently saves data about the individual identifier, individual name,
    date of birth, date of death, family id of any children, and
    family id of any spouse'''
    
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
        
    # Right now, just push values as strings straight into the fields.
    # Parsing into dates/etc can come later.
    def parse_value(self, gedcomTag,  gedcomValue):
        '''This function determines which fields to add into the individual
        record. If it is a child or spouse record, it will be added to the 
        ids list. Otherwise the remaining tags will be added as the 
        individual record attributes'''
        if gedcomTag == "FAMC":
            self.child_family_ids.append(gedcomValue)
        elif gedcomTag == "FAMS":
            self.spouse_family_ids.append(gedcomValue)
        else:
            setattr(self, Individual.TAG_MAP[gedcomTag], gedcomValue)

class Family:
    '''This is a datastructure to store information about a family.
    The datastructure currently holds values of family id, date of 
    marriage, date of divorce, husband id, wife id, and children ids'''
    
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
        
    # Right now, just push values as strings straight into the fields.
    # Parsing into dates/etc can come later.
    def parse_value(self, gedcomTag,  gedcomValue):
        '''This function determines which fields to add to the family
        record. If it encounters children ids, it adds it to the children
        list. Otherwise, if adds it as new data to the family record'''
        if gedcomTag == "CHIL":
            self.children_id_list.append(gedcomValue)
        else:
            setattr(self, Family.TAG_MAP[gedcomTag], gedcomValue)

