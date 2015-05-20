"""bill do the dan flan dance"""

from urllib import quote
import re
import requests
from random import shuffle

def gif(unsafe=False):

    return "https://raw.githubusercontent.com/BobbyJohansen/imgs/master/dan.png"

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"bill do the dan flan dance", text)
    if not match: return

    searchterm = match[0]
    return gif()
