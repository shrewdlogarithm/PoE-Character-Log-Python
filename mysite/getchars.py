import os,base64,zlib,glob
from xml.dom import minidom


def getchars():
    retval = {}

    for pobfile in sorted(glob.glob('pob/builds/*.xml')):
        print(pobfile)
        accchar = os.path.basename(pobfile).replace(".xml","")
        datapath = "data/" + os.path.basename(pobfile).replace(".xml",".json")
        logpath = "logs/" + os.path.basename(pobfile).replace(".xml",".log")
        htmlpath = "logs/" + os.path.basename(pobfile).replace(".xml",".html")
        account,charname = accchar.split("-")
        if account not in retval:
            retval[account] = []
        try:
            with minidom.parse(pobfile) as dom:
                classname = dom.getElementsByTagName("Build")[0].getAttribute("className")
                ascendClassname = dom.getElementsByTagName("Build")[0].getAttribute("ascendClassName")
                if ascendClassname != "None":
                    classname = ascendClassname
                summary = dom.getElementsByTagName("Summary")
                if len(summary) > 0:
                    levelfrom = dom.getElementsByTagName("Summary")[0].getAttribute("LevelFrom")
                    levelto = dom.getElementsByTagName("Summary")[0].getAttribute("LevelTo")
                retval[account].append({
                    "filepath": pobfile,
                    "datapath": datapath,
                    "logpath": logpath,
                    "htmlpath": htmlpath,
                    "account": account,
                    "charname": charname,
                    "classname": classname,
                    "levelfrom": levelfrom,
                    "levelto": levelto,
                    "pcode": base64.b64encode(zlib.compress(dom.toxml().encode('ascii')),altchars=b"-_")
                })
        except Exception as e:
            print(e)
    return retval