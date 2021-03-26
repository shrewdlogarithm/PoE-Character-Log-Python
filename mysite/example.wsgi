# This is an example WSGI to install the mysite application somewhere like PythonAnywhere
# Simply copy the code below to the WSGI file on the server and edit the "project_home" to point to where your code is installed

import bottle
import os
import sys
  
# add your project directory to the sys.path
project_home = '/home/YOURPYTHONANYWHEREUSERNAME/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
  
if project_home not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, project_home)
  
# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_home, 'views/')
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)
  
# import bottle application
from bottle_app import application`