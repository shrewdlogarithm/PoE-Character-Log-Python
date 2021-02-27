import json,glob,os
from charparser import makexml

accountdb = "data/accountdb.json"
accounts = {}

if os.path.exists(accountdb):
    with open(accountdb) as json_file:
        accounts = json.load(json_file)
        for account in accounts:
            for char in accounts[account]:    
                datafile = f'data/{account}-{char}.json'
                if os.path.exists(datafile):
                    with open(f'data/{account}-{char}.json', encoding='utf-8') as json_file:
                        chardata = json.load(json_file)
                        print(f'{account} - {char}')
                        root = makexml(account,char,chardata,accounts[account][char])
with open(accountdb, 'w') as json_file:
    json.dump(accounts, json_file, indent=4)

