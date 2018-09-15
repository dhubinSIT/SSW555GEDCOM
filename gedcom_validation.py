# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import datetime
import gedcom_types

def US01_DatesBeforeCurrentDate(individuals,  families):
    today = datetime.datetime.today()
    bad_birthdays = [gedcom_types.Validation_Results('US01','Individual %s has a birthday in the future.' % x.id)
                     for x in individuals.values()
                     if x.birth != None and x.birth > today]
    bad_deaths =    [gedcom_types.Validation_Results('US01','Individual %s has a death in the future.' % x.id)
                     for x in individuals.values()
                     if x.death != None and x.death > today]
    bad_marriages = [gedcom_types.Validation_Results('US01','Family %s has a marriage in the future.' % x.id)
                     for x in families.values()
                     if x.married != None and x.married > today]
    bad_divorce =   [gedcom_types.Validation_Results('US01','Family %s has a divorce in the future.' % x.id)
                     for x in families.values()
                     if x.divorced != None and x.divorced > today]
    return bad_birthdays + bad_deaths + bad_marriages + bad_divorce

def collect_validation_warnings(individuals,  families):
    warnings = []
    
    warnings = warnings + US01_DatesBeforeCurrentDate(individuals, families)
    
    return warnings
