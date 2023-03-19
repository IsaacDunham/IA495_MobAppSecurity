#!/usr/bin/python

#this script will initiate mobsfscan, saving its json file to
# to scan_results.json. Then, it will kickstart our custom scripts to append
# edge case results to the json file. Finally, it will produce a PDF report.

### Imports ###
from subprocess import Popen, PIPE
import sys
import os
edgecases_dir = os.getcwd() + "/edge_cases/"
current_dir = os.getcwd() + "/"


### Static Variables ###
outpath = current_dir + "scan_results.json"


#Run mobsfscan and output JSON file


if len(sys.argv) < 2:
                print("Usage: " + sys.argv[0] + " root directory of mobile application")
                sys.exit(1)

#Checking that exists and is correct
path = os.path.dirname(sys.argv[1])

if not os.path.exists(path):
        print("Error: " + path + " does not exist")
        sys.exit(1)


p = Popen(["mobsfscan", "--json", "-o", outpath, path], stdout=PIPE,
                        stderr=PIPE)
output, err = p.communicate()
rc = p.returncode

"""if rc != 0: mobfscan is expected to have a non-zero return code, for now
    print("Error: " + str(err))
    print("mobsfscan failed")
    sys.exit(1)
"""
    
#Run edge case scripts
os.system(edgecases_dir + "targetSdkVersion.py " + path)


#Run report script
os.system(current_dir + "make_pdf.py")