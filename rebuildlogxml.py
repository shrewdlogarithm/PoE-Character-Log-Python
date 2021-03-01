import glob,json,os
from charparser import makelogs,makexml

accountdb = "accountdb.json"
accounts = {}

if os.path.exists(accountdb):
    with open(accountdb) as json_file:
        accounts = json.load(json_file)

POEChars = glob.glob('data/*.json')

for POEChar in POEChars:

    account,char = os.path.basename(POEChar).replace(".json","").split("-")

    logs = glob.glob(f'logs/{account}-{char}.*')
    for log in logs:
        os.remove(log)

    with open(POEChar, encoding='utf-8') as json_file:
        chardata = json.load(json_file)
        print(f'{account} - {char}')
        updated = False
        for i in range(1,len(chardata)):
            if makelogs(account,char, chardata[i-1], chardata[i]):
                updated=True
        if updated:
            print("Updated")
        if char in accounts[account]:
            root = makexml(account,char,chardata,accounts[account][char])
        else:
            root = makexml(account,char,chardata,{})

with open(accountdb, 'w') as json_file:
    json.dump(accounts, json_file, indent=4)

