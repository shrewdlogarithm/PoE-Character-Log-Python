import json,glob,os
from charparser import makexml

POEChars = glob.glob('data/*-*.json')

for POEChar in POEChars:

    account,char = os.path.basename(POEChar).replace(".json","").split("-")

    with open(POEChar, encoding='utf-8') as json_file:
        print(POEChar)
        chardata = json.load(json_file)
        root = makexml(account,char,chardata)
