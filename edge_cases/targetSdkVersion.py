#!/usr/bin/python
#This script will check the targetSdkVersion of an APK file. To do this, it will
# create an apktool.yml file using /usr/bin/apktool. #It will then
# read the contents of the file in Python and extract the targetSdkVersion.

### Imports ###

from subprocess import Popen, PIPE
from pathlib import Path
import sys
import os
import yaml
import json
import glob


### Static Variables ###

#results is the dictionary that holds the results of security scan scripts 
# use fields as is appropriate for context
"""  resultsdictionary schema:

     Results:
        <issue_name_no_spaces>:
                files:
                        file_path: str or list
                        match_lines: int or list
                        match_position: int or list
                        match_string: string
                metadata:
                        cwe: str
                        description: str
                        masvs: str
                        owasp-mobile: str
                        reference: str or list
                        severity: str of either ERROR, WARNING, or INFO
                        """



#Output JSON file holds all scan results under results key
output_json = "scan_results.json"

### Functions ###
def write_scanresults(results, scanfile):
        #if file doesn't exist, create it
        if not os.path.exists(scanfile):
                with open(scanfile, "w+") as f:
                        json.dump({"results": results}, f, indent=4)
        else:
                with open(scanfile, "r+") as f:
                        outresults = json.load(f)
                        outresults["results"].update(results)
                        
                with open(scanfile, "w+") as f:
                        json.dump(outresults, f, indent=4)
                        


#YAML doesn't support unknown tags, so we must ignore it.
# solution via onlynone https://stackoverflow.com/users/436287/onlynone
def unknown(loader, suffix, node):
        if isinstance(node, yaml.ScalarNode):
                constructor = loader.__class__.construct_scalar
        elif isinstance(node, yaml.SequenceNode):
                constructor = loader.__class__.construct_sequence
        elif isinstance(node, yaml.MappingNode):
                constructor = loader.__class__.construct_mapping

        data = constructor(loader, node)
        return data

### Execution

def main():
        issuefiles = []
        results = {}
        if len(sys.argv) < 2:
                print("Usage: " + sys.argv[0] + " APK file or root directory of mobile application")
                sys.exit(1)

        
        path = os.path.dirname(sys.argv[1])
        files = []

        for f in glob.glob(path + "/**/*.apk", recursive=True):
                files += [f]
        
        if len(files) == 0:
                print("No APK files found")
                sys.exit(1)
        

        #apktool output location
        outpath = os.getcwd() + "/edge_cases/apktool/"
        if not os.path.exists(outpath):
                os.makedirs(outpath)

        #YAML won't parse unknown tags, so we run this
        yaml.add_multi_constructor('!', unknown, Loader=yaml.SafeLoader)
        yaml.add_multi_constructor('tag', unknown, Loader=yaml.SafeLoader)



        if isinstance(files, list):
                files = files
        else:
                files = [files]
        for filename in files:
                #Create apktool.yml file
                print("Creating apktool.yml file")
                p = Popen(["apktool", "d", "-o", outpath, "-f", filename], stdout=PIPE,
                        stderr=PIPE)
                output, err = p.communicate()
                rc = p.returncode

                if rc != 0:
                        print("Error: " + str(err))
                        print("apktool failed")
                        sys.exit(1)

        
                #Read apktool.yml file
                print("Reading apktool.yml file")
                with open(outpath + "apktool.yml", "r") as file:
                        data = yaml.safe_load(file)
                        targetSdkVersion = int(data["sdkInfo"]["targetSdkVersion"])

                print("targetSdkVersion for file " + filename + " is: " + str(targetSdkVersion))
                if targetSdkVersion < 24:
                        issue = True
                        issuefiles.append(filename)

        if issue:
                if len(issuefiles) == 1:
                        issuefiles = (issuefiles[0])
                        print("issuefiles is length 1")
                print("targetSdkVersion is less than 24")
                results["targetSdkVersion_less_than_24"] = {
                        "files":{
                                 "file_path": issuefiles
                                },
                        "metadata":{
                                "cwe": "CWE-295: Improper Certificate Validation",
                                "description": "The targetSdkVersion is less than 24. Android applications targeting Android 7.0 (API level 24) or higher will use a default Network Security Configuration that doesn't trust any user-supplied CAs. Please ensure the application does not trust user-supplied CAs.",
                                "masvs": "MSTG-NETWORK-3",
                                "owasp-mobile": "M3: Insecure Communication",
                                "reference": ["https://developer.android.com/training/articles/security-config", 
                                                "https://github.com/OWASP/owasp-masvs/blob/master/Document/0x10-V5-Network_communication_requirements.md", 
                                                "https://github.com/MobSF/owasp-mstg/blob/master/Document/0x05g-Testing-Network-Communication.md#testing-endpoint-identify-verification-mstg-network-3"
                                                ],
                                "severity": "INFO"
                                }
                        }
                write_scanresults(results, output_json)
                sys.exit(0)
main()