from flask import Flask
from flask import abort
from flask import Response
from flask import request
import json

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
