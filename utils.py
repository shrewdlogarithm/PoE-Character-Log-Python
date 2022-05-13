import json

base_path = ""
accountdb = "accountdb.json"
      
# OPTIONS
options = {}
defaultoptions = {
    "toscan": [],
    "shortsleep": 1,    # min. seconds between API requests - avoid hitting the rate-limit
    "longsleep": 120,   # min. seconds between scans and after errors such as PoE being down etc.
    "maxlevel": 90,     # ignore characters at this level or higher
    "minlevel": 10,      # ignore new characters above this level
    "POBTREEVER": "3_18" # league tag for PoB and passive-tree
}

def getopt(opt):
    global options
    if opt in options:
        return options[opt]
    else:
        return 0

def setopt(opt,val):
    global options
    options[opt] = val
    saveopt()

def saveopt():
    global options
    with open('settings.json', 'w') as outfile:
        json.dump(options, outfile, sort_keys=True, indent=4)

def loadopt():
    global options,defaultoptions
    try:
        with open('settings.json') as json_file:
            options = json.load(json_file)
    except:
        options = {}
    options = {**defaultoptions, **options}
    saveopt()

loadopt()