from pymongo import MongoClient
from bson.json_util import dumps

import json


##########################Original Version######################################
## Author:Tristan Van Egroo
## Debug the following snippet
## Problem:
    # • Database does not start
    # • IP address of the VeryImportantRouter is not updated correctly
    # • Displaying only the important routers does not work
################################################################################


def get_mongo():
    print('Connecting')
    client   = MongoClient("127.0.0.1",270017)
    return client['my_nice_database']
    print('Connected')

def display_row(r):
    print('------- Database Dump --------')    
    for i in r:
         print(dumps(i))
    print('------------------------------')
def main_code():
    db = get_mongo()
    table = db.hosts

    # Clean start, deleting everything from the table.
    table.delete_many({})

    # Inserting 5 routers into the table

    rows_to_insert = [{'hostname':'VeryImportantRouter','ip':'1.1.1.1','domain':'Incubator.com'},
                      {'hostname':'VeryImportantBackupRouter','ip':'1.1.1.2','domain':'Incubator.com'},
                      {'hostname':'NotSoImportantRouter','ip':'1.1.1.3','domain':'Incubator.com'},
                      {'hostname':'NetFlixRouter','ip':'1.1.1.4','domain':'Home.com'},
                      {'hostname':'CoreRouter','ip':'1.1.1.5','domain':'Home.com'}]

    res = table.insert_many(rows_to_insert)

    # Display all database
    print('\nDisplaying all entries in DB')
    res = table.find()
    display_row(res)    

    # Update the IP address of the very important router to 2.2.2.2 and dump the DB after that
    print('\nAfter update of IP address')
    res = table.update_one({'Hostname':'VeryImportantRouter'},{'$set':{'ip':'2.2.2.2'}})
    res = table.find()
    display_row(res)

    # Listing only the Important routers    
    print('\nDisplaying only the important routers')
    res = table.find({'hostname':{'$regex':'ImportantRouter.'}})
    display_row(res)

main_code()
