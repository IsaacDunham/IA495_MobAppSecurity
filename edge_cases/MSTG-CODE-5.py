#!/usr/bin/python
# 1. detect vulnerabilities in third-party dependencies using OWASP Dependency Check
# 2. Detect undesired licenses used by the libraries of the application using OWASP dependency check


### Imports ###

import sys
import os
import datetime
from subprocess import Popen, PIPE

### static variables ###

output_json = "scan_results.json"
issue = False


### Functions ###


### Execution ###
def main():
    if len(sys.argv) < 2:
        print(
            "Usage: " + sys.argv[0] + " root directory of mobile application")
        sys.exit(1)

    path = os.path.dirname(sys.argv[1])

    global issue
    global debug_issue
    global signaturescheme_issue

    issuefiles = []
    results = {}
    files = []

    outpath = os.getcwd() + "/edge_cases/OWASP/"

    p = Popen(["curl", "-s", "https://jeremylong.github.io/DependencyCheck/current.txt"], stdout=PIPE,
            stderr=PIPE)
    version, err = p.communicate()

    rc = p.returncode
    if rc != 0:
        print("Error: " + str(err))
        print("retrieving OWASP dependency checker version failed")
        sys.exit(1)

    p = Popen(["curl", "-s", "https://jeremylong.github.io/DependencyCheck/current.txt"], stdout=PIPE,
            stderr=PIPE)
    version, err = p.communicate()

    rc = p.returncode
    if rc != 0:
        print("Error: " + str(err))
        print("retrieving OWASP dependency checker version failed")
        sys.exit(1)

    if os.path.exists(outpath + "dependency-check"): #figure out full path later:
        print("OWASP dependency checker already installed")
    else:
        os.mkdir (outpath)
        depcheckURL = "https://github.com/jeremylong/DependencyCheck/releases/download/v" + version + "/dependency-check-" + version + "-release.zip"
        p = Popen(["wget", depcheckURL, "-O", outpath + "depcheck.zip" ], stdout=PIPE,
            stderr=PIPE)
        result, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            print("Error: " + str(err))
            print("retrieving OWASP dependency checker failed")
            sys.exit(1)
        p = Popen(["unzip", outpath + "depcheck.zip", "-d", outpath], stdout=PIPE,
            stderr=PIPE)
        result, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            print("Error: " + str(err))
            print("unzipping OWASP dependency checker failed")
            sys.exit(1)

    now = datetime.datetime.now()
    outfilename = os.getcwd + "dependency-check-report" + str(now.strftime("%m%d%Y_%H%M")) + ".html"
    p = Popen([outpath + "dependency-check/bin/dependency-check.sh", 
               "--scan", path, "--out", outfilename, "--format", "HTML"], 
               stdout=PIPE, stderr=PIPE)
    result, err = p.communicate()
    rc = p.returncode
    if rc != 0:
        print("Error: " + str(err))
        print("OWASP dependency checker failed")
        sys.exit(1)
    
    print("To see dependency and license check results, open " + outfilename + " in a browser.")
    
main()