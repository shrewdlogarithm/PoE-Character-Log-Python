import json,glob,os
from charparser import checkchanges,writelogs

POEChars = glob.glob('data/*-*.json')

for POEChar in POEChars:

    account,char = os.path.basename(POEChar).replace(".json","").split("-")

    logs = glob.glob(f'logs/{account}-{char}.*')
    for log in logs:
        os.remove(log)

    with open(POEChar, encoding='utf-8') as json_file:
        print(POEChar)
        chardata = json.load(json_file)
        changes = []
        for i in range(1,len(chardata)):
            chgs = checkchanges(chardata[i-1], chardata[i])
            writelogs(account,char,chgs)