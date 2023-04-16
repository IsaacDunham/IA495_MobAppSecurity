#!/usr/bin/python3.8
# 1.	Make sure that the release build has been signed via both the v1 and v2
#   schemes for Android 7.0 (API level 24) and above and via all three schemes
#   for Android 9 (API level 28) and above. Use apksigner.
# 2. Ensure that code-signing certificate belongs to the developer. --
#   Make sure it is not CN=Android Debug. Use jarsigner.


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
debug_issue = False
signaturescheme_issue = False


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
        friendlyname = os.path.basename(filename)

        # check targetSdkVersion level
        if os.path.exists(os.getcwd() + "/edge_cases/apktool/" + friendlyname +
                          "_targetSdkVersion.txt"):
            with open(os.getcwd() + "/edge_cases/apktool/" + friendlyname +
                      "_targetSdkVersion.txt", "r") as f:
                targetSdkVersion = int(f.read())
        else:
            print("targetSdkVersion not found for " +
                  filename + ". Noting as 0.")
            targetSdkVersion = 0

        if targetSdkVersion < 24:
            print(
                "API level is below 24. Skipping v1 and v2 scheme check for " + filename)

        elif targetSdkVersion >= 24:
            p = Popen(["apksigner", "verify",
                      "--verbose", filename], stdout=PIPE)
            output, err = p.communicate()
            rc = p.returncode
            if rc != 0:
                print("Error: " + str(err))
                print("apksigner failed")
                sys.exit(1)

            p = Popen(["grep", '"verified using"'], stdout=PIPE, stdin=PIPE)
            output, err = p.communicate()
            if "Verified using v1 scheme (JAR signing): true" not in str(output):
                print("v1 scheme not used")
                issue = True
                issuefiles.append(filename)
            if "Verified using v2 scheme (APK Signature Scheme v2): true" not in str(output):
                print("v2 scheme not used")
                issue = True
                issuefiles.append(filename)

            if targetSdkVersion >= 28:
                if "Verified using v3 scheme (APK Signature Scheme v3): true" not in str(output):
                    print("v3 scheme not used")
                    issue = True
                    issuefiles.append(filename)
            if issue:
                signaturescheme_issue = True

        # use jarsigner to check if the code-signing certificate belongs to the developer
        p = Popen(["jarsigner", "--verify", "-verbose",
                  "-certs", filename], stdout=PIPE)
        output, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            print("Error: " + str(err))
            print("jarsigner failed")
            sys.exit(1)
        p = Popen(["grep", '"CN="'], stdout=PIPE, stdin=PIPE)
        output, err = p.communicate()
        if "CN=Android Debug" in str(output):
            print("CN=Android Debug found")
            debug_issue = True
            issue = True
            issuefiles.append(filename)

    if issue:
        if len(issuefiles) == 1:
            issuefiles = (issuefiles[0])
        if signaturescheme_issue:
            results["release_build_not_signed_with_appropriate_schemes"] = {
                "files": {
                    "file_path": issuefiles
                },
                "metadata": {
                    "cwe": "CWE-295: Improper Certificate Validation",
                    "description": "The release build has not been signed via both the v1 and v2 schemes for Android 7.0 (API level 24) and above and via all three schemes for Android 9 (API level 28) and above. Please ensure the application is signed via all three schemes for Android 9 (API level 28) and above and via both the v1 and v2 schemes for Android 7.0 (API level 24) and above.",
                    "masvs": "MSTG-CODE-1",
                    "owasp-mobile": "M3: Insecure Communication",
                    "reference": ["https://github.com/OWASP/owasp-masvs/blob/master/Document/10-MASVS-CODE.md",
                                  "https://github.com/OWASP/owasp-mastg/blob/master/Document/0x05i-Testing-Code-Quality-and-Build-Settings.md"
                                  ],
                    "severity": "WARNING"
                }
            }

        if debug_issue:
            results["cert_not_signed_with_developer_signature"] = {
                "files": {
                    "file_path": issuefiles
                },
                "metadata": {
                    "cwe": "CWE-295: Improper Certificate Validation",
                    "description": "The code-signing certificate should belong to the developer. It was detected as using CN=Android Debug. Please ensure the application is signed with the appropriate developer certificate.",
                    "masvs": "MSTG-CODE-1",
                    "owasp-mobile": "M3: Insecure Communication",
                    "reference": ["https://developer.android.com/studio/publish/preparing#publishing-configure",
                                  "https://github.com/OWASP/owasp-masvs/blob/master/Document/0x12-V7-Code_quality_and_build_setting_requirements.md",
                                  "https://github.com/OWASP/owasp-mastg/blob/master/Document/0x05i-Testing-Code-Quality-and-Build-Settings.md#making-sure-that-the-app-is-properly-signed-mstg-code-1"
                                  ],
                    "severity": "WARNING"
                }
            }

        write_scanresults(results, output_json)
        sys.exit(0)


main()
