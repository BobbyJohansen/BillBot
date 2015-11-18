# -*- coding: utf-8 -*-
"""bill what is the weather in <zip or place name> return the 5-day forecast"""

from urllib import quote
import re
import requests
import time

# http://openweathermap.org/weather-conditions
iconmap = {
    "01": ":sunny:",
    "02": ":partly_sunny:",
    "03": ":partly_sunny:",
    "04": ":cloud:",
    "09": ":droplet:",
    "10": ":droplet:",
    "11": ":zap:",
    "13": ":snowflake:",
    "50": ":umbrella:", #mist?
}

def weather(searchterm):
    print 'weathering the storm'
    searchterm = quote(searchterm)
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={0}&cnt=5&mode=json&units=imperial&APPID=0f86b804395e5ea7759da43fa3df4315'
    url = url.format(searchterm)

    print url
    dat = requests.get(url)
    print dat
    dat = dat.json()

    msg = ["{0}: ".format(dat["city"]["name"])]
    for day in dat["list"]:
        name = time.strftime("%a", time.gmtime(day["dt"]))
        high = str(int(round(float(day["temp"]["max"]))))
        icon = iconmap.get(day["weather"][0]["icon"][:2], ":question:")
        msg.append(u"{0} {1}° {2}".format(name, high, icon))

    return " ".join(msg)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"bill what is the weather in (.*)", text)
    if not match: return

    searchterm = match[0]
    return weather(searchterm)
