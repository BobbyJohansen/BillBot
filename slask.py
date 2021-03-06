#!/usr/bin/env python
from __future__ import print_function
from glob import glob
import importlib
import logging
import os
import re
import sys
import time
import traceback
import requests
import json

from slackclient import SlackClient
attach = 0

def init_log(config):
    loglevel = config.get("loglevel", logging.INFO)
    logformat = config.get("logformat", '%(asctime)s:%(levelname)s:%(message)s')
    if config.get("logfile"):
        logfile = config.get("logfile", "slask.log")
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)

    handler.setLevel(loglevel)

    # create formatter
    formatter = logging.Formatter(logformat)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # make it the root logger (I hate the logging module)
    logging.root = logger

def init_plugins(plugindir):
    hooks = {}

    for plugin in glob(os.path.join(plugindir, "[!_]*.py")):
        logging.debug("plugin: {0}".format(plugin))
        try:
            mod = importlib.import_module(plugin.replace(os.path.sep, ".")[:-3])
            modname = mod.__name__.split('.')[1]
            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                hookfun = getattr(mod, "on_" + hook)
                logging.debug("attaching {0}.{1} to {2}".format(modname, hookfun, hook))
                hooks.setdefault(hook, []).append(hookfun)

            if mod.__doc__:
                firstline = mod.__doc__.split('\n')[0]
                hooks.setdefault('help', {})[modname] = firstline
                hooks.setdefault('extendedhelp', {})[modname] = mod.__doc__

        #bare except, because the modules could raise any number of errors
        #on import, and we want them not to kill our server
        except:
            logging.info("import failed on module {0}, module not loaded".format(plugin))
            logging.info("{0}".format(sys.exc_info()[0]))
            logging.info("{0}".format(traceback.format_exc()))

    return hooks

def run_hook(hooks, hook, data, server):
    responses = []
    for hook in hooks.get(hook, []):
        h = hook(data, server)
        if h: responses.append(h)

    return responses

def handle_message(client, event, hooks, config):
    # ignore bot messages and edits
    subtype = event.get("subtype", "")
    if subtype == "bot_message" or subtype == "message_changed": return

    botname = client.server.login_data["self"]["name"]
    try:
        msguser = client.server.users.get(event["user"])
    except KeyError:
        logging.debug("event {0} has no user".format(event))
        return

    if msguser["name"] == botname or msguser["name"].lower() == "slackbot":
        return

    #this is expecting a string for event aka body may need to look as to how to pass json
    #see slackbot-python for example of returning the right json need attachement section
    response = run_hook(hooks, "message", event, {"client": client, "config": config, "hooks": hooks})
    logging.warn("RESPONSE TYPE  {0}".format(type(response)))


    if len(response) == 0:
        return
    if type(response[0]) is str:
        return "\n".join(response)
        
    elif type(response[0]) is list:
        print ('list me timbers')
        url = "https://hooks.slack.com/services/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"
        icon = 'http://theredlist.com/media/database/muses/icon/cinematic_men/1980/bill-murray/002-bill-murray-theredlist.jpg'
        channel = event["channel"]
        # Don't fucking touch the index. It makes everything wonderful.
        payload = {'channel': channel,'username': 'bill', 'icon_url': icon, 'attachments': response[0]}
        reqresponse = requests.post(url, data=json.dumps(payload), timeout=5)
        
        logging.warn("RESPONSE: {0}".format(reqresponse))
        return
        
    elif type(response) is dict:
        for item in response:
            if 'fallback' in item:
                url = "https://hooks.slack.com/services/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"
                icon = 'http://theredlist.com/media/database/muses/icon/cinematic_men/1980/bill-murray/002-bill-murray-theredlist.jpg'
                channel = event["channel"]
                payload = {'channel': channel,'username': 'bill', 'icon_url': icon, 'attachments': response}
                reqresponse = requests.post(url, data=json.dumps(payload), timeout=5)
                logging.warn("RESPONSE: {0}".format(reqresponse))
                return
    
        
        
    #for item in response:
       # if 'fallback' in item:



    return "\n".join(response)

event_handlers = {
    "message": handle_message
}



def main(config):
    hooks = init_plugins("plugins")

    client = SlackClient(config["token"])
    if client.rtm_connect():
        users = client.server.users
        while True:
            events = client.rtm_read()
            for event in events:
                #print "got {0}".format(event.get("type", event))
                handler = event_handlers.get(event.get("type"))
                if handler:
                    response = handler(client, event, hooks, config)
                    if response:
                        client.rtm_send_message(event["channel"], response)
            time.sleep(1)
    else:
        logging.warn("Connection Failed, invalid token <{0}>?".format(config["token"]))

if __name__=="__main__":
    from config import config

    init_log(config)
    main(config)
