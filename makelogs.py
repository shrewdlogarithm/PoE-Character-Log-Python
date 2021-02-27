import json,glob,os
from charparser import makelogs

POEChars = glob.glob('data/*-*.json')

for POEChar in POEChars:

    account,char = os.path.basename(POEChar).replace(".json","").split("-")

    logs = glob.glob(f'logs/{account}-{char}.*')
    for log in logs:
        os.remove(log)

    with open(POEChar, encoding='utf-8') as json_file:
        chardata = json.load(json_file)
        changes = []
        updated = False
        for i in range(1,len(chardata)):
            if makelogs(account,char, chardata[i-1], chardata[i]):
                updated=True
        print(POEChar)
        if updated:
            print("Updated")