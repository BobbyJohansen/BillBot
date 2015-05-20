"""bill <equation> will return the google calculator result for <equation>"""
from bs4 import BeautifulSoup
import re
from urllib import quote
import requests

def msg(text):
    return 'I love you too.'

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(?i)((bill)\[,:]\s*i.*love|i.*love.*(bill).*)", text)
    if not match: return

    return msg(text)
