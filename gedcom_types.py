# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

from collections import namedtuple
from datetime import datetime,  timedelta

# Pass around named fields for ease of use (probably overkill)
Parser_Results = namedtuple("Parser_Results", ['valid', 'level', 'tag', 'args'])

Validation_Results = namedtuple("Validation_Results", ['story',  'message'])
"""Holder for validation issues."""

class GedcomDate(datetime):
    """This subclass of datetime is intended to provide functionality
    specific to the parsing, rendering, and validation of GEDCOM datestrings."""
    
    # How one deals with subclassing an immutable object class was not entirely obvious.
    # https://stackoverflow.com/questions/399022/why-cant-i-subclass-datetime-date
    def __new__(cls, datestring):
        """Create a new GedcomDate based on a GEDCOM datestring"""
        value = datetime.strptime(datestring, "%d %b %Y")
        return datetime.__new__(cls, value.year, value.month, value.day)
    
    def __str__(self):
        """Return a string of this object's date."""
        return datetime.strftime(self, "%d %b %Y")

    def isDateInPast(self):
        """Return True if the date is in the past."""
        return self < datetime.today()

    def isDateGreaterThan(self, comparedate):
        '''Return True if Date is greater than date to compare'''
        return comparedate != None and self > comparedate

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
        self.child_families = []
        self.spouse_family_ids = []
        self.spouse_families = []
        
    def apply_value(self, gedcomTag,  value):
        '''This function determines which fields to add into the individual
        record. If it is a child or spouse record, it will be added to the 
        ids list. Otherwise the remaining tags will be added as the 
        individual record attributes.
        
        Values are expected to be strings, except for dates, which should be datetime objects.'''
        if gedcomTag == "FAMC":
            self.child_family_ids.append(value)
        elif gedcomTag == "FAMS":
            self.spouse_family_ids.append(value)
        else:
            setattr(self, Individual.TAG_MAP[gedcomTag], value)

    def add_family_ref(self, gedcomTag, ref):
        """Add an object reference for the associated tag."""
        if gedcomTag == "FAMC":
            self.child_families.append(ref)
        elif gedcomTag == "FAMS":
            self.spouse_families.append(ref)

    def validate(self):
        '''This function checks for the following errors
        US01 : Dates before current date.
        US03 : Birth should occur before death of an individual'''
        return self._Check_Dates_Before_Today() + self._Check_Birth_Before_Death() +\
               self._Check_References() # + self._Next_Validation_Routine()...

    def _Check_Dates_Before_Today(self):
        """Validation routine for US01 : Dates before current date."""
        warnings = []
        if self.birth != None and not self.birth.isDateInPast():
            warnings.append(Validation_Results("US01", 'Individual %s has a birth date in the future.' % self.id))
        if self.death != None and not self.death.isDateInPast():
            warnings.append(Validation_Results("US01", 'Individual %s has a death date in the future.' % self.id))
        return warnings

    def _Check_Birth_Before_Death(self):
        '''Validation routine for US03 : Birth date before Death date'''
        warnings = []
        if self.birth != None and self.birth.isDateGreaterThan(self.death):
            warnings.append(Validation_Results("US03", 'Individual %s has a birth date after death date.' % self.id))
        return warnings
        
    def _Check_References(self):
        warnings = []
        for fam in self.spouse_families:
            if self != fam.husband and self != fam.wife:
                warnings.append(Validation_Results("US26",  "Individual %s references family %s as a spouse, but family does not have same reference." % (self.id,  fam.id)))
        for fam in self.child_families:
            if self not in fam.children_list:
                warnings.append(Validation_Results("US26",  "Individual %s references family %s as a child, but family does not have same reference." % (self.id,  fam.id)))
        return warnings
        
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
        self.husband = None
        self.wife_id = None
        self.wife = None
        self.children_id_list = []
        self.children_list = []
        
    def apply_value(self, gedcomTag,  value):
        '''This function determines which fields to add to the family
        record. If it encounters children ids, it adds it to the children
        list. Otherwise, if adds it as new data to the family record.
        
        Values are expected to be strings, except for dates, which should be datetime objects.'''
        if gedcomTag == "CHIL":
            self.children_id_list.append(value)
        else:
            setattr(self, Family.TAG_MAP[gedcomTag], value)

    def add_spouse_ref(self, gedcomTag, ref):
        """Add an object reference to the associated tag field."""
        if gedcomTag == "HUSB":
            self.husband = ref
        elif gedcomTag == "WIFE":
            self.wife = ref
            
    def add_child_ref(self,  ref):
        """Add an object reference for a child."""
        self.children_list.append(ref)

    def validate(self):
        '''This function checks for all family-supported errors.'''        
        return self._Check_Dates_Before_Today() +\
               self._Check_References() +\
               self._Check_Marriage_Before_Divorce() +\
               self._Check_Excessive_Siblings() +\
               self._Check_Parent_Child_Relative_Ages() +\
               self._Check_Children_Birth_After_Marriage() +\
               self._Check_Children_Birth_After_Divorce() +\
               self._Check_Children_Birth_Before_Parent_Death() +\
               self._Check_Familial_Roles()
                # + self._Next_Validation_Routine()...
        
    def _Check_Dates_Before_Today(self):
        """Validation routine for US01 : Dates before current date."""
        warnings = []
        if self.married != None and not self.married.isDateInPast():
            warnings.append(Validation_Results("US01", 'Family %s has a marriage date in the future.' % self.id))
        if self.divorced != None and not self.divorced.isDateInPast():
            warnings.append(Validation_Results("US01", 'Family %s has a divorce date in the future.' % self.id))
        return warnings
        
    def _Check_References(self):
        '''Validation routine for US26: All family roles (spouse, child) specified in an
        individual record should have corresponding entries in the corresponding family
        records. Likewise, all individual roles (spouse, child) specified in family records
        should have corresponding entries in the corresponding  individual's records.
        I.e. the information in the individual and family records should be consistent.'''
        warnings = []
        if self.husband != None and self not in self.husband.spouse_families:
            warnings.append(Validation_Results("US26",  "Family %s references husband %s, but husband does not reference family." % (self.id,  self.husband_id)))
        if self.wife != None and self not in self.wife.spouse_families:
            warnings.append(Validation_Results("US26",  "Family %s references wife %s, but wife does not reference family." % (self.id,  self.wife_id)))
        for child in self.children_list:
            if self not in child.child_families:
                warnings.append(Validation_Results("US26",  "Family %s references child %s, but child does not reference family." % (self.id,  child.id)))
        return warnings

    def _Check_Marriage_Before_Divorce(self):
        '''Validation routine for US04: Marriage date before Divorce date'''
        warnings = []
        if self.married != None and self.married.isDateGreaterThan(self.divorced):
            warnings.append(Validation_Results("US04", 'Family %s has a marriage date after divorce date.' % self.id))
        return warnings

    def _Check_Excessive_Siblings(self):
        '''Validation routine for US15: There should be fewer than 15 siblings in a family.'''
        warnings = []
        if len(self.children_list) >= 15:
            warnings.append(Validation_Results("US15", "Family %s has a suspiciously large number of children (%d)" % (self.id, len(self.children_list))))
        return warnings

    def _Check_Parent_Child_Relative_Ages(self):
        warnings = []
        if self.husband != None and self.husband.birth != None:
            for child in self.children_list:
                if child.birth != None and (self.husband.birth + timedelta(80 * 365.25)) <= child.birth:
                    warnings.append(Validation_Results("US12", "Father %s of %s is suspiciously old at the time of birth." % (self.husband.id,  child.id)))
        if self.wife != None and self.wife.birth != None:
            for child in self.children_list:
                if child.birth != None and (self.wife.birth + timedelta(60 * 365.25)) <= child.birth:
                    warnings.append(Validation_Results("US12", "Mother %s of %s is suspiciously old at the time of birth." % (self.wife.id,  child.id)))
        return warnings

    def _Check_Children_Birth_After_Marriage(self):
        '''Validation routine for US08: Birth after marriage of parents'''
        warnings = []
        if self.married != None:
            for child in self.children_list:
                if child.birth != None and child.birth < self.married:
                    warnings.append(Validation_Results("US08", 'Child %s was born before Parents marriage date.' % child.id))
        return warnings

    def _Check_Children_Birth_After_Divorce(self):
        '''Validation routine for US08: Birth Nine months after divorce of parents'''
        warnings = []
        if self.divorced != None:
            for child in self.children_list:
                if child.birth != None and child.birth > (self.divorced + timedelta(274)):
                    warnings.append(Validation_Results("US08", 'Child %s was born nine months after Parents divorce date' % child.id))
        return warnings

    def _Check_Children_Birth_Before_Parent_Death(self):
        '''Validation routine for US09: Birth before death of parents'''
        warnings = []
        if self.wife != None and self.wife.death != None:
            for child in self.children_list:
                if child.birth != None and child.birth > self.wife.death:
                    warnings.append(Validation_Results("US09", 'Child %s was born after Mothers death' % child.id))

        if self.husband != None and self.husband.death != None:
            for child in self.children_list:
                if child.birth != None and child.birth > (self.husband.death + timedelta(274)):
                    warnings.append(Validation_Results("US09", 'Child %s was born nine months after Fathers death' % child.id))

        return warnings

    def _Check_Familial_Roles(self):
        """Validation routine for US21: Correct gender for role"""
        warnings = []
        if self.wife != None and self.wife.gender != None and self.wife.gender != "F":
            warnings.append(Validation_Results("US21", "Wife %s of family %s isn't female." % (self.wife.id, self.id)))
        if self.husband != None and self.husband.gender != None and self.husband.gender != "M":
            warnings.append(Validation_Results("US21", "Husband %s of family %s isn't male." % (self.husband.id, self.id)))
        return warnings
