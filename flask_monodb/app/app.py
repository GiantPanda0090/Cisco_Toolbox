from flask import Flask,render_template,request,jsonify


from mongo import *
import re

import json
import pymongo

from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



app = Flask(__name__)

#Control Panel View
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    titles=dict(0,0,0,home_phone=0,work_phone=0)
    titles=list(titles.keys())
    titles.insert(0,'_id')
    entries =display_entries()
    if request.method == 'POST':
        if request.form['action'] == 'Generate random Address Book entry':
            id=insert_new_entry(example_generator())
            result = collection.find({"$and": [{"_id": id}]})
            entries = display_entries()
            return render_template('index.html',entry=result,entries=entries,titles=titles)
        elif request.form['action']=='Delete Entry':
            first_name=request.form['FirstName']
            last_name=request.form['LastName']
            (id,result) = delete_entries(first_name,last_name)
            entries = display_entries()
            return render_template('index.html',entry=result,entries=entries,titles=titles)
        elif request.form['action'] == 'List Entry':
            first_name = request.form['FirstName']
            last_name = request.form['LastName']
            result = display_entries(first_name,last_name)
            return render_template('index.html',entry=result,entries=entries,titles=titles)
        elif re.match('update_\w*',request.form['action']) != None:
            id=str(re.match('update_\w*',request.form['action']).group()).split('_')[1]
            first_name=request.form[id+'_First Name']
            last_name=request.form[id+'_Last Name']
            email=request.form[id+'_Email address']
            phone_home=request.form[id+'_Home Phone Number']
            phone_work=request.form[id+'_Work Phone Number']
            dict_1=dict(first_name,last_name,email,home_phone=phone_home,work_phone=phone_work)
            new_id=insert_new_entry(dict_1,id)
            result = collection.find({"$and": [{"_id":new_id}]})
            entries=display_entries()
            return render_template('index.html',entry=result,entries=entries,titles=titles)
        elif request.form['action'] == 'Create Address Book Entry':
            
            return render_template('index.html',entry=result,entries=entries,titles=titles)


    return render_template('index.html',entry =None,entries=entries,titles=titles)


#API
@app.route('/api/v1.0/all_entries', methods=['GET'])
def api_all_entries():
    entries =display_entries()
    output={}
    for entry in entries:
        output[entry['_id']]=[entry]
    return jsonify(output)


@app.route('/api/v1.0/entry/<string:first_name>/<string:last_name>', methods=['GET'])
def api_one_entry(first_name,last_name):
    entries = display_entries(first_name,last_name)
    output = {}
    for entry in entries:
        output[entry['_id']] = [entry]
    return jsonify(output)

@app.route('/api/v1.0/entry/<string:id>', methods=['GET'])
def api_one_entry_id(id):
    first_name, last_name='',''
    result =  collection.find({"$and": [{"_id":ObjectId(id)}]})
    for item in result:
        first_name=item['First Name']
        last_name=item['Last Name']
    entries = display_entries(first_name,last_name)
    output = {}
    for entry in entries:
        output[entry['_id']] = [entry]
    return jsonify(output)


@app.route('/api/v1.0/entry/<string:id>', methods=['PUT'])
def update_entry(id):
    result=request.headers
    keys=result.keys()
    dictionary={'Ad-First-Name':'n/a','Ad-Last-Name':'n/a','Ad-Email-Address':'n/a','Ad-Home-Phone':'n/a','Ad-Work-Phone':'n/a'}
    for key in keys:
        if str(key).split('-')[0]=='Ad':
            dictionary[key]=result.get(key)

    dict_1 = dict(dictionary['Ad-First-Name'], dictionary['Ad-Last-Name'], dictionary['Ad-Email-Address'], home_phone=dictionary['Ad-Home-Phone'], work_phone=dictionary['Ad-Work-Phone'])
    new_id = insert_new_entry(dict_1, id)
    new_entries = collection.find({"$and": [{"_id": new_id}]})

    out={}
    for entry in new_entries:
        entry['_id']=str(entry['_id'])
        out=entry
    return jsonify(out)



@app.route('/api/v1.0/delete_entry/<string:first_name>/<string:last_name>', methods=['DELETE'])
def api_delete_entry(first_name,last_name):
    (id, result) = delete_entries(first_name, last_name)
    return "Deleted: {0} \n".format(result)



if __name__ == '__main__':
    app.run()
