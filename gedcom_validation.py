# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju
from gedcom_types import Validation_Results

def collect_validation_warnings(individuals,  families):
    """This procedure will run through every validation routine
    returning the accumulated warnings.  This is separate in case
    we want to add validation routines that sit outside the classes."""
    warnings = []
    for i in individuals.values():
        warnings = warnings + i.validate()
    for f in families.values():
        warnings = warnings + f.validate()

    warnings = warnings + _US02_Birth_Before_Marriage(individuals, families) + _US05_Death_Before_Marriage(individuals, families)
    return warnings

def _US02_Birth_Before_Marriage(individuals, families):
    warnings = []
    for fam in families:
        if families[fam].married != None:
            if families[fam].husband_id != None and families[fam].husband.birth != None and families[fam].husband.birth > families[fam].married:
                warnings.append(Validation_Results("US02", 'Individual %s has a birth date after marriage date.' % families[fam].husband_id))
            if families[fam].wife_id != None and families[fam].wife.birth != None and families[fam].wife.birth > families[fam].married:
                warnings.append(Validation_Results("US02", 'Individual %s has a birth date after marriage date.' % families[fam].wife_id))
    return warnings

def _US05_Death_Before_Marriage(individuals, families):
    warnings = []
    for fam in families:
        if families[fam].married != None:
            if families[fam].husband_id != None and families[fam].husband.death != None and families[fam].husband.death < families[fam].married:
                warnings.append(Validation_Results("US05", 'Individual %s has a death date before marriage date.' % families[fam].husband_id))
            if families[fam].wife_id != None and families[fam].wife.death != None and families[fam].wife.death < families[fam].married:
                warnings.append(Validation_Results("US05", 'Individual %s has a death date before marriage date.' % families[fam].wife_id))        
    return warnings
