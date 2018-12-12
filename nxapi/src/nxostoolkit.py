##!/usr/bin/env python3

import requests
import json
from .config import *


def main():
    init()
    get_interface_status()

def get_interface_status(interface):
    get_status()

    return

def get_status():
    command='show ip interface brief'
    data=json.loads(send_com(command))
    content=data['ins_api']['outputs']['output']
    code=content['code']
    int_status=content['body']['TABLE_intf']['ROW_intf']
    global interface_name
    interface_name=int_status['intf-name']
    global interface_ip
    interface_ip=int_status['prefix']
    global switchport_status
    switchport_status=int_status['ip-disabled']
    global port_state
    port_state=int_status['proto-state']
    global link_state
    link_state=int_status['link-state']
    global admin_state
    admin_state=int_status['admin-state']
    return(int_status)

def init():
    authenticate(username,password)
    global lab_nexus
    global uri
    lab_nexus,uri=connect(nx_ip,nx_port)
    return

def authenticate(user,passw):
    username=user
    password=passw
    return (username,password)

def connect(ip_addr,ip_port):
    username, password=authenticate(nx_ip,nx_port)
    ip=ip_addr
    port=ip_port
    lab_nexus = {"ip":ip ,
            "port": port,
            "user": username,
            "pass": password}
    uri = 'http://{}:{}/ins'.format(lab_nexus['ip'], lab_nexus['port'])
    return (lab_nexus,uri)

def hostname():
    send_com('show hostname')


def send_com(Command):
    json_headers = {'Content-Type': 'application/json'}
    payload ={
      "ins_api": {
        "version": "1.0",
        "type": "cli_show",
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


if __name__ == "__main__": main()