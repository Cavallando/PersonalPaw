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
        res = makeMenuWebhookPayload(data)
        return res
    elif req.get("result").get("action") in "course.lookup":
        parameters = req.get("result").get("parameters")
        searchString = parameters['course_list'] + "+" + str(parameters['number-integer'])
        return makeCourseWebhookPayload(courses_crawler.search_course(searchString))
    elif req.get("result").get("action") in "building.lookup":
        parameters = req.get("result").get("parameters")
        return makeBuildingWebhookPayload(parameters['building'])
    elif req.get("result").get("action") in "event.athletics.lookup":
        parameters = req.get("result").get("parameters")
        data = {'date':parameters['date'],'sport':parameters.get("sport", ""),'gender':parameters.get("gender", "")}
        return makeAthleticEventPayload(data)
        

def makeWebhookResult(payload):
    return {
        "speech": payload,
        "displayText": payload,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

def makeAthleticEventPayload(data):
    data= data


def makeBuildingWebhookPayload(data):
    addressURL = data + "%2C University Park%2C PA"
    addressURL = addressURL.replace(" ", "+")
    key="AIzaSyCeehrTvN-wy1sJUqP5B-D4wRXZsKHE6Fc"
    payload = json.dumps({'text': "Here is the location of "+data+": ", 'link':"https://www.google.com/maps/search/?api=1&query="+addressURL, 'image':"https://maps.googleapis.com/maps/api/staticmap?center="+addressURL+"&zoom=15&size=200x200&key="+key})
    return makeWebhookResult(payload)

def makeCourseWebhookPayload(data):
    payload = json.dumps({'text':"Here are your results: " + data,'link':"",'image':''})
    return makeWebhookResult(payload)

def makeMenuWebhookPayload(data):
    foodList = data['food_items'].split(", ")
    food_items = ""
    if (len(foodList) > 5):
        for i in range(0,5):
            food_items += foodList[i] +"<br/>"
        food_items = food_items.rstrip(", ")
        food_items += "The full menu can be found <a href='http://menu.hfs.psu.edu'>here</a>."
        
    else:
        food_items =data['food_items']
    speech = "For " + data['menu']+", " + data['location'] + " is serving: "+food_items
    payload = json.dumps({'text':speech,'link':"",'image':''})
    return makeWebhookResult(payload)

if __name__ == "__main__":
    app.run()

