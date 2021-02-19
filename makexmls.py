import json,glob
from charparser import makexml

POEChars = glob.glob('data/*-*.json')

for POEChar in POEChars:

    xmname = POEChar.replace(".json",".xml").replace("data","pob/builds")

    with open(POEChar, encoding='utf-8') as json_file:
        print(POEChar)
        chardata = json.load(json_file)
        if int(chardata[len(chardata)-1]["character"]["level"]) > 10:
            root = makexml(chardata)
            xml_str = root.toprettyxml(indent ="\t")
            with open(xmname, "w") as f:
                f.write(xml_str)
