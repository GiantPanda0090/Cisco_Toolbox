

import pymongo
import names
import random
import string

#############################Database Structure#################################
################################################################################
        # ◦ First Name
        # ◦ Last Name
        # ◦ Email address (not mandatory, should not be stored in the document if omitted)
        # ◦ Home and Work phone numbers (Either of them are not mandatory fields)
#################################################################################



#mongodb initialization
def init(ip="localhost",port=27017,database_name="test",collec="incubator"):
    address="mongodb://"+ip+":"+str(port)+"/"
    myclient = pymongo.MongoClient(address)
    mydb = myclient[database_name]
    collection=mydb[collec]
    return collection


collection=init()


#demo
def demo():
    #input
    print('inserting random sample')
    id=insert_new_entry(example_generator())
    print('insertion item has new id: '+str(id))
    #delete
    entries =display_entries()
    result=delete_entries(entries[0]['First Name'], entries[0]['Last Name'])
    if result==1:
        print('Entries successfully removed from the database')
    else:
        print("Something wrong delete failed")
    #show all entries
    print("printing all entries")
    entries =display_entries()
    for entrie in entries:
       print(entrie)

    # show specific entries
    print("printing specific entries")
    entries_1 =display_entries()
    entries = display_entries(entries_1[0]['First Name'],entries_1[0]['Last Name'])
    for entrie in entries:
        print(entrie)
    return


#create dictionary
def dict(first_name,last_name,*email,**phone):
    dict={"First Name":first_name,"Last Name":last_name}

    if len(email) >1:
        raise Exception('dict() function cotain too many parameter. The function suppose to be used as <dict(first name, last name,email(optional),home or/and work phone numer>')

    if len(email) != 0:
        dict["Email address"]=email[0]

    if 'home_phone'in phone:
        home_phone=phone['home_phone']
        dict["Home Phone Number"]=home_phone
    if 'work_phone' in phone:
        work_phone=phone['work_phone']
        dict["Work Phone Number"]=work_phone


    return dict

#generate example dict
def example_generator():
    first_name=names.get_first_name()
    last_name=names.get_last_name()
    email=first_name+'_'+last_name+'@'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))+'.se'
    home_phone=''.join(random.choice(string.digits) for _ in range(10))
    work_phone=''.join(random.choice(string.digits) for _ in range(10))
    dictionary={}
    email_choice=random.randint(0,1)
    phone_choice=random.randint(0,2)
    if email_choice==0:
        if phone_choice==0:
            dictionary = dict(first_name, last_name, home_phone=home_phone)
        elif phone_choice==1:
            dictionary = dict(first_name, last_name, work_phone=work_phone)
        else:
            dictionary = dict(first_name, last_name, work_phone=work_phone, home_phone=home_phone)
    else:
        if phone_choice==0:
            dictionary = dict(first_name, last_name,email, home_phone=home_phone)
        elif phone_choice==1:
            dictionary = dict(first_name, last_name,email, work_phone=work_phone)
        else:
            dictionary = dict(first_name, last_name,email, work_phone=work_phone, home_phone=home_phone)
    return dictionary




#insert new entry. if exist update base on names
def insert_new_entry(dict:dict):
    id =0
    first_name=dict.get('First Name')
    last_name=dict.get('Last Name')

    result=collection.find({"$and": [{"First Name": first_name},
                          {"Last Name": last_name}]})
    if result.count() == 0:
        item=collection.insert_one(dict)
        id =item.inserted_id
    else:
        for item in result:
            for key in dict.keys():
                collection.update_one({"_id": item['_id']},{"$set": {key:dict[key]} })
                id=item['_id']
            #print(item['_id'])


    return id



def display_entries(firstname=None,lastname=None):
    if firstname == None and lastname == None:
        result = collection.find().sort([("First Name",pymongo.ASCENDING),("Last Name",pymongo.ASCENDING)])
    else:
        result = collection.find({"$and": [{"First Name": firstname},
                                       {"Last Name": lastname}]}).sort([("First Name",pymongo.ASCENDING),("Last Name",pymongo.ASCENDING)])
    output=[]

    for item in result:
            output.append(item)
    return output

def delete_entries(firstname=None,lastname=None):
    result = collection.delete_many({"$and": [{"First Name": firstname},
                                       {"Last Name": lastname}]})
    return result.deleted_count



    ##main class trigger
if __name__ == "__main__":
    demo()