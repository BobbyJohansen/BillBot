"""Show Bill some love by telling him you love him"""
from bs4 import BeautifulSoup
import re
from urllib import quote
import requests

def message(text):
    return 'I love you too.'

def on_message(msg, server):
    text = msg.get("text", "")
    # match = re.findall(r"(?i)((bill)\[,:]\s*i.*love|i.*love.*(bill).*)", text)
    match = re.findall(r"((i)\[,:]\s*i.*love|i.*love.*(bill|you).*)", text)
    if not match: return

    return message(text)
