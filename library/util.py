#This is a library file containing functions common to multiple tests. It is not a test in itself.


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
            