# **Regex Switch Information Parser**
The purpose of this module is create a toolbox for extract useful information form switch CLI output. Some module include function to directly extract information from the switch via SSH. At test banch, the Nexus 9000v is running under VMware® Workstation 14 Pro-14.1.2 build-8497320. Programming language is Python 3.6.4 :: Anaconda, Inc.

## Project structure
.<br />
├── demo_find_src_types.txt<br />
├── find_crc_types.py<br />
├── ip_validator.py<br />
├── README.md<br />
├── README.me<br />
├── remove_dup_words.py<br />
├── requirements.txt<br />
├── test_vlan_info.txt<br />
└── vlan_db.py<br />

## Prequisition
Run command: pip3 install -r requirments.txt 

## Excute Modules
Run command: python3 \<module name>.py


## find_crc_types.py
 Parse internal CRC counters of a Nexus


##  ip_validator.py
IP address validator

## remove_dup_words.py
Find the duplicate words in the given text,  and return the string without duplicates.

## vlan_db.py
Parse vlan status

