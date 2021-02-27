import glob,json,os
from charparser import makexml

accountdb = "data/accountdb.json"
accounts = {}

if os.path.exists(accountdb):
    with open(accountdb) as json_file:
        accounts = json.load(json_file)
        POEChars = glob.glob('data/*-*.json')
        for POEChar in POEChars:
            account,char = os.path.basename(POEChar).replace(".json","").split("-")
            if os.path.exists(POEChar):
                with open(POEChar, encoding='utf-8') as json_file:
                    chardata = json.load(json_file)
                    print(f'{account} - {char}')
                    if char in accounts[account]:
                        root = makexml(account,char,chardata,accounts[account][char])
                    else:
                        print("JSON without entry in accountdb " + account + " " + char)
with open(accountdb, 'w') as json_file:
    json.dump(accounts, json_file, indent=4)

