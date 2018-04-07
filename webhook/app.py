# -*- coding:utf8 -*-
# !/usr/bin/env python
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import time
import json
import os

from flask import Flask
from flask import request
from flask import make_response

from db.models import *

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "menu.lookup":
        parameters = req.get("parameters")
        date = parameters['date']
        location = parameters['dining_commons']
        menu = parameters['menu']
        data = {'date':date,'location':location,'menu':menu,'food_items':select_menu(date,location, menu)}
        res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    speech = data['menu'] + " is serving: \n "+ data['food_items']

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

