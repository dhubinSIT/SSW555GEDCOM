# David Hubin
# SSW 555 Project 2
# GEDCOM Validator

import re
from gedcom_types import *

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

SKIPPABLE_TAGS = ["NOTE", "HEAD", "TRLR"]
DIRECT_SET_TAGS = ["NAME", "SEX", "HUSB", "WIFE", "FAMC", "FAMS", "CHIL"]
DATE_TAGS = ["BIRT", "DEAT", "MARR", "DIV"]

def Empty_Record (tag, id):
    if tag == "INDI":
        return Individual(identifier = id)
    else:
        return Family (identifier = id)
    
# Take a single string and figure out whether it is valid.
def parse_line (line):
    for tag in TAGS:
        m = re.match(tag, line)
        if m != None:
            return Validation_Results(valid = True,
                                      level = m.group('level'),
                                      tag = m.group('tag'),
                                      args = m.group('args'))
        
    # Didn't match anything... try badly leveled FAM or INDI
    m = re.match("(?P<level>\d)\s+(?P<args>.*)\s+(?P<tag>INDI|FAM)$",line)

    # If that didn't work, try generic tag format, where tag is second field
    if m == None:
        m = re.match("(?P<level>\d)\s+(?P<tag>\S+)\s+(?P<args>.*)", line)
    if m != None:
        return Validation_Results(valid = False,
                                  level = m.group('level'),
                                  tag = m.group('tag'),
                                  args = m.group('args'))


def parse_file (handle):
    data = {'INDI' : {},
            'FAM' : {}}
    stack = []
    
    for line in handle:
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
            print("Unknown tag:" + fields.tag)
    
    return (data['INDI'], data['FAM'])
