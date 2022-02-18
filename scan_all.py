import os,requests,json,traceback
from datetime import datetime
from charparser import makelogs, makexml, tolog, mywait
from bottle import template
import utils

poesite = 'https://www.pathofexile.com'
session = requests.Session()
session.headers.update({'User-Agent': 'POEClog'})
response = session.get(poesite)

accounts = {}

def archivedata(account,char):
    rrdate = datetime.today().strftime('%Y%m%d%H%M')
    if os.path.exists(f'data/{account}-{char}.json'):
        os.rename(f'data/{account}-{char}.json',f'data/{account}-{char}DEL{rrdate}.json')
    if os.path.exists(f'logs/{account}-{char}.log'):
        os.rename(f'logs/{account}-{char}.log',f'logs/{account}-{char}DEL{rrdate}.log')
    if os.path.exists(f'logs/{account}-{char}.html'):
        os.rename(f'logs/{account}-{char}.html',f'logs/{account}-{char}DEL{rrdate}.html')
    if os.path.exists(f'pob/builds/{account}-{char}.xml'):
        os.rename(f'pob/builds/{account}-{char}.xml',f'pob/builds/{account}-{char}DEL{rrdate}.xml')
    return f'{char}DEL{rrdate}'

first = True

while 1==1:

    utils.loadopt()

    if utils.getopt("stop"):
        break

    if first:
        first = False
    else:
        mywait(utils.getopt("longsleep"))

    try:
        if os.path.exists(utils.accountdb):
            with open(utils.accountdb) as json_file:
                accounts = json.load(json_file)
    except:
        tolog(f'Error: accountdb file invalid or corrupted')

        with open("mysite/index.html","w", encoding="utf-8") as webfile:
            webfile.write(template("mysite/index.tpl",{"accounts": accounts}))

    for account in utils.getopt("toscan"):

        toscan = []

        try:
            tolog(f"Scanning Account {account}")
            if account not in accounts:
                accounts[account] = {}
            apichars = session.get(f"{poesite}/character-window/get-characters?accountName={account}&realm=pc")
            if apichars.status_code != 200:
                tolog(f'Error: failed to read characters for account {account}')
            else:
                apichardb = apichars.json()
                for apichar in apichardb:
                    if apichar["name"] in accounts[account]:
                        if int(apichar["level"]) < int(utils.getopt("maxlevel")):
                            if "experience" in accounts[account][apichar["name"]] and accounts[account][apichar["name"]]["experience"] != apichar["experience"]:
                                if os.path.exists(f'data/{account}-{apichar["name"]}.json'):
                                    tolog (f'{apichar["name"]} ({apichar["level"]}) has been active')
                                    toscan.append({
                                        "account": account,
                                        "char": apichar["name"]
                                    })
                                else:
                                    tolog (f'{apichar["name"]} ({apichar["level"]}) has been active but no history - ignoring')
                    else:
                        dbname = f'data/{account}-{apichar["name"]}.json'
                        if os.path.exists(dbname):
                            tolog (f'{apichar["name"]} ({apichar["level"]}) recreating in accountdb!')
                            toscan.append({
                                "account": account,
                                "char": apichar["name"]
                            })
                        elif int(apichar["level"]) < int(utils.getopt("minlevel")):
                            tolog (f'{apichar["name"]} ({apichar["level"]}) is new!')
                            toscan.append({
                                "account": account,
                                "char": apichar["name"]
                            })
                        else:
                            tolog (f'{apichar["name"]} ({apichar["level"]}) is new but over Level {utils.getopt("minlevel")} - ignoring')
                    if apichar["name"] in accounts[account] and "clogextradata" in accounts[account][apichar["name"]] and os.path.exists(f'data/{account}-{apichar["name"]}.json'):
                        apichar["clogextradata"] = accounts[account][apichar["name"]]["clogextradata"]
                    accounts[account][apichar["name"]] = apichar
            
            for char in toscan:
            
                try:
                    tolog(f'Scanning Char {char["account"]} - {char["char"]}')
                    scantime = datetime.now()
                    dbname = f'data/{char["account"]}-{char["char"]}.json'
                    passives = session.get(f'{poesite}/character-window/get-passive-skills?reqData=0&accountName={char["account"]}&realm=pc&character={char["char"]}')
                    passivedb = passives.json()
                    payload = {'accountName':char["account"], 'character': char["char"]}
                    items = session.get(url = f'{poesite}/character-window/get-items' , params = payload)
                    itemdb = items.json()
                    chardata = [{
                            "update": scantime,
                            "character": itemdb["character"],
                            "items": [],
                            "passives": [],
                            "POBTREEVER": utils.getopt("POBTREEVER")
                    }]
                    if os.path.exists(dbname):
                        with open(dbname) as json_file:
                            chardata = json.load(json_file)
                    chardata.append({
                            "update": scantime,
                            "character": itemdb["character"],
                            "items": itemdb["items"],
                            "passives": passivedb["hashes"],
                            "POBTREEVER": utils.getopt("POBTREEVER")
                    })

                    if len(chardata) > 1:
                        tolog(makelogs(char['account'],char['char'],chardata[len(chardata)-2], chardata[len(chardata)-1]))

                        accounts[char["account"]][char["char"]]["clogextradata"] = makexml(char['account'],char['char'],chardata)

                    with open(dbname, 'w') as json_file:
                        json.dump(chardata, json_file, indent=4, default=str)

                except:
                    tolog("Error during Character Scan")
                    track = traceback.format_exc()
                    tolog(track)
                    mywait(utils.getopt("longsleep"))

        except:
            tolog("Error during Account Scan")
            track = traceback.format_exc()
            tolog(track)
            mywait(utils.getopt("longsleep"))
           
        with open(utils.accountdb, 'w') as json_file:
            json.dump(accounts, json_file, indent=4)

        mywait(utils.getopt("shortsleep"))