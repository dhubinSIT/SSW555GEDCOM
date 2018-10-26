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

    warnings = warnings +\
               _US02_Birth_Before_Marriage(individuals, families) +\
               _US05_Death_Before_Marriage(individuals, families) +\
               _US23_Unique_Individuals(individuals)
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

def _US23_Unique_Individuals(individuals):
    """US23: Unique name and birth date.  Only covering those individuals that have both fields defined."""
    reverse_individuals = {}
    
    for individual in filter(lambda x: x.birth != None and x.name != None, individuals.values()):
        key = individual.name + str(individual.birth)
        if key not in reverse_individuals:
            reverse_individuals[key] = [individual.id]
        else:
            reverse_individuals[key].append(individual.id)
            
    warnings = list(map(lambda group: Validation_Results("US23", "The following individuals all have the same name and birthdate: %s" % group), 
                        filter(lambda group: len(group) > 1,  reverse_individuals.values())))
    return warnings
