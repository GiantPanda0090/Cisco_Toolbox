# **NX-API Toolbox**
The purpose of this module is create a toolbox for interatct with Cisco Nexus 9000v switches. The API used is NX-API CLI. Nexus 9000v is running under VMware® Workstation 14 Pro-14.1.2 build-8497320. Programming language is Python 3.6.4 :: Anaconda, Inc.

## config.py
Configuration file for nxostoolkit.py. Incude username,password,ip address and port number  The file can be regenerate from nxostoolkit.py.  Username and Password section is encrypted.


## nxostoolkit.py
main class for NX--API Toolbox

**Structure**

Router object
class Router(object):

\##demo <br />
def main():

\##get the version of the hardware <br />
def get_version():


\##get the model of the hardware <br />
def get_plattform():

\##get the feedback of the 'show version' <br />
def get_showversion():


\##configure the description of the interface <br />
def configure_interface_desc(intf,descpt):


\##adapt all interface name <br />
def parse_if(interface):


\##get the status of the interface <br />
def get_interface_status(intf):


\##get the status per interface <br />
def get_interface_state(interface):


\##parse the admin state <br />
def get_interface_admin_state(row):


\##parse the link state <br />
def get_interface_link_state(row):


\##parse the proto state <br />
def get_interface_proto_state(row):

\##parse the ip-disabled <br />
def get_interface_swtichport_stat(row):


\##parse the prefix <br />
def get_interface_ip(row):

\##parse intf-name <br />
def get_interface_name(row):


\##collect the feedback of 'show ip interface brief' <br />
def get_status():



\##encrypt text <br />
def encrypt(str):


\##decrypt cypher <br />
def decrypt(cipher):


\##initialization of the class <br />
def init():
def dynamic_auth():


\##authentication info import <br />
def authenticate(user,passw):

\##connection information import/json formate for hardware <br />
def connect(ip_addr,ip_port):


\##get the hostname <br />
def hostname():

\##send command to the hardware <br />
def send_com(Command,type):