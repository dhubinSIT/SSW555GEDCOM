# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

def collect_validation_warnings(individuals,  families):
    """This procedure will run through every validation route
    returning the accumulated warnings.  This is separate in case
    we want to add validation routines that sit outside the classes."""
    warnings = []
    for i in individuals.values():
        warnings = warnings + i.validate()
    for f in families.values():
        warnings = warnings + f.validate()
    return warnings

