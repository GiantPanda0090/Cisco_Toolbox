
###################################################
# Duplicate words 
# The students will have to find the duplicate words in the given text,
# and return the string without duplicates.
#
###################################################

import re

def demo():
    print(remove_duplicates("the bus bus will never be a bus bus in a bus bus bus"))

def remove_duplicates(text):
	#write here
    exression_0=r"\b(\w+)(?!\s+\1)\b"

    text_with_no_dup_list=re.findall(exression_0,text)
    text_with_no_dup=""
    for word in text_with_no_dup_list:
        text_with_no_dup=text_with_no_dup+" "+word
    return text_with_no_dup



    ##main class trigger
if __name__ == "__main__":
    demo()