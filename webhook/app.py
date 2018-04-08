# -*- coding:utf8 -*-
# !/usr/bin/env python
import time
import json
import os

from flask import Flask
from flask import request
from flask import make_response

from db.menu_models import *



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
    #Request is name of Intent on DialogFlow
    if req.get("result").get("action") in "menu.lookup":
        parameters = req.get("result").get("parameters")
        date = parameters["date"]
        location = parameters["dining_commons"]
        menu = parameters["menu"]
        data = {'date':date,'location':location,'menu':menu,'food_items':select_menu(date,location, menu)}
        res = makeWebhookResult(data)
        return res

def makeWebhookResult(data):
    foodList = data['food_items'].split(", ")
    food_items = ""
    if (len(foodList) > 5):
        for i in range(0,5):
            food_items += foodList[i] +", "
        food_items = food_items.rstrip(", ")
        food_items += "\nThe full menu can be found at http://menus.hfs.psu.edu\n"
        
    else:
        food_items =data['food_items'].rstrip(",")
    speech = "For " + data['menu']+", " + data['location'] + " is serving: \r\n "+food_items

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

if __name__ == "__main__":
    app.run()

