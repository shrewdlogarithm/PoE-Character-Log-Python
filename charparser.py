import base64,zlib,json,re,os,time,traceback
from xml.dom import minidom
import utils

def fixspec(strin):
    strin = strin.replace(chr(246),"o") # diaresis 'o' as in Maelstrom
    strin = strin.replace(chr(228),"a") # umlaut 'a' as in Doppelganger
    strin = strin.replace(chr(237),"i") # accent i from Spanis#
    specchar = re.search(r"...[\x80-\xff]...",strin)
    if specchar:
        tolog("Special Character encountered " + specchar.group() + " - Charcode " + str(ord(specchar.group()[3:4])),False)
        strin = re.sub(r"[\x80-\xff]","?",strin)            
    return strin

def tolog(out,fix = True):
    if out:
        if fix:
            out = fixspec(out)
        out = out.rstrip()
        try:
            print(out)
            with open("scan_all.log", 'a', encoding="utf-8") as logout:
                logout.write(out + "\n")
        except Exception as e:
            tolog("Unexpected error during Log Writing")
            track = traceback.format_exc()
            tolog(track)

def mywait(mytime):
    time.sleep(mytime)

with open(utils.base_path + 'passive-skill-tree' + utils.getopt("POBTREEVER") + '.json') as json_file:
    passivedb = json.load(json_file)

def getpassives(passives):
    ret = []
    for passive in passives:
        if str(passive) in passivedb["nodes"] and "name" in passivedb["nodes"][str(passive)]:
            if "isNotable" in passivedb["nodes"][str(passive)]:
                ret.append("<a class=notable href=\"https://pathofexile.gamepedia.com/" + passivedb["nodes"][str(passive)]["name"].replace(" ","_") + "\">" + passivedb["nodes"][str(passive)]["name"] + '</a>')
            else:
                ret.append("<span class=notable>" + passivedb["nodes"][str(passive)]["name"] + f' [{str(passive)}]</span>')
        else:
            ret.append(f"Unknown passive {passive}")
    return ret

def getitems(items):
    ret = []
    for item in items:
        sockets = ""
        slot = item["inventoryId"]
        if slot  and slot != "MainInventory":
            name = ""
            if "sockets" in item:
                for socket in item["sockets"]:
                    sockets += "<span class=\"socket" + socket["sColour"] + "\">" + socket["sColour"] + "</span>"
            name += "<span class=\"itemquality" + str(item["frameType"]) + "\">"
            if "name" in item and len(item["name"]) > 0:
                if item["frameType"] == 3:
                    name += f'<a href="https://pathofexile.gamepedia.com/{item["name"]}">{item["name"]}</a> {item["typeLine"]}'
                else:
                    name += f'{item["name"]} {item["typeLine"]}'
            else:
                name += item["typeLine"]
            name += " iLvl:" + str(item["ilvl"])
            name += "</span>"
            name += " " + sockets
            ret.append(name)
    return ret

def buildskills(items):
    gemgroups = {}
    for item in items:
        slot = item["inventoryId"]
        if slot and slot != "MainInventory" and slot != "Flask" and slot != "Weapon2" and slot != "Offhand2":
            gemobjs = []
            for g in range(0, 6):
                gemobjs.append({
                    "gems": [],
                    "supports": []
                })
            gemgroups[slot] = gemobjs
            if "socketedItems" in item:
                for gem in range(0,len(item["socketedItems"])):
                    gqual = "0"
                    glvl = "1"
                    for prop in item["socketedItems"][gem]["properties"]:
                        if prop["name"] == "Quality":
                            gqual = re.findall(r'-?\d+\.?\d*', prop["values"][0][0])[0]
                        elif prop["name"] == "Level":
                            glvl = re.findall(r'-?\d+\.?\d*', prop["values"][0][0])[0]
                    group = item["sockets"][gem]["group"]
                    if item["socketedItems"][gem]["colour"] and item["socketedItems"][gem]["typeLine"]:
                        gemstr = {
                            "color": item["socketedItems"][gem]["colour"],
                            "name": item["socketedItems"][gem]["typeLine"],
                            "quality": gqual,
                            "level": glvl
                        }
                        if " Support" in item["socketedItems"][gem]["typeLine"] or ("support" in item["socketedItems"][gem] and item["socketedItems"][gem]["support"]):
                            gemgroups[slot][group]["supports"].append(gemstr)
                        else:
                            gemgroups[slot][group]["gems"].append(gemstr)
    return gemgroups

