
###################################################
# IP address validator 
# details: https://en.wikipedia.org/wiki/IP_address
# Student should enter function on the next lines.
# 
# 
# First function is_valid_ip() should return:
# True if the string inserted is a valid IP address
# or False if the string is not a real IP
# 
# 
# Second function get_ip_class() should return a string:
# "X is a class Y IP" or "X is classless IP" (without the ")
# where X represent the IP string, 
# and Y represent the class type: A, B, C, D, E
# ref: http://www.cloudtacker.com/Styles/IP_Address_Classes_and_Representation.png
# Note: if an IP address is not valid, the function should return
# "X is not a valid IP address"
###################################################

import re

def demo():
    print(get_ip_class("192.168.0.1"))


def extract_ip_dig(correct_formate_ip):
    expression_1=r"(\d+)"
    ip_per_dig = re.findall(expression_1, correct_formate_ip)
    return ip_per_dig


def is_valid_ip(ip): #xxx.xxx.xxx.xxx 0-255
    valid_flag=True
    expression_0=r"^((\d+)(\.)){3}(\d+)$"
    correct_formate=re.match(expression_0,ip)
    if correct_formate:
        correct_formate_ip = correct_formate.group()
        ip_per_dig=extract_ip_dig(correct_formate_ip)
        range_flag=check_ip_range(ip_per_dig)
        if range_flag==False:
            valid_flag=False
    else:
        valid_flag=False
    return valid_flag

def check_ip_range(ip_dig_list):
    range_flag= True
    for dig in ip_dig_list:
        dig_int=int(dig)
        if dig_int<0 or dig_int >255:
            range_flag=False
    return range_flag


def define_ip_class(ip_per_dig):
    ip_class=None
    first_octa=int(ip_per_dig[0])
    if first_octa>=1 and first_octa<=127:#class A
        ip_class="A"
    elif(first_octa>=128 and first_octa<=191):#class B
        ip_class="B"
    elif (first_octa >= 192 and first_octa <= 223):  # class C
        ip_class = "C"
    elif (first_octa >= 224 and first_octa <= 239):  # class D
        ip_class = "D"
    elif (first_octa >= 240 and first_octa <= 255):  # class E
        ip_class = "E"
    else:
        ip_class=None
    return ip_class

def get_ip_class(ip):
    ip_class=None
    return_text= "X is classless IP"
    valid_flag=is_valid_ip(ip)
    if valid_flag==False:
        return_text=ip+" is not a valid IP address"
    else:
        ip_per_dig=extract_ip_dig(ip)
        ip_class=(define_ip_class(ip_per_dig))
        if ip_class:
            return_text= ip+" is a class "+ip_class +" IP"

    return return_text

    ##main class trigger
if __name__ == "__main__":
    demo()

