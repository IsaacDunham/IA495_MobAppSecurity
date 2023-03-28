# This is a library file containing functions common to multiple tests. It is not a test in itself.

import os
import json
import yaml
import glob
from pathlib import Path

def write_scanresults(results, scanfile):
    # if file doesn't exist, create it
    if not os.path.exists(scanfile):
        with open(scanfile, "w+") as f:
            json.dump({"results": results}, f, indent=4)
    else:
        with open(scanfile, "r+") as f:
            outresults = json.load(f)
            outresults["results"].update(results)

        with open(scanfile, "w+") as f:
            json.dump(outresults, f, indent=4)


def get_best_practices(extensions):
    best_practices_dir = os.getcwd() + "/semgrep/best_practices/"

    all_rules = {}
    ids = set()
    supported_extensions = set([".java", ".kotlin"])
    for extension in extensions:
    # Better to functionalize this if additional languages are added
        if extension in supported_extensions:
            print("Checking for missing best practices in " + extension + " files")
            if extension == ".java":
                for yml in glob.glob(best_practices_dir + "java/*.yaml"):
                    #make yml a file object
                    yml = Path(yml)
                    try:
                        rules = yaml.safe_load(yml.read_text('utf-8', 'ignore'))
                    except yaml.YAMLError:
                        print("Error parsing YAML file: " + yml)
                    for rule in rules['rules']:
                        all_rules[rule['id']] = rule
                        ids.add(rule['id'])
            elif extension == ".kotlin":
                for yml in glob.glob(best_practices_dir + "/kotlin/*.yaml"):
                    #make yml a file object
                    yml = Path(yml)
                    try:
                        rules = yaml.safe_load[yml]
                    except yaml.YAMLError:
                        print("Error parsing YAML file: " + yml)
                    for rule in rules['rules']:
                        all_rules[rule['id']] = rule
                        ids.add(rule['id'])
    return ids, all_rules


def get_file_extensions(path):
    extensions = set()
    files = glob.glob(path + '/**/*', recursive=True)
    for file in files:
        if os.path.isfile(file):
            ext = os.path.splitext(file)[1]
            extensions.add(ext)
    return extensions
