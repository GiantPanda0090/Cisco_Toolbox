
###################################################
# Parse vlan status
# 
# Students will need to parse the output of a "show vlan" from a NXOS devices
# and return a dictionary with the parsed info
# 
# How the text input will look like:
# 
# 
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Po213, Eth1/1, Eth1/2, Eth1/3
#                                                 Eth1/4
# 10   Vlan10                           active    Po1, Po10, Po111, Po213, Eth1/2
#                                                 Eth1/5, Eth1/16, Eth1/17
#                                                 Eth1/18, Eth1/49, Eth1/50
# How the output must look like:
# 
# vlan_db = {
# 	"1": {
# 		"Name": "default",
# 		"Status": "active",,
# 		"Ports": ["Po213", "Eth1/1"...]
# 	},
# 	"2":{},
# 	...
# }
#
###################################################

from paramiko import SSHClient
import re
import getpass
import pprint

def demo():
    vlan_info=None
    port=None
    username =None
    password=None
    host=input('Enter the ip address of the Nexus9000v Swiches: ')
    while len(host)==0:
        host=input('Host Can not be empty. please enter the ip address of the host nexus 9000v switches. if user decide to use default offline\n'
                   'file, please enter Offline\nEnter the ip address of the Nexus9000v Swiches: ')
    if (host=='Offline'):
        print('Loading vlan information from offline file')
        file=open('test_vlan_info.txt','r')
        vlan_info=file.read()
    else:
        port=input('Enter the port number of the ssh connection(default is 22): ')
        if len(port)==0:
            port =22
        username=input('Enter the switch username: ')
        password=getpass.getpass(prompt='Enter the switch password: ', stream=None)
        #password=input('Enter the switch password: ')
    if vlan_info == None:
        vlan_info=ssh(host,port,username,password,"show vlan")
    vlan_db=get_vlan_db(vlan_info)
    pprint.pprint(vlan_db)
    return(vlan_db)

def get_vlan_db(text):
    print("parsing vlan information")
    expression_0=r"((VLAN)(\s+)(Name)(\s+)(Status)(\s+)(Ports)(\n))" \
                 r"(([\-,\s]+)(\n))" \
                 r"(((\d+)(\s+)(((\w+)(\s+)){2})(\s*((Eth\d+\/\d+)(\,?)(\s?)))+)+)"
    vlan_form=re.search(expression_0,text).group(13)
    expression_1=r"(((\d+)(\s+)(((\w+)(\s+)){2})(\s*((Eth\d+\/\d+)(\,?)(\s?)))+))"
    vlan_info_list=re.findall(expression_1,vlan_form)
    # vlan_db = {
    # 	"1": {
    # 		"Name": "default",
    # 		"Status": "active",,
    # 		"Ports": ["Po213", "Eth1/1"...]
    # 	},
    # 	"2":{},
    # 	...
    # }
    vlan_db={}

    for vlan_info in vlan_info_list:
        dict,vlan_number=parse_per_vlan_info(vlan_info)
        vlan_db[vlan_number]=dict
    #return vlan_db
    return vlan_db

def parse_per_vlan_info(vlan_info):
    expression_number=r"(\d+)(\s+)"
    expression_name_status_number=r"\b([A-Z a-z 0-9]+)(\s)\b"
    expression_ports=r"(((Eth\d+\/\d+)))"
    expression_word=r"\b(\w+)\b"
    vlan_name_status_number =re.search(expression_name_status_number,str(vlan_info)).group()
    vlan_name_status_number_list=re.findall(expression_word,str(vlan_name_status_number))
    vlan_number =vlan_name_status_number_list[0]
    vlan_name =vlan_name_status_number_list[1]
    vlan_status =vlan_name_status_number_list[2]
    vlan_list=re.findall(expression_ports,str(vlan_info))
    vlan_port_list=[]
    for parse_info in vlan_list:
        vlan_port_list.append(parse_info[0])

    dict={}
    dict['Name']=vlan_name
    dict['Status']=vlan_status
    dict['Ports']=vlan_port_list

    return (dict,vlan_number)

def ssh(host,port,username,password,command):
    print("obtaining vlan information from "+host+" via ssh")
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ##connect(hostname, port=22, username=None, password=None, pkey=None, key_filename=None, timeout=None, allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=True, passphrase=None)
    ssh.connect(host,port=port,username=username,password=password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    output=(str(ssh_stdout.read().decode('ascii')))  # print the output of ls command
    ssh.close()
    print("vlan information is obtained and have been saved offlinie at 'test_vlan_info.txt'")
    demo_file=open('test_vlan_info.txt','w+')
    demo_file.write(output)
    demo_file.close()
    return output

    ##main class trigger
if __name__ == "__main__":
    demo()