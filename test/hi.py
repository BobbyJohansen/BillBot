"""bill hi"""
from bs4 import BeautifulSoup
import re
from urllib import quote
import requests
import random

def msg():
    set1 = ['yo', 'hey', 'hi', 'Hi', 'hello', 'Hello', 'Welcome']
    set2 = ['~', '~~~', '!', '?', ' :)', ':D', 'xD', '(Y)', '(y)', ':P', ':-D', ';)', ', How do you do?']
    respond = str1 + ' ' + str2 for str1 in set1 for str2 in set2
    print respond
    response = choice(set1)
    return "hi"
    

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"^\s*(([Hh]+([AaEe]+[Ll]+[Oo]+|[Ii]+)+\s*(all)?)|[Yy]+[Oo]+|[Aa]+[Ll]+|[Aa]nybody)\s*(!+|\?+|~+|.+|[:;][)DPp]+)*$", text)
    if not match: "nope"

    return msg()
