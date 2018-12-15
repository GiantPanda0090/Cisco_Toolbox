##!/usr/bin/env python3


##AUTHOR:QI LI
##DATE: 2018 DEC 15
##MODULE:NXAPI


###################################################
##Nexus 9000v toolbox mainclass
##Hard coded configuration info is in config.py
####################################################

import requests
import json
import config
import importlib
import base64
import getpass


##Router object
class Router(object):

    def __init__(self, i_var):
        self.i_var = i_var
        self.version=get_version()
        self.platform=get_plattform()





##demo
def main():
    init()
    print('#########################Demo Result#############################')
    print(hostname())
    print(get_interface_status('Ethernet1/2'))
    print(configure_interface_desc('Eth1/2','test'))
    router=Router(0)
    print(router.version)
    print(router.platform)
    print('##################################################################')


##get the version of the hardware
def get_version():
    body=get_showversion()
    version=body['kickstart_ver_str']
    return version

##get the model of the hardware
def get_plattform():
    body=get_showversion()
    plattform = body['chassis_id']
    return plattform

##get the feedback of the 'show version'
def get_showversion():
    command='show version'
    data = json.loads(send_com(command,"cli_show"))
    content = data['ins_api']['outputs']['output']
    body=content['body']
    return body

##configure the description of the interface
def configure_interface_desc(intf,descpt):
    interface=parse_if(intf)
    command='interface '+interface+' ; description '+descpt
    data = json.loads(send_com(command,"cli_conf"))
    content = data['ins_api']['outputs']['output']
    counter=0
    out=''
    for code_perreq in content:
        counter+=1
        code = code_perreq['code']
        if code != '200':
            print('Error at configure_interface_desc. code: ' + code)
            print('Error at number '+counter+' lines of command')
            out = 'Failed'
    else:
        out='OK'

    return ['desc_update_'+interface,out]

##adapt all interface name
def parse_if(interface):
    length=len(interface)
    return(interface[0:3]+interface[length-3:length])

##get the status of the interface
def get_interface_status(intf):
    interface=parse_if(intf)
    row = get_interface_state(interface)
    if len(row) != 0 or row !='n/a':
        proto_state=get_interface_proto_state(row)
        link_state=get_interface_link_state(row)
        admin_state=get_interface_admin_state(row)
    else:
        proto_state = 'N/A'
        link_state ='N/A'
        admin_state = 'N/A'
    #result=interface+' : '+admin_state+' / '+proto_state+' / '+link_state
    #print(result)
    return (['interface_status',interface,admin_state,proto_state,link_state])

##get the status per interface
def get_interface_state(interface):
    int_status=get_status()
    if int_status=='n/a':
        return 'n/a'
    out={}
    for address in int_status:
        if address =='ROW_intf':
            row =int_status['ROW_intf']
        else:
            row=address['ROW_intf']
        interface_name = get_interface_name(row)
        if interface_name ==interface:
            out=row
            break

    return(out)

##parse the admin state
def get_interface_admin_state(row):
    admin_state = row['admin-state']
    return (admin_state)

##parse the link state
def get_interface_link_state(row):
    link_state = row['link-state']
    return (link_state)


##parse the proto state
def get_interface_proto_state(row):
    port_state = row['proto-state']
    return (port_state)

##parse the ip-disabled
def get_interface_swtichport_stat(row):
    switchport_status = row['ip-disabled']
    return (switchport_status)

##parse the prefix
def get_interface_ip(row):
    interface_ip = row['prefix']
    return (interface_ip)

##parse intf-name
def get_interface_name(row):
    interface_name = row['intf-name']
    return (interface_name)

##collect the feedback of 'show ip interface brief'
def get_status():
    command='show ip interface brief'
    data=json.loads(send_com(command,"cli_show"))
    content = data['ins_api']['outputs']['output']
    code = content['code']
    if code !='200':
        print('Error at get_status. code: '+code)
        int_status='n/a'
    else:
    ##print(content)
        int_status = content['body']['TABLE_intf']
    return int_status


##encrypt text
def encrypt(str):
    str_encode = str.encode("utf-8")
    out=base64.b64encode(str_encode)
    return out


#decrypt cypher
def decrypt(cipher):
    out=base64.b64decode(cipher)
    str_decode = out.decode("utf-8")
    return str_decode



##initialization of the class
def init():
    print('1. Use current config.py setting \n 2. Use new setting')
    choice = input('Your Choice: ')
    if choice=='2':
        (u,p,ip,port)=dynamic_auth()
        config_file = open('config.py', 'w+')
        config_file.writelines(['##!/usr/bin/env python3\n','\n','##AUTHOR:QI LI\n','##DATE: 2018 DEC 15\n','##MODULE:NXAPI\n','\n','####################################################################\n','##configuration of nxostoolkit.py\n','####################################################################\n','\n',
                              'username='+str(encrypt(u))+'\n','password='+str(encrypt(p))+'\n','nx_ip='+'\"'+ip+'\"\n','nx_port='+'\"'+port+'\"\n'])
        config_file.close()
        importlib.reload(config)
    else:
        importlib.reload(config)


    authenticate(decrypt(config.username),decrypt(config.password))
    global lab_nexus
    global uri
    lab_nexus,uri=connect(config.nx_ip,config.nx_port)
    return


def dynamic_auth():
    ip = input('The router IP address: ')
    port = input('The router port number: ')
    user = input('Enter your username: ')
    passw = getpass.getpass('Enter your password: ')


    return(user,passw,ip,port)


##authentication info import
def authenticate(user,passw):
    global login
    global secret
    login=user
    secret=passw
    return (login,secret)

##connection information import/json formate for hardware
def connect(ip_addr,ip_port):
    ip=ip_addr
    port=ip_port
    lab_nexus = {"ip":ip ,
            "port": port,
            "user": login,
            "pass": secret}
    uri = 'http://{}:{}/ins'.format(lab_nexus['ip'], lab_nexus['port'])
    return (lab_nexus,uri)

##get the hostname
def hostname():
    data = json.loads(send_com('show hostname',"cli_show"))
    out=data['ins_api']['outputs']['output']['body']['hostname']
    return(['hostname',out])

##send command to the hardware
def send_com(Command,type):
    json_headers = {'Content-Type': 'application/json'}
    payload ={
      "ins_api": {
        "version": "1.0",
        "type": type,
        "chunk": "0",
        "sid": "1",
        "input": Command,
        "output_format": "json"
      }
    }

    response = requests.post(uri,
                             data=json.dumps(payload),
                             headers=json_headers,
                             auth=(lab_nexus["user"], lab_nexus["pass"]))

    return(response.text)


##main class trigger
if __name__ == "__main__":
    main()