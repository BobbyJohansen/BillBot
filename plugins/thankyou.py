"""bill <equation> will return the google calculator result for <equation>"""
from bs4 import BeautifulSoup
import re
from urllib import quote
import requests

def thankyou(text):
    #if (text.find(" no ") == -1) and (text.find("no ") == -1) and (text.find(" no") == -1):
    return "You're welcome."

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"((?i).*(thank).*(you).*(bill).*$)|((?i).*(thanks).*(bill).*$)", text)
    if not match:
        match = re.findall(r"(?i)bill\:\s+(thank).*(you).*",text)
        if not match: return

    return thankyou(text)
