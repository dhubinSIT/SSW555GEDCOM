# David Hubin
# SSW 555 Project 2
# GEDCOM Validator

from collections import namedtuple

# Pass around named fields for ease of use (probably overkill)
Validation_Results = namedtuple("Validation_Results", ['valid', 'level', 'tag', 'args'])

class Individual:
    def __init__(self, identifier):
        self.id = identifier
        self.name = None
        self.gender = None
        self.birth = None
        self.death = None
        self.child_family_id = None
        self.spouse_family_id = None
    def __str__(self):
        return self.id + " name=" + self.name + self.birth

class Family:
    def __init__(self, identifier):
        self.id = identifier
        self.married = None
        self.divorced = None
        self.husband_id = None
        self.wife_id = None
        self.children_id_list = None
    def __str__(self):
        return self.id + self.husband_id + self.wife_id

