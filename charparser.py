import base64,zlib,json,re,os
from xml.dom import minidom 
from datetime import datetime

POBTREEVER = "3_13"

with open('passive-skill-tree.json') as json_file:
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
                    group = item["sockets"][gem]["group"]
                    if item["socketedItems"][gem]["colour"] and item["socketedItems"][gem]["typeLine"]: 
                        gemstr = "<a class=gem" + item["socketedItems"][gem]["colour"] + " href=\"https://pathofexile.gamepedia.com/" + item["socketedItems"][gem]["typeLine"].replace(" ","_") + "\">" + item["socketedItems"][gem]["typeLine"] + "</a>"
                    elif  item["socketedItems"][gem]["typeLine"]:
                        gemstr = item["socketedItems"][gem]["typeLine"]
                    else:
                        gemstr = "Unknown Gem!"
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
            #for gem in sorted(group["gems"]):
            #    ret.append(gem)
            #for gem in sorted(group["supports"]):
            #    ret.append(f'{gem} >> {" ".join(group["gems"])}')
            if len(group["gems"]) > 0 or len(group["supports"]) > 0:
                ret.append(" | ".join(group["gems"]) + " >> " + " | ".join(group["supports"]))
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
        return True
    else:
        return False

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

def makexml(account,char,chardata,accountdb):
    root = minidom.Document()     
    pob = root.createElement('PathOfBuilding')  
    root.appendChild(pob) 
    accountdb["levelfrom"] = chardata[0]["character"]["level"]
    accountdb["league"] = chardata[len(chardata)-1]["character"]["league"]
    build = root.createElement('Build')
    build.setAttribute("targetVersion","3_0")
    build.setAttribute('level',str(chardata[len(chardata)-1]["character"]["level"]))
    build.setAttribute('className',className[chardata[len(chardata)-1]["character"]["classId"]])
    build.setAttribute('ascendClassName',ascendName[chardata[len(chardata)-1]["character"]["classId"]][chardata[len(chardata)-1]["character"]["ascendancyClass"]])
    build.setAttribute("viewMode","ITEMS")
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
    skilldb = []
    itemdb = {}
    lastset = {}
    itn = 1
    isn = 1
    for e in range(0,len(chardata)):
        level = chardata[e]["character"]["level"]
        lastnodes = ",".join(str(node) for node in chardata[e-1]["passives"])
        nodes = ",".join(str(node) for node in chardata[e]["passives"])
        if nodes != lastnodes:
            id = root.createElement("Spec")
            id.setAttribute("title",f'{e} - Level {chardata[e]["character"]["level"]}')
            id.setAttribute("ascendClassId",str(chardata[e]["character"]["ascendancyClass"]))
            id.setAttribute("nodes",nodes)
            id.setAttribute("treeVersion",POBTREEVER)
            id.setAttribute("classId",str(chardata[e]["character"]["classId"]))
            tree.appendChild(id)   
        gemgroups = buildskills(chardata[e]["items"])  
        mainskills = []
        for slot in gemgroups:
            skill = root.createElement("Skill")
            for group in gemgroups[slot]:                    
                if (len(group["supports"]) > 0):
                    for gm in group["gems"]:
                        mainskills.append("[" + str(len(group["supports"])) + "] " + re.sub('<[^>]+>', '', gm))
                if len(group["gems"]) > 0:
                    skillset = " ".join(sorted(group["gems"])) + " " + ",".join(sorted(group["supports"]))
                    skillset = re.sub('<[^>]+>', '', skillset).replace(" Support","")
                    if skillset not in skilldb:
                        skilldb.append(skillset)
                        for gm in group["gems"]+group["supports"]:
                            gem = root.createElement("Gem")
                            gem.setAttribute("level","1")
                            gem.setAttribute("nameSpec",re.sub('<[^>]+>', '',gm.replace(" Support","")))
                            gem.setAttribute("quality","0")
                            gem.setAttribute("enabled","true")
                            skill.appendChild(gem)
                        skill.setAttribute("label",f"{level}-{skillset}")
                        skill.setAttribute("enabled","true")                        
                        skills.appendChild(skill)
        if len(mainskills) > 0:
            accountdb["skillset"] = re.sub("\[[0-9]*\] ","","  ".join(sorted(set(mainskills[0:4]),reverse=True)))
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
                    itemtext = itemtext.replace(chr(246),"o") # the Maelstrom 'o'
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
    accountdb["pcode"] = base64.b64encode(zlib.compress(root.toxml().encode('ascii')),altchars=b"-_").decode("ascii")
    with open(f"pob/builds/{account}-{char}.xml", 'w') as f:
        f.write(root.toprettyxml(indent ="\t"))