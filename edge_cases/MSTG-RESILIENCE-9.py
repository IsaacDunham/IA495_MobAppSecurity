#!/usr/bin/python3.8
# 1. run apkid to determine if the app has been obfuscated. 
# if the app does not have obfuscation, write a scan result


### Imports ###

import glob
import os
import sys
from subprocess import Popen, PIPE

sys.path.append(os.getcwd() + "/library/")
from util import write_scanresults

### static variables ###

output_json = "scan_results.json"
issue = False
apkid_path = os.getcwd() + "/edge_cases/APKiD/"
apkid_exec = apkid_path + "docker/apkid.sh"


### Functions ###


### Execution ###


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: " + sys.argv[0] + " root directory of mobile application")
        sys.exit(1)

    path = os.path.dirname(sys.argv[1])

    global issue

    issuefiles = []
    results = {}
    files = []

    #check to see if the Docker build has already been made. 
    #if not, build the Docker image
    p = Popen(["sudo", "docker", "images", "-q", "rednaga:apkid"], stdout=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    if rc != 0:
        print("Error: " + str(err))
        print("Docker check failed")
        sys.exit(1)
    if len(str(output)) == 0:
        print("Docker image not found. Building...")
        p = Popen(["git clone https://github.com/rednaga/APKiD"], stdout=PIPE)
        p = Popen(["sudo", "docker", "build", apkid_path, "-t", "rednaga:apkid"], stdout=PIPE)

    for f in glob.glob(path + "/**/*.apk", recursive=True):
        files += [f]

    if len(files) == 0:
        print("No APK files found")
        sys.exit(1)

    if isinstance(files, list):
        files = files
    else:
        files = [files]

    for filename in files:

        p = Popen(["sudo", apkid_exec, filename], stdout=PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            print("Error: " + str(err))
            print("apkid failed")
            sys.exit(1)
        if "obfuscator:" not in str(output):
            issue = True
            issuefiles += [filename]
            print("Obfuscator missing in ", filename)
    

    if issue:
        if len(issuefiles) == 1:
            issuefiles = (issuefiles[0])
        results["obfuscation_not_performed"] = {
            "files": {
                "file_path": issuefiles
            },
            "metadata": {
                "cwe": "CWE-312: Cleartext Storage of Sensitive Information",
                "description": "The application does not perform any form of obfuscation on the application code. This can make it easier for an attacker to reverse engineer the application and extract sensitive information. Please ensure that the application is obfuscated.",
                "masvs": "MSTG-RESILIENCE-9",
                "owasp-mobile": "M9: Reverse Engineering",
                "reference": ["https://github.com/OWASP/owasp-mastg/blob/master/Document/0x04c-Tampering-and-Reverse-Engineering.md",
                              "https://github.com/OWASP/owasp-masvs/blob/master/Document/10-MASVS-CODE.md",
                              "https://github.com/OWASP/owasp-mastg/blob/master/Document/0x05j-Testing-Resiliency-Against-Reverse-Engineering.md#dynamic-analysis"
                              ],
                "severity": "INFO"
            }
        }
        
        write_scanresults(results, output_json)
        sys.exit(0)
main()


