import os,requests,json,time,traceback
from datetime import datetime
from charparser import makelogs, makexml, archivedata

session = requests.Session()
session.headers.update({'User-Agent': 'POEClog'}) 
response = session.get('https://api.pathofexile.com') 

settings = {
    "toscan": [],
    "shortsleep": 1,    # min. seconds between API requests - avoid hitting the rate-limit
    "longsleep": 120,   # min. seconds between scans and after errors such as PoE being down etc.
    "maxlevel": 90,     # ignore characters at this level or higher
    "minlevel": 10      # ignore new characters above this level
}

accountdb = "data/accountdb.json"
accounts = {}

def mywait(mytime):
    print (f"Sleeping for {mytime}s")
    time.sleep(mytime)

while 1==1:

    if os.path.exists("settings.json"):
        with open("settings.json") as json_file:
            settings = json.load(json_file)
    else:
        with open("settings.json", 'w') as json_file:
            json.dump(settings, json_file, indent=4)

    chars = []
    if os.path.exists(accountdb):
        with open(accountdb) as json_file:
            accounts = json.load(json_file)

    for account in settings["toscan"]:
        try:
            print(f"Scanning Account {account}")
            if account not in accounts:
                accounts[account] = {}
            apichars = session.get(f"https://api.pathofexile.com/character-window/get-characters?accountName={account}&realm=pc")
            apichardb = apichars.json()
            for apichar in apichardb:
                if "level" in apichar and int(apichar["level"]) < int(settings["maxlevel"]):
                    if apichar["name"] in accounts[account]:
                        if accounts[account][apichar["name"]]["experience"] != apichar["experience"]:
                            if os.path.exists(f'data/{account}-{apichar["name"]}.json'):
                                if int(accounts[account][apichar["name"]]["level"]) > int(apichar["level"]):
                                    print (f'{apichar["name"]} has been rerolled - archiving old character data')
                                    archivedata(account,apichar["name"])
                                else:
                                    print (f'{apichar["name"]} ({apichar["level"]}) has been active')
                                chars.append({
                                    "account": account,
                                    "char": apichar["name"]
                                })
                            else:
                                print (f'{apichar["name"]} ({apichar["level"]}) has been active but no history - ignoring')
                    else:
                        if int(apichar["level"]) < int(settings["minlevel"]):
                            print (f'{apichar["name"]} ({apichar["level"]}) is new!')
                            chars.append({
                                "account": account,
                                "char": apichar["name"]
                            })
                        else:
                            print (f'{apichar["name"]} ({apichar["level"]}) is new but over Level {settings["minlevel"]} - ignoring')
                    accounts[account][apichar["name"]] = apichar
        except:
            track = traceback.format_exc()
            print(track)
            print('Waiting {settings["longsleep"]}s before continuing')
            mywait(settings["longsleep"])
        else:
            mywait(settings["shortsleep"])

    for char in chars:
        try:
            print(f'Scanning Char {char["account"]} - {char["char"]}')
            scantime = datetime.now()
            dbname = f'data/{char["account"]}-{char["char"]}.json'
            passives = session.get(f'https://api.pathofexile.com/character-window/get-passive-skills?reqData=0&accountName={char["account"]}&realm=pc&character={char["char"]}')
            passivedb = passives.json()
            payload = {'accountName':char["account"], 'character': char["char"]}
            items = session.get(url = 'https://api.pathofexile.com/character-window/get-items' , params = payload)
            itemdb = items.json()
            chardata = [{
                    "update": scantime,
                    "character": itemdb["character"],
                    "items": [],
                    "passives": []
            }]
            if os.path.exists(dbname):
                with open(dbname) as json_file:
                    chardata = json.load(json_file)
            chardata.append({
                    "update": scantime,
                    "character": itemdb["character"],
                    "items": itemdb["items"],
                    "passives": passivedb["hashes"]
            })

            if len(chardata) > 1:
                if makelogs(char['account'],char['char'],chardata[len(chardata)-2], chardata[len(chardata)-1]):                   
                    makexml(char['account'],char['char'],chardata,accounts[char["account"]][char["char"]])

            with open(dbname, 'w') as json_file:
                json.dump(chardata, json_file, indent=4, default=str)

        except:
            track = traceback.format_exc()
            print(track)
            print('Waiting {settings["longsleep"]}s before continuing')
            mywait(settings["longsleep"])

        mywait(settings["shortsleep"])

    with open(accountdb, 'w') as json_file:
        json.dump(accounts, json_file, indent=4)

    mywait(settings["longsleep"])