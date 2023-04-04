#!/usr/bin/python3.8
# This code is strongly inspired by the code from the MobSF project. The original code can be found here:
# https://github.com/MobSF/mobsfscan/blob/main/mobsfscan/utils.py

#at present, this code needs to be re-optimized. 

import sys
import os
from libsast import Scanner

# import functions from util.py
sys.path.append(os.getcwd() + "/library/")
from util import write_scanresults, get_file_extensions, get_best_practices

### static variables ###
best_practices_dir = os.getcwd() + "/semgrep/best_practices/"
output_json = "scan_results.json"
 
def main():
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + "root directory of mobile application")
        sys.exit(1)

    path = os.path.dirname(sys.argv[1])
    path_list = [(sys.argv[1])]  # require for libsast scanner

    extensions = get_file_extensions(path)
    supported_extensions = set([".java", ".kotlin"])
    extensions = extensions.intersection(
        supported_extensions)  # intersections is for set())

    # Perform semgrep scan
    results = {
        "results": {},
        'errors': {}
    }
    write_results = {
        "results": {},
        "errors": {}
    }
    for extension in extensions:
        if extension == ".java":
            libsast_option = {'sgrep_rules': best_practices_dir + "java/best_practices.yaml",
                              'sgrep_extensions': {'.java'}}
        elif extension == ".kotlin":
            libsast_option = {'sgrep_rules': best_practices_dir + "kotlin/best_practices.yaml",
                              'sgrep_extensions': {'.kotlin'}}
        else:
            print("No best practices rules for this extension")
            sys.exit(1)
        scanner = Scanner(libsast_option, path_list)
        output = scanner.scan()
        #nothing at top level
        output = output['semantic_grep']

        results['results'].update(output['matches'])
        results['errors'].update(output['errors'])


    ids, all_rules = get_best_practices(extensions)
    #need to investigate this further to determine necessity

    #result keys are the rule ids
    result_keys = results['results'].keys() 
    deleted = set()
    for rule_id in ids:
        if rule_id in result_keys:
            # Control Present
            deleted.add(rule_id)
            del results['results'][rule_id]
    # Add Missing
    missing = ids.difference(result_keys)
    for rule_id in missing:
        if rule_id in deleted:
            continue

        results['results'][rule_id] = {}
        res = results['results'][rule_id]
        details = all_rules[rule_id]
        res['metadata'] = details['metadata']
        res['metadata']['description'] = details['message']
        res['metadata']['severity'] = details['severity']

        #need to append and then write_scanresults at end, because some function
        #does not like writing to a file multiple times in one execution. 
        write_results['results'].update({rule_id: res})
    write_scanresults(write_results['results'], output_json)
main()