def getskills(items):
    ret = []
    gemgroups = buildskills(items)
    for slot in gemgroups:
        for group in gemgroups[slot]:
            if len(group["gems"]) > 0 or len(group["supports"]) > 0:
                gms = []
                for gm in group["gems"]:
                    if "color" in gm:
                        gms.append("<a class=gem" + gm["color"] + " href=\"https://pathofexile.gamepedia.com/" + gm["name"].replace(" ","_") + "\">" + gm["name"] + "</a>")
                    else:
                        gms.append(gm["name"])
                sps = []
                for gm in group["supports"]:
                    if "color" in gm:
                        sps.append("<a class=gem" + gm["color"] + " href=\"https://pathofexile.gamepedia.com/" + gm["name"].replace(" ","_") + "\">" + gm["name"] + "</a>")
                    else:
                        sps.append(gm["name"])
                ret.append(" | ".join(gms) + " >> " + " | ".join(sps))
    return ret

def showchanges(before, after, bpref, apref):
    ret = []
    for bef in before:
        if bef not in after:
           ret.append(f"{bpref}{bef}\n")
    for aft in after:
        if aft not in before:
           ret.append(f"{apref}{aft}\n")
    return ret

def maketreelink(char):
    header = [0,0,0,4,int(char["character"]["classId"]),int(char["character"]["ascendancyClass"]),0]
    bhead = bytearray(header)
    for node in char["passives"]:
        bhead.append(node//256)
        bhead.append(node%256)
    return "https://www.pathofexile.com/fullscreen-passive-skill-tree/" + base64.b64encode(bhead,altchars=b"-_").decode("utf-8")

def makelogs(account,char,before,after):
    out = ""
    if (before["character"]["level"] != after["character"]["level"]):
        out = out + f'Reached Level {after["character"]["level"]}\n'
    for change in showchanges(getpassives(before["passives"]),getpassives(after["passives"]),"Deallocated ","Allocated "):
        out = out + change
    for change in showchanges(getitems(before["items"]),getitems(after["items"]),"Removed ","Equipped "):
        out = out + change
    for change in showchanges(getskills(before["items"]),getskills(after["items"]),"Unsocketed ","Socketed "):
        out = out + change
    if (before["character"]["level"] != after["character"]["level"]):
        lasttreelink = maketreelink(before)
        treelink = maketreelink(after)
        if lasttreelink != treelink:
            out = out + "Passive Tree <a href=\"" + treelink  + "\">" + treelink + '</a>\n'
    if len(out) > 0:
        if not os.path.exists(f"logs/{account}-{char}.html"):
            with open(f"logs/{account}-{char}.html", 'w', encoding='utf8') as f:
                f.write("<head><link rel=\"stylesheet\" href=\"/css/style.css\"><link rel=\"stylesheet\" href=\"/css/poe.css\"></head>")
                f.write(f"Account: {account} - Character: {char}<BR><BR>")
        if not os.path.exists(f"logs/{account}-{char}.log"):
            with open(f"logs/{account}-{char}.log", 'w', encoding='utf8') as f:
                f.write(f"Account: {account} - Character: {char}\n")
        with open(f"logs/{account}-{char}.html", 'a') as f:
            f.write(out.replace("\n","<BR><BR>"))
        with open(f"logs/{account}-{char}.log", 'a') as f:
            out = re.sub('<[^>]+>', '', out)
            f.write(out)
    return out
    
className = ("Scion","Marauder","Ranger","Witch","Duelist","Templar","Shadow")
ascendName = (
    ("None","Ascendant"),
    ("None","Juggernaut","Berserker","Chieftain"),
    ("None","Raider","Deadeye","Pathfinder"),
    ("None","Occultist","Elementalist","Necromancer"),
    ("None","Slayer","Gladiator","Champion"),
    ("None","Inquisitor","Hierophant","Guardian"),
    ("None","Assassin","Trickster","Saboteur")
)
rarity = ("NORMAL","MAGIC","RARE","UNIQUE")
socketTrans = {
    "Weapon": "Weapon 1",
    "Offhand": "Weapon 2",
    "Weapon2": "Weapon 1 Swap",
    "Offhand2": "Weapon 2 Swap",
    "Amulet": "Amulet",
    "Gloves": "Gloves",
    "Boots": "Boots",
    "Ring": "Ring 1",
    "Ring2": "Ring 2",
    "Belt": "Belt",
    "BodyArmour": "Body Armour",
    "Helm": "Helmet",
    "Flask": "Flask"
}

def getbyname(attrs,attr,name):
    if attr in attrs:
        for at in attrs[attr]:
            if "name" in at and at["name"] == name:
                return at["values"][0][0]

def getname(gem):
    gem = gem["name"]
    gem = gem.replace(" Support","")
    gem = gem.replace("Anomalous ","")
    gem = gem.replace("Divergent ","")
    gem = gem.replace("Phantasmal ","")
    return gem

def abbrev(gem):
    abb = gem.split()
    if len(abb) > 2:
        return abb[0][:1] + abb[1][:1] + abb[2][:1]
    elif len(abb) > 1:
        return abb[0][:2] + abb[1][:2]
    else:
        return abb[0][:4]

def makexml(account,char,chardata):
    root = minidom.Document()
    pob = root.createElement('PathOfBuilding')
    root.appendChild(pob)
    build = root.createElement('Build')
    build.setAttribute("targetVersion","3_0")
    build.setAttribute('level',str(chardata[len(chardata)-1]["character"]["level"]))
    build.setAttribute('className',className[chardata[len(chardata)-1]["character"]["classId"]])
    build.setAttribute('ascendClassName',ascendName[chardata[len(chardata)-1]["character"]["classId"]][chardata[len(chardata)-1]["character"]["ascendancyClass"]])
    build.setAttribute("viewMode","ITEMS")
    # add a dummy playerstat node because PoB's XML parser doesn't read "empty" Build nodes correctly
    dummyplayerstat = root.createElement("PlayerStat")
    build.appendChild(dummyplayerstat)
    pob.appendChild(build)
    tree = root.createElement('Tree')
    tree.setAttribute('activeSpec', '1')
    pob.appendChild(tree)
    items = root.createElement("Items")
    items.setAttribute("activeItemSet","1")
    items.setAttribute("useSecondWeaponSet","nil")
    pob.appendChild(items)
    skills = root.createElement("Skills")
    pob.appendChild(skills)
    skilldb = {}
    itemdb = {}
    lastset = {}
    itn = 1
    isn = 1
    lltree = 0
    for e in range(0,len(chardata)):
        level = chardata[e]["character"]["level"]
        lastnodes = ",".join(str(node) for node in chardata[e-1]["passives"])
        nodes = ",".join(str(node) for node in chardata[e]["passives"])
        #if nodes != lastnodes:
        if chardata[e]["character"]["level"] - lltree >= 5 or len(chardata)-e <= 1:
            id = root.createElement("Spec")
            lltree = chardata[e]["character"]["level"]
            id.setAttribute("title",f'{e} - Level {chardata[e]["character"]["level"]}')
            id.setAttribute("ascendClassId",str(chardata[e]["character"]["ascendancyClass"]))
            id.setAttribute("nodes",nodes)
            id.setAttribute("treeVersion",utils.getopt("POBTREEVER"))
            id.setAttribute("classId",str(chardata[e]["character"]["classId"]))
            tree.appendChild(id)
        gemgroups = buildskills(chardata[e]["items"])
        mainskills = []
        for slot in gemgroups:            
            skill = root.createElement("Skill")
            skillset = ""
            for group in gemgroups[slot]:
                if (len(group["supports"]) > 0):
                    for gm in group["gems"]:
                        mainskills.append("[" + str(len(group["supports"])) + "] " + getname(gm))
                if len(group["gems"]) > 0:
                    for mg in sorted(group["gems"], key=lambda k: k['name']): # sorted([x["name"] for x in group["gems"]])
                        skillset += "," + getname(mg)
                    for sg in sorted(group["supports"], key=lambda k: k["name"]): # sorted([x["name"] for x in group["supports"]])
                        skillset += "+" + abbrev(getname(sg))
                    for gm in group["gems"]+group["supports"]:
                        gem = root.createElement("Gem")
                        gem.setAttribute("level",gm["level"])
                        gem.setAttribute("nameSpec",getname(gm))
                        gem.setAttribute("quality",gm["quality"])
                        gem.setAttribute("enabled","true")
                        skill.appendChild(gem)
            if skillset != "" and (slot not in skilldb or skillset not in skilldb[slot]):
                skill.setAttribute("label",f"{level}{skillset}")
                skill.setAttribute("slot",socketTrans[slot])
                skill.setAttribute("enabled","true")
                skills.appendChild(skill)
                skilldb[slot] = skillset
        itemset = root.createElement("ItemSet")
        itemset.setAttribute("id",str(isn))
        itemset.setAttribute("useSecondWeaponSet","nil")
        itemset.setAttribute("title",f'{isn} - Level {chardata[e]["character"]["level"]}')
        fln = 1
        for itm in chardata[e]["items"]:
            if itm["inventoryId"] in socketTrans and itm['frameType'] < 4:
                itemkey = f"{itm['name']}{itm['typeLine']}"
                itemno = str(itn)
                if itemkey in itemdb:
                    itemno = itemdb[itemkey]
                else:
                    itemdb[itemkey] = str(itn)
                    item = root.createElement("Item")
                    item.setAttribute("id",itemno)
                    itemtext = f"\nRarity: {rarity[itm['frameType']]}\n{itm['name']}\n{itm['typeLine']}\n"
                    if "id" in itm:
                        itemtext += f'Unique ID:{itm["id"]}\n'
                    if "ilvl" in itm:
                        itemtext +=  f'Item Level: {itm["ilvl"]}\n'
                    lvlreq = getbyname(itm,"requirements","Level")
                    if "sockets" in itm:
                        itemtext += "Sockets: "
                        for gem in range(0,len(itm["sockets"])):
                            if gem > 0 and itm["sockets"][gem-1]["group"] != itm["sockets"][gem]["group"]:
                                itemtext += " "
                            elif gem > 0:
                                itemtext += "-"
                            itemtext += itm["sockets"][gem]["sColour"]
                        itemtext += "\n"
                    if lvlreq:
                        itemtext +=  f'LevelReq: {lvlreq}\n'
                    if "implicitMods" in itm:
                        itemtext +=  f'Implicits: {len(itm["implicitMods"])}\n'
                        for imp in itm["implicitMods"]:
                            itemtext += imp + "\n"
                    if "explicitMods" in itm:
                        for exp  in itm["explicitMods"]:
                            itemtext += exp + "\n"
                    itemtext = fixspec(itemtext)                    
                    text = root.createTextNode(itemtext)
                    item.appendChild(text)
                    items.appendChild(item)
                    itn = itn + 1
                iid = socketTrans[itm["inventoryId"]]
                if iid == "Flask":
                    iid += f" {fln}"
                    fln = fln + 1
                islot = root.createElement("Slot")
                islot.setAttribute("name",iid)
                islot.setAttribute("itemId",itemno)
                itemset.appendChild(islot)
                if itemset.parentNode is None and (iid not in lastset or lastset[iid] != itemno):
                    items.appendChild(itemset)
                    isn = isn + 1
                lastset[iid] = itemno
    
    mainskills = re.sub("\[[0-9]*\] ","","  ".join(sorted(set(mainskills),reverse=True)))
    if len(mainskills) > 75:
        mainskills = mainskills[0:75] + "..."

    try:
        pcode = base64.b64encode(zlib.compress(root.toxml().encode('ascii')),altchars=b"-_").decode("ascii")
    except Exception as e:
        tolog("Unexpected error during XML to pastecode conversion")
        track = traceback.format_exc()
        tolog(track)


    with open(f"pob/builds/{account}-{char}.xml", 'w') as f:
        f.write(root.toprettyxml(indent ="\t"))

    pobtreever = utils.getopt("POBTREEVER")
    if "POBTREEVER" in chardata[len(chardata)-1]:
        pobtreever = chardata[len(chardata)-1]["POBTREEVER"]
    return {
        "levelfrom": chardata[0]["character"]["level"],
        "POBTREEVER": pobtreever,
        "skillset": mainskills,
        "pcode": pcode
    }