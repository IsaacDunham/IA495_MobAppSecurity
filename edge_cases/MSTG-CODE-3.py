#!/usr/bin/python
# 1. ensure that cppFlags "-fvisibility=hidden" is set in the build.gradle file


### Imports ###
from subprocess import Popen, PIPE
from pathlib import Path
import sys
import os
import yaml
import json
import glob

#import functions from util.py
sys.path.append(os.getcwd() + "/library/")
from util import write_scanresults

### static variables ###

output_json = "scan_results.json"
issue = False


### Functions ###


### Execution ###


def main():

    if len(sys.argv) < 2:
        print(
            "Usage: " + sys.argv[0] + "root directory of mobile application")
        sys.exit(1)

    path = os.path.dirname(sys.argv[1])

    issuefiles = []
    results = {}
    files = []

    for f in glob.glob(path + "/**/build.gradle", recursive=True):
        files += [f]

    if isinstance(files, list):
        files = files
    else:
        files = [files]

    for filename in files:
        friendlyname = os.path.basename(filename)
        with open(filename, "r") as f:
            content = f.read()
            if "cppFlags" in content:
                if "-fvisibility=hidden" in content:
                    issue = False
                else:
                    issue = True
                    issuefiles.append(filename)

    if issue:
        if len(issuefiles) == 1:
            issuefiles = (issuefiles[0])
        results["fvisibility_not_set_to_hidden"] = {
                "files": {
                    "file_path": issuefiles
                },
                "metadata": {
                    "cwe": "CWE-215: Information Leak Through Debug Information",
                    "description": "The application does not set the cppFlags to '-fvisibility=hidden'. Dynamic symbols can be used to reverse engineer the application. Please ensure they are stripped via the visibility compiler flag",
                    "masvs": "MSTG-CODE-1",
                    "owasp-mobile": "M3: Insecure Communication",
                    "reference": ["https://developer.android.com/studio/publish/preparing#publishing-configure",
                                  "https://github.com/OWASP/owasp-masvs/blob/master/Document/0x12-V7-Code_quality_and_build_setting_requirements.md",
                                  "https://github.com/OWASP/owasp-mastg/blob/master/Document/0x05i-Testing-Code-Quality-and-Build-Settings.md#testing-for-debugging-symbols-mstg-code-3"
                                  ],
                    "severity": "INFO"
                }
            }
        write_scanresults(results, output_json)
        sys.exit(0)