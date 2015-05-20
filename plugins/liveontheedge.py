"""bill youtube <search term> return the first youtube search result for <search term>"""

import re
from urllib import quote

import requests

def theNights():
    return "https://www.youtube.com/watch?v=UtF6Jej8yb4"

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"bill how do you want to be remembered?", text)
    if not match: return

    return theNights()
