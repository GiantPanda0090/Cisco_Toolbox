# **Pymongo/Flask Test Banch**
The purpose of this module is create a testbranch for query/insert/modify information from mongodb database with pymongo Programming language is Python 3.6.4 :: Anaconda, Inc.

## Project structure

.<br />
├── app<br />
│   ├── app.py<br />
│   ├── Flask-Troubleshooting_original.py<br />
│   ├── Flask-Troubleshooting.py<br />
│   ├── mongo.py<br />
│   ├── Mongo-Troubleshooting_original.py<br />
│   ├── Mongo-Troubleshooting.py<br />
│   ├── __pycache__<br />
│   ├── static<br />
│   ├── templates<br />
│   │   └── index.html<br />
│   └── venv<br />
│   │   └── ...<br />
├── document<br />
│   ├── Flask.docx<br />
│   └── Mongo.docx<br />
├── mongo.py -> app/mongo.py<br />
├── Mongo-Troubleshooting.py -> app/Mongo-Troubleshooting.py<br />
├── README.md<br />
├── README.me<br />
└── requirements.txt<br />
<br />
165 directories, 1181 files<br />


## Prequisition
Run command: pip3 install -r requirments.txt 

## Excute Modules (.py file)
Run command: python3 \<module name>.py

## Excute Modules (Flask)
Run command to start local development server: flask run 
Access address to open Control Panel in develpment server:`http://localhost:5000/`
Query external RestAPI under development server: `http://localhost:5000/api/v1.0/<request>`


# document
  Documentation of the project
  
## Mongo.docx
Purpose and requirments for Mongodb part of this module. Reference to Cisco Systems bld.C. Author:Tristan Van Egroo

## Flask.docx
Purpose and requirments for Flask refactor and functionality part of this module. Reference to Cisco Systems bld.C. Author:Tristan Van Egroo
# app
  Flask/Main Application folder
   
## app.py
 Main Controller of Flask Framework

## mongo.py
 Create/modify/query an address book in mongodb
 
## Flask-Troubleshooting_original.py
Code that has issue that need to be fixed. Fixed version are in Flask-Troubleshooting.py <br />
Author:Tristan Van Egroo

## Flask-Troubleshooting.py
Fixed version of Flask-Troubleshooting_original.py<br />
Original Author:Tristan Van Egroo<br />
Debuger: Qi Li<br />

## Mongo-Troubleshooting_original.py
Code that has issue that need to be fixed. Fixed version are in Mongo-Troubleshooting_original.py <br />
Author:Tristan Van Egroo <br />

##  Mongo-Troubleshooting.py
Fixed version of Mongo-Troubleshooting_original.py<br />
Original Author:Tristan Van Egroo<br />
Debuger: Qi Li<br />


# RestAPI documentation
Documentation for RestAPI usage in app.py. The API is used as `http://<address of the Rest server>:<port>/<address that stated below>'`

## Get all entries
`'/api/v1.0/entries'`, methods:'GET'<br />

## List specific entry base on first and last name
`'/api/v1.0/entry/<string:first_name>/<string:last_name>'`, methods:'GET'<br />

## List specific entry base on Objectid
`'/api/v1.0/entry/<string:id>'`, methods:'GET'<br />'

## Update specific/multiple data in specific entry
`'/api/v1.0/entry/<string:id>'`, methods:'PUT'<br />
Data injection should be under headers as parameter.<br />
key allowed:'Ad-First-Name','Ad-Last-Name','Ad-Email-Address','Ad-Home-Phone','Ad-Work-Phone'<br />

## add a new entry into the databsae
`'/api/v1.0/entry'`, methods:'POST'
## delete one entry in the database base on first and last name
`'/api/v1.0/entry/<string:first_name>/<string:last_name>'`, methods:'DELETE'
