from pymongo import MongoClient
from bson.json_util import dumps

import json
import re #new


#############################Fixed Version#######################################
## Original Author: Tristan Van Egroo
## Debuger: Qi Li
## Debug the following snippet
## Problem:
    # • Database does not start Fixed
    # • IP address of the VeryImportantRouter is not updated correctly FIXED
    # • Displaying only the important routers does not work Fixed
################################################################################


def get_mongo():
    print('Connecting')
    client   = MongoClient("127.0.0.1",27017)##270017 -> 27017
    print('Connected')
    return client['my_nice_database']


def display_row(r):
    print('------- Database Dump --------')    
    for i in r:
         print(dumps(i))
    print('------------------------------')
def main_code():
    db = get_mongo()
    table = db['hosts']##db.hosts -> db['hosts']

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
    res = table.update_one({'hostname':'VeryImportantRouter'},{'$set':{'ip':'2.2.2.2'}})#    res = table.update_one({'Hostname':'VeryImportantRouter'},{'$set':{'ip':'2.2.2.2'}}) ->  res = table.update_one({'hostname':'VeryImportantRouter'},{'$set':{'ip':'2.2.2.2'}})
    res = table.find()
    display_row(res)

    # Listing only the Important routers    
    print('\nDisplaying only the important routers')

    ##{'hostname':{'$regex':'ImportantRouter.'}} -> pattern=re.compile(r'\b((?!Not).)*Important') res = table.find({'hostname':{'$regex':pattern}})
    pattern=re.compile(r'\b((?!Not).)*Important')
    res = table.find({'hostname':{'$regex':pattern}})

    display_row(res)

##Orgnize the main function trigger formation
## main_code() -> if __name__ == "__main__": main_code()
if __name__ == "__main__":
    main_code()

