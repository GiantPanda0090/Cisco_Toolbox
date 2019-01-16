##########################################################################################
# Flask View/API module
# Author:Qi Li
# partial of the code with assistant from stack overflow and other website
##########################################################################################

from flask import Flask, render_template, request, jsonify

from tshoot import *

from mongo import *
import re

import json
import pymongo

from bson import ObjectId


# basckup object id stringifier under json
# Other solution used: use flask jsonify as dict['_id']=str(dict['_id']) jsonify(dict)
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)


# Control Panel View
# Templet: index.html
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # title extraction
    titles = dict(0, 0, 0, home_phone=0, work_phone=0)
    titles = list(titles.keys())
    titles.insert(0, '_id')
    entries = display_entries()
    # submit buttons and text boxes handler
    if request.method == 'POST':
        if request.form['action'] == 'Generate random Address Book entry':
            id = insert_new_entry(example_generator())
            result = collection.find({"$and": [{"_id": id}]})
            entries = display_entries()
            return render_template('index.html', entry=result, entries=entries, titles=titles)
        elif request.form['action'] == 'Delete Entry':
            first_name = request.form['FirstName']
            last_name = request.form['LastName']
            (id, result) = delete_entries(first_name, last_name)
            entries = display_entries()
            return render_template('index.html', entry=result, entries=entries, titles=titles)
        elif request.form['action'] == 'List Entry':
            first_name = request.form['FirstName']
            last_name = request.form['LastName']
            result = display_entries(first_name, last_name)
            return render_template('index.html', entry=result, entries=entries, titles=titles)
        elif re.match('update_\w*', request.form['action']) != None:
            id = str(re.match('update_\w*', request.form['action']).group()).split('_')[1]
            first_name = request.form[id + '_First Name']
            last_name = request.form[id + '_Last Name']
            email = request.form[id + '_Email address']
            phone_home = request.form[id + '_Home Phone Number']
            phone_work = request.form[id + '_Work Phone Number']
            dict_1 = dict(first_name, last_name, email, home_phone=phone_home, work_phone=phone_work)
            new_id = insert_new_entry(dict_1, id)
            result = collection.find({"$and": [{"_id": new_id}]})
            entries = display_entries()
            return render_template('index.html', entry=result, entries=entries, titles=titles)
        elif request.form['action'] == 'Create Address Book Entry':
            first_name = request.form['FirstName_create']
            if len(first_name) == 0:
                first_name = 'n/a'

            last_name = request.form['LastName_create']
            if len(last_name) == 0:
                last_name = 'n/a'

            email = request.form['Email_create']
            if len(email) == 0:
                email = 'n/a'

            phone_home = request.form['Home_Phone_create']
            if len(phone_home) == 0:
                phone_home = 'n/a'

            phone_work = request.form['Work_Phone_create']
            if len(phone_work) == 0:
                phone_work = 'n/a'
            error = ''
            try:
                result = dict(first_name, last_name, email, home_phone=phone_home, work_phone=phone_work)
            except Exception as e:
                error = str(e)
                result = {}
            else:
                new_id = insert_new_entry(result)
                entries = display_entries()
                result = collection.find({"$and": [{"_id": new_id}]})
            return render_template('index.html', entry=result, error=error, entries=entries, titles=titles)

    return render_template('index.html', entry=None, entries=entries, titles=titles)


# External API

# list all entries
@app.route('/api/v1.0/entries', methods=['GET'])
def api_all_entries():
    entries = display_entries()
    output = {}
    for entry in entries:
        output[entry['_id']] = [entry]
    return jsonify(output)


# list specific entry base on first and last name
@app.route('/api/v1.0/entry/<string:first_name>/<string:last_name>', methods=['GET'])
def api_one_entry(first_name, last_name):
    entries = display_entries(first_name, last_name)
    output = {}
    for entry in entries:
        output[entry['_id']] = [entry]
    return jsonify(output)


# list specific entry base on Objectid
@app.route('/api/v1.0/entry/<string:id>', methods=['GET'])
def api_one_entry_id(id):
    first_name, last_name = '', ''
    result = collection.find({"$and": [{"_id": ObjectId(id)}]})
    for item in result:
        first_name = item['First Name']
        last_name = item['Last Name']
    entries = display_entries(first_name, last_name)
    output = {}
    for entry in entries:
        output[entry['_id']] = [entry]
    return jsonify(output)


# update specific/multiple data in specific entry. Data injection should be under headers as parameter.
# key allowed:'Ad-First-Name','Ad-Last-Name','Ad-Email-Address','Ad-Home-Phone','Ad-Work-Phone'
@app.route('/api/v1.0/entry/<string:id>', methods=['PUT'])
def api_update_entry(id):
    result = request.headers
    keys = result.keys()
    dictionary = {'Ad-First-Name': 'n/a', 'Ad-Last-Name': 'n/a', 'Ad-Email-Address': 'n/a', 'Ad-Home-Phone': 'n/a',
                  'Ad-Work-Phone': 'n/a'}
    for key in keys:
        if str(key).split('-')[0] == 'Ad':
            dictionary[key] = result.get(key)

    dict_1 = dict(dictionary['Ad-First-Name'], dictionary['Ad-Last-Name'], dictionary['Ad-Email-Address'],
                  home_phone=dictionary['Ad-Home-Phone'], work_phone=dictionary['Ad-Work-Phone'])
    new_id = insert_new_entry(dict_1, id)
    new_entries = collection.find({"$and": [{"_id": new_id}]})

    out = {}
    for entry in new_entries:
        entry['_id'] = str(entry['_id'])
        out = entry
    return jsonify(out)


# add a new entry into the databsae
@app.route('/api/v1.0/entry', methods=['POST'])
def api_add_one_entry():
    result = request.form['ad_dict']
    result = json.loads(result)

    first_name = result['First Name']
    if len(first_name) == 0:
        first_name = 'n/a'

    last_name = result['Last Name']
    if len(last_name) == 0:
        last_name = 'n/a'

    email = result['Email address']
    if len(email) == 0:
        email = 'n/a'

    phone_home = result['Home Phone Number']
    if len(phone_home) == 0:
        phone_home = 'n/a'

    phone_work = result['Work Phone Number']
    if len(phone_work) == 0:
        phone_work = 'n/a'
    output = {}
    try:
        result = dict(first_name, last_name, email, home_phone=phone_home, work_phone=phone_work)
    except Exception as e:
        error = str(e)
        result = {"Error": error}
    else:
        new_id = insert_new_entry(result)
        result = collection.find({"$and": [{"_id": new_id}]})
        for item in result:
            item['_id'] = str(item['_id'])
            output = item
    return jsonify(output)


# delete one entry in the database base on first and last name
@app.route('/api/v1.0/entry/<string:first_name>/<string:last_name>', methods=['DELETE'])
def api_delete_entry(first_name, last_name):
    (id, result) = delete_entries(first_name, last_name)
    return "Deleted: {0} \n".format(result)


# main calss trigger
# flask app run under port 7676 (does not work on development server)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='7676')
