import glob,json,os,traceback
from charparser import makelogs,makexml
import utils

def run():
    accounts = {}
    logs = glob.glob(f'logs/*-*.*')
    for log in logs:
        os.remove(log)
    xmls = glob.glob(f'pob/builds/*-*.*')
    for xml in xmls:
        os.remove(xml)

    POEChars = glob.glob('data/*.json')

    for POEChar in POEChars:

        account,char = os.path.basename(POEChar).replace(".json","").split("-")

        print(account,"-",char)

        with open(POEChar, encoding='utf-8') as json_file:
            try:
                chardata = json.load(json_file)
                for i in range(1,len(chardata)):
                    makelogs(account,char, chardata[i-1], chardata[i])
                if account not in accounts:
                    accounts[account] = {}
                if char not in accounts[account]:
                    accounts[account][char] = chardata[len(chardata)-1]["character"]
                accounts[account][char]["clogextradata"] = makexml(account,char,chardata)
            except Exception as e:
                print("Error parsing character")
                track = traceback.format_exc()
                print(track)

    with open(utils.accountdb, 'w') as json_file:
        json.dump(accounts, json_file, indent=4)

if __name__ == "__main__":
    run()
