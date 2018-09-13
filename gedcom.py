# SSW 555 Project GEDCOM Parser / Validator
#
# David Hubin
# Ayana Perry
# Rakshith Varadaraju

import os
from prettytable import PrettyTable
import sys

from gedcom_types import *
from gedcom_parser import parse_file

def directfilecheck(directory):
    pt_indi = PrettyTable(field_names=['ID','Name','Gender','Birthday','Age','Alive','Death','Child','Spouse'])
    pt_fam = PrettyTable(field_names=['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife Name','Children'])
               
    for filename in os.listdir(directory):   #Python program that given a directory name, searches that directory for GEDCOM files"): 
            num_of_id, num_of_name, num_of_gender, num_of_birthday,num_of_age, num_of_alive,num_of_death,num_of_child,num_of_spouse = filecheck(directory,filename)
            pt_indi.add_row([filename,num_of_id, num_of_name, num_of_gender, num_of_birthday,num_of_age, num_of_alive,num_of_death,num_of_child,num_of_spouse])
            
            num_of_famid, num_of_married, num_of_divorced, num_of_husbandid, num_of_husbandname, num_of_wifeid, num_of_wifename, num_of_children = filecheck(directory,filename)
            pt_indi.add_row([filename,num_of_famid, num_of_married, num_of_divorced, num_of_husbandid, num_of_husbandname, num_of_wifeid, num_of_wifename, num_of_children])
    print(pt_indi)
    print(pt_fam)
          
def filecheck(directory,filename):
    try:
        f = open(os.path.join(directory, filename),mode="r", encoding="utf-8")
    except FileNotFoundError:
        print('The file cannot be opened:', f)
        return (0,0,0,0)
    else:
        with f:  #Automatically closes the file
            lines = f.readlines() 
            num_of_id = 0 
            num_of_name = 0
            num_of_gender = 0
            num_of_birthday = 0
            num_of_age = 0 
            num_of_alive = 0
            num_of_death = 0
            num_of_child = 0
            num_of_spouse = 0
            num_of_famid = 0
            num_of_married = 0
            num_of_husbandid = 0
            num_of_husbandname = 0 
            num_of_wifeid = 0
            num_of_wifename = 0
            num_of_children = 0
            (indi, fam) = parse_file(f)
            
            for x in indi:
                print(indi[x])
                num_of_id += 1
                num_of_name += 1
                num_of_gender += 1
                num_of_birthday += 1
                num_of_age += 1 
                num_of_alive += 1
                num_of_death += 1
                num_of_child += 1
                num_of_spouse += 1
                line = line.strip().lower()  # from left and right
            return (num_of_id, num_of_name, num_of_gender, num_of_birthday,num_of_age, num_of_alive, num_of_death, num_of_child, num_of_spouse)
            print
            
            for x in fam:
                print(fam[x])
                num_of_famid += 1
                num_of_married += 1
                num_of_divorced += 1
                num_of_husbandid += 1
                num_of_husbandname += 1 
                num_of_wifeid += 1
                num_of_wifename += 1
                num_of_children += 1
                line = line.strip().lower()  # from left and right
            return (num_of_famid, num_of_married, num_of_divorced, num_of_husbandid, num_of_husbandname, num_of_wifeid, num_of_wifename, num_of_children)
                
#Main function results:
def main():
    directfilecheck(sys.argv[1])
if __name__ == "__main__":
    main()    





