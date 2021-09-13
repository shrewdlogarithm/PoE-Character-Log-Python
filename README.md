# PoE-Character-Log-Python #
## Path of Exile Character Log - track any PoE character as it's played ##

This is VERY much work-in-progress - sharing for feedback/ideas!

### What it Does ###
Download Passives, Skills and Items for any character which has been active on the Accounts you choose to monitor.
Create a 'Build Log' showing changes to the character over-time
Create a Path-of-Building Pastecode/XML which contains the same data

[PoEClog in less than 60s (YouTube Link)](https://www.youtube.com/watch?v=Mje0pl9L8sY)

## How to Use ##
Run "scan_all"
This runs endlessly, tracking characters as they are played...  

The first time you run this it creates "settings.json" - edit that to  
Specify the account(s) you wish to monitor.  
Specify short (between API accesses) and long (between scans or after errors) sleep times between scans
Specify the max level to consider a character "new" and the max level to monitor any character at all

Note: settings.json is read every time the scanner loops - no-need to restart!

## What it creates ##
In the 'data' directory 
JSON files which are a complete dump of API data for Tree, Skills and Items - 1 entry per scan

In the "logs" directory 
LOG files - textfiles detailing changes made to a character over-time
HTML files - the same content as the LOG but hyperlinked/colourized 

In the "pob/builds" directory 
XML - a Path-of-Building-compatible savefile 

## Other stuff ##
The "mysite" directory contains a Bottle.py application which creates a webpage summarizing all the accounts/characters tracked  
This also includes PoB "build codes" which can be pasted into PoB directly  
To see an example of this, this site tracks popular PoE streamers  
http://poeclog.pythonanywhere.com

rebuildlogxml re-creates all log/html/xml files  
This can be useful to update older characters when changes are made to the parsing/output

## Known Issues ##
If someone creates multiple characters with the same name, data from all those characters will be gathered into a single .json file
This means PoB output etc. will be nonsensical - but I'm also not really sure what to do with this right now so...
The only person who really does this is Zizaran - try to die less than he does perhaps? :)

## Notes ##
There is  a Powershell version of this for desktop use/people who don't want to install Python  
https://github.com/shrewdlogarithm/PoE-Character-Log-PS  
It lags behind the Python version in features but it's data gathering is identical (JSON files can be interchanged between the PS and Python versions)

## Running this on PythonAnywhere ##
Clone this repo into PythonAnywhere and it should "just work"  

_Update: whilst this would, in theory, work on a free account, GGG recently changed how their API works and the site we need to access is not currently 'whitelisted' at PythonAnywhere.  I have asked the to add it - I'll update here when they respond to that..._  
_Note: CPU limits on free accounts mean you won't be able to track more than 1 or 2 characters and/or may need to increase the pause between scans (Longwait) in settings.json_  

To get the 'mysite' Bottle.py app working...  
- Create a new WebApp, choose "Manual Configuration" and "Python 3.8"  
- Then, edit the WSGI and copy the code from [this file](mysite/example.wsgi)  
