# -*- coding:utf8 -*-
# !/usr/bin/env python
import time
import json
import os

from flask import Flask
from flask import request
from flask import make_response

from db.menu_models import *

import courses_crawler

#Google Maps API
#AIzaSyB6ByDVZ9g2cXdnPqd0rgBSuceK66j6K2A


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
        res = makeMenuWebhookResult(data)
        return res
    elif req.get("result").get("action") in "course.lookup":
        parameters = req.get("result").get("parameters")
        searchString = parameters['course_list'] + "+" + str(parameters['number-integer'])
        return makeCourseWebhookResult(courses_crawler.search_course(searchString))
    elif req.get("result").get("action") in "building.lookup":
        parameters = req.get("result").get("parameters")
        return makeBuildingWebhookResult(parameters['building'])


def makeBuildingWebhookResult(data):
    addressURL = data + "%2C University Park%2C PA"
    addressURL = addressURL.replace(" ", "+")
    key="AIzaSyCeehrTvN-wy1sJUqP5B-D4wRXZsKHE6Fc"
    speech = "Here is the location of "+data+": <br/>"
    speech += "<a href='https://www.google.com/maps/search/?api=1&query="+addressURL+"'><img src='https://maps.googleapis.com/maps/api/staticmap?center="+addressURL+"&zoom=15&size=200x200&key="+key+"'></img></a>"
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

def makeCourseWebhookResult(data):
    speech = "Here are your results: <br/>" + data
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

def makeMenuWebhookResult(data):
    foodList = data['food_items'].split(", ")
    food_items = ""
    if (len(foodList) > 5):
        for i in range(0,5):
            food_items += foodList[i] +"<br/>"
        food_items = food_items.rstrip(", ")
        food_items += "The full menu can be found <a href='http://menu.hfs.psu.edu'>here</a>."
        
    else:
        food_items =data['food_items']
    speech = "For " + data['menu']+", " + data['location'] + " is serving: <br/> "+food_items

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

if __name__ == "__main__":
    app.run()

