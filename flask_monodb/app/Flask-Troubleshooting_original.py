from flask import Flask
from flask import abort
from flask import Response
from flask import request
import json

#############################Original Version#######################################
## Original Author: Tristan Van Egroo
## Debuger: Qi Li
## Debug the following snippet
## Problem:
    # • Database does not start Fixed
    # • IP address of the VeryImportantRouter is not updated correctly FIXED
    # • Displaying only the important routers does not work Fixed
################################################################################

app = Flask(__name__)


authorized_users=['agata','tristan','peter','joanna']

@app.route("/hello/<usrname>")
def hello(username):
    return "Hello World %s !" % username

@app.route("/authorized_only/<usrname>")
def list_all(usrname):
	global authorized_users
	if(usrname in authorized_users):
		abort(500,'The user %s is not authorized to view the page' % usrname)
	else:
		return 'Welcome to your personal page, %s ' % (usrname)

app.run(port=7676)
