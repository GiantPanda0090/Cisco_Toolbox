
###################################################
# Parse internal CRC counters of a Nexus
# The students will have to parse the next output, and return a dictionary,
# with the parsed info
# 
# How the text input will look like:
#
# --------------------------------------------------------------------------------
# Port          Align-Err    FCS-Err   Xmit-Err    Rcv-Err  UnderSize OutDiscards
# --------------------------------------------------------------------------------
# Eth1/1                0          0          0          0          0           0
# Eth1/2                0          0          0          0          0           0
# Eth1/3                0          0          0          0          0           0
# Eth1/4                0          0          0          0          0           0
# <snip>
#
# --------------------------------------------------------------------------------
# Port         Single-Col  Multi-Col   Late-Col  Exces-Col  Carri-Sen       Runts
# --------------------------------------------------------------------------------
# Eth1/1                0          0          0          0          0           0
# Eth1/2                0          0          0          0          0           0
# <snip>
#
# --------------------------------------------------------------------------------
# Port          Giants SQETest-Err Deferred-Tx IntMacTx-Er IntMacRx-Er Symbol-Err
# --------------------------------------------------------------------------------
# Eth1/1             0          --           0           0           0          0
# Eth1/2             0          --           0           0           0          0
#
# How the output must look like:
#
# int_dict = {
# 	"Eth1/1": {
# 		"Align-Err": 0,
# 		"FCS-Err": 0,
# 		...
# 	}
# }
###################################################

import re
import json

def demo():
    input = load_file('demo_find_src_types.txt')
    #print(input)
    out=get_error_counters(input)
    print(out)



def load_file(file_path):
    file=open(file_path,'r')
    item=file.read()
    return (item)

def seperate_form(text):
    expression_1 = r"(\s\-+)\n" \
                   r"(((\s+)((\w+\-\w+)|(\w+)))+)\n" \
                   r"(\s\-+)\n" \
                   r"((((\s([A-Z,a-z]{3}[1-9]\/[1-9]))(((\s+)([0-9]|\-\-))+))\n)+)"
    search_1 = re.findall(expression_1,text)
    return search_1

def get_Err_form(search_1):
    expression_0 = r"(\w+)(\-E(r+))"
    form_Err = []
    for form in search_1:
        matched_form = re.findall(expression_0, form[1])
        if matched_form:
            form_Err.append(form)
    return(form_Err)




def get_error_counters(text):
    search_1 = seperate_form(text)
    form_Err=get_Err_form(search_1)
    Err_data=[]
    expression_0 = r"(\w+)(\-E(r+))"
    Err_data_interface = {}

    for Err_form in form_Err:
        titles=str(Err_form[1]).split()

        counter =0
        content = Err_form[8].split('\n')
        for item in content:
            data = item.split()
            if len(data) != 0:
                if data[0] not in Err_data_interface:
                    Err_data_interface[str(data[0])]={}

        for title in titles:
            matched_title = re.search(expression_0, title)
            if matched_title:
                for item in content:
                    data=item.split()
                    if len(data) != 0:
                        Err_data_interface[str(data[0])][matched_title.group()]=data[counter]

            counter+=1


    interfaces_dict=(Err_data_interface)

    return interfaces_dict

##main class trigger
if __name__ == "__main__":
    demo()