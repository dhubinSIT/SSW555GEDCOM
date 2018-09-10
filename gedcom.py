# David Hubin
# SSW 555 Project 2
# GEDCOM Validator

from collections import namedtuple
import re
import sys

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

# Pass around named fields for ease of use (probably overkill)
Validation_Results = namedtuple("Validation_Results", ['valid', 'level', 'tag', 'args'])

# Take a single string and figure out whether it is valid.
def validate_line(line):
    for tag in TAGS:
        m = re.match(tag, line)
        if m != None:
            return Validation_Results(valid = "Y",
                                      level = m.group('level'),
                                      tag = m.group('tag'),
                                      args = m.group('args'))
        
    # Didn't match anything... try badly leveled FAM or INDI
    m = re.match("(?P<level>\d)\s+(?P<args>.*)\s+(?P<tag>INDI|FAM)$",line)

    # If that didn't work, try generic tag format, where tag is second field
    if m == None:
        m = re.match("(?P<level>\d)\s+(?P<tag>\S+)\s+(?P<args>.*)", line)
    if m != None:
        return Validation_Results(valid = "N",
                                  level = m.group('level'),
                                  tag = m.group('tag'),
                                  args = m.group('args'))

if __name__ == "__main__":
    with open (sys.argv[1], 'r') as f:
        for line in f:
            print "--> %s" % line,
            results = validate_line(line)
            print "<-- %s|%s|%s|%s" % (results.level, results.tag, results.valid, results.args)

