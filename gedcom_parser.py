# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import re
import gedcom_types

# All of the valid tags in this subset of GEDCOM
# Use named part of the regexp to make extraction easy.
TAGS = [
    "(?P<level>0)\s+(?P<tag>NOTE)\s+(?P<args>.*)",
    "(?P<level>0)\s+(?P<tag>HEAD)\s*(?P<args>)",
    "(?P<level>0)\s+(?P<tag>TRLR)\s*(?P<args>)",
    "(?P<level>0)\s+(?P<args>.*)\s+(?P<tag>INDI)$",
    "(?P<level>0)\s+(?P<args>.*)\s+(?P<tag>FAM)$",

    "(?P<level>1)\s+(?P<tag>NAME)\s+(?P<args>.*)",
    "(?P<level>1)\s+(?P<tag>SEX)\s+(?P<args>.*)",
    "(?P<level>1)\s+(?P<tag>BIRT)\s+(?P<args>)",
    "(?P<level>1)\s+(?P<tag>DEAT)\s+(?P<args>)",
    "(?P<level>1)\s+(?P<tag>FAMC)\s+(?P<args>.*)",
    "(?P<level>1)\s+(?P<tag>FAMS)\s+(?P<args>.*)",
    "(?P<level>1)\s+(?P<tag>MARR)\s+(?P<args>)",
    "(?P<level>1)\s+(?P<tag>DIV)\s+(?P<args>)",
    "(?P<level>1)\s+(?P<tag>HUSB)\s+(?P<args>.*)",
    "(?P<level>1)\s+(?P<tag>WIFE)\s+(?P<args>.*)",
    "(?P<level>1)\s+(?P<tag>CHIL)\s+(?P<args>.*)",

    "(?P<level>2)\s+(?P<tag>DATE)\s+(?P<args>.*)"
]

"""Helper constants for the parser, allowing some dispatching based on function read."""
SKIPPABLE_TAGS = ["NOTE", "HEAD", "TRLR"]
DIRECT_SET_TAGS = ["NAME", "SEX", "HUSB", "WIFE", "FAMC", "FAMS", "CHIL"]
DATE_TAGS = ["BIRT", "DEAT", "MARR", "DIV"]

def Empty_Record (tag, id):
    """Helper function for making an empty record based on GEDCOM tag."""
    if tag == "INDI":
        return gedcom_types.Individual(identifier = id)
    else:
        return gedcom_types.Family (identifier = id)
    
def parse_line (line):
    """Take a single string and figure out whether it is valid."""
    for tag in TAGS:
        m = re.match(tag, line)
        if m != None:
            return gedcom_types.Validation_Results(valid = True,
                                                   level = m.group('level'),
                                                   tag = m.group('tag'),
                                                   args = m.group('args'))
        
    # Didn't match anything... try badly leveled FAM or INDI
    m = re.match("(?P<level>\d)\s+(?P<args>.*)\s+(?P<tag>INDI|FAM)$",line)

    # If that didn't work, try generic tag format, where tag is second field
    if m == None:
        m = re.match("(?P<level>\d)\s+(?P<tag>\S+)\s+(?P<args>.*)", line)
    if m != None:
        return gedcom_types.Validation_Results(valid = False,
                                              level = m.group('level'),
                                              tag = m.group('tag'),
                                              args = m.group('args'))


def parse_file (handle):
    """Parse lines from the file handle, and return a tuple of two dictionaries.
    Each dictionary (one for individuals, one for family) is keyed based on unique identifiers."""
    data = {'INDI' : {},
            'FAM' : {}}
    stack = []
    
    # Parsing the GEDCOM format is done as a stack.
    # First element => Individual or Family dictionary.
    # Second element => Unique identifier in that dictionary
    # Third element (if needed) => Which date field was just read (birth/death/etc)
    #       This element will be popped once the date is processed.
    for line in handle:
        try:
            fields = parse_line (line)
            if fields.valid:
                if fields.tag in SKIPPABLE_TAGS:
                    continue
                elif fields.level == "0":
                    data[fields.tag][fields.args] = Empty_Record(fields.tag, fields.args)
                    stack = [fields.tag,fields.args]
                elif fields.tag in DIRECT_SET_TAGS:
                    data[stack[0]][stack[1]].parse_value(fields.tag,  fields.args)
                elif fields.tag in DATE_TAGS:
                    stack.append(fields.tag)
                elif fields.tag == "DATE":
                    data[stack[0]][stack[1]].parse_value(stack.pop(), fields.args)
            else:
                print("Line failed validation (invalid tag or bad level):" + line.strip())
        except:
            print("Unknown error parsing line:" + line.strip())
    return (data['INDI'], data['FAM'])
