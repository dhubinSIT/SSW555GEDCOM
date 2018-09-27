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

    warnings = warnings + _US02_Birth_Before_Marriage(individuals, families)
    return warnings

def _US02_Birth_Before_Marriage(individuals, families):
    warnings = []
    for fam in families:
        if families[fam].married != None:
            if families[fam].husband_id != None and individuals[families[fam].husband_id].birth != None and individuals[families[fam].husband_id].birth > families[fam].married:
                warnings.append(Validation_Results("US02", 'Individual %s has a birth date after marriage date.' % families[fam].husband_id))
            if families[fam].wife_id != None and individuals[families[fam].wife_id].birth != None and individuals[families[fam].wife_id].birth > families[fam].married:
                warnings.append(Validation_Results("US02", 'Individual %s has a birth date after marriage date.' % families[fam].wife_id))        
    return warnings
