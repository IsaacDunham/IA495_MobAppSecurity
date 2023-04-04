#!/usr/bin/python3.8

# this script will initiate mobsfscan, saving its json file to
# to scan_results.json. Then, it will kickstart our custom scripts to append
# edge case results to the json file. Finally, it will produce a PDF report.

### Imports ###
from subprocess import Popen, PIPE
import sys
import os
import glob
edgecases_dir = os.getcwd() + "/edge_cases/"
current_dir = os.getcwd() + "/"


### Static Variables ###
outpath = current_dir + "scan_results.json"
best_practices_dir = current_dir + "semgrep/"


# Run mobsfscan and output JSON file


if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " root directory of mobile application")
    sys.exit(1)

# Ending in a slash ensures glob works correctly
if (sys.argv[1][-1] != "/"):
    print("Please provide a trailing slash to the provided directory.")
    sys.exit(1)

# Checking that exists and is correct
path = os.path.dirname(sys.argv[1])

if not os.path.exists(path):
    print("Error: " + path + " does not exist")
    sys.exit(1)


p = Popen(["mobsfscan", "--json", "-o", outpath, path], stdout=PIPE,
          stderr=PIPE)
output, err = p.communicate()
rc = p.returncode

"""if rc != 0: mobsfscan is expected to have a non-zero return code, for now
    print("Error: " + str(err))
    print("mobsfscan failed")
    sys.exit(1)
"""

# Run edge case scripts

scripts = []
for f in glob.glob(edgecases_dir + "*.py", recursive=True):
    scripts += [f]
scripts.sort()

for script in scripts:
    os.system(script + " " + path)

# Perform custom semgrep scans -- best practices
os.system(current_dir + "semgrep/best_practices.py " + sys.argv[1])

# Run report script
os.system(current_dir + "make_pdf.py")

print("Completed! Please view the ScanResults pdf for detected potential OWASP Mobile App Security Verification Framework violations. For MSTG-CODE-5, review the OWASP Dependency Checker HTML report.")