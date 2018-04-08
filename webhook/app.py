# -*- coding:utf8 -*-
# !/usr/bin/env python
import time
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import datetime
from db.menu_models import *

import courses_crawler
import athletics_crawler
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
        query = req.get("result").get("resolvedQuery") 
        data = {'query':query, 'date': parameters.get("date", ""),'sport':parameters.get("gender", "")+" "+parameters.get("sport", "")}
        return makeAthleticEventPayload(data)
        

def makeWebhookResult(payload):
    return {
        "speech": payload,
        "displayText": "",
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

def makeAthleticEventPayload(data):
    event = {}
    events = []
    payload=""
    text =""
    if ("NEXT" in data['query'].upper()):
        if data['sport']:
            event = athletics_crawler.next_event_by_sport(data)
        else:
            data['date'] = datetime.date.today().strftime('%Y-%m-%d')
            event = athletics_crawler.next_event(data)
        if not event:
            text = "I'm sorry, I couldn't locate that event!"
        else:
            day = datetime.date(day=int(event['date'][8:10]), month=int(event['date'][5:7]), year=int(event['date'][:4])).strftime('%A, %d %B %Y')
                
            text = "The next event is for "+event['sport']+ " is on "+ day +""
    else:
        if data['date']:
            events = athletics_crawler.search_events_by_date(data)
            if not events:
                text = "I'm sorry, I couldn't locate that event!"
            else:
                day = datetime.date(day=int(data['date'][8:10]), month=int(data['date'][5:7]), year=int(data['date'][:4])).strftime('%A, %d %B %Y')
                text = "Here are the events for "+day+": "
        elif data['sport']:
            events = athletics_crawler.search_event_by_sport(data)
            if not events:
                text = "I'm sorry, I couldn't locate that event!"
            else:
                e = events[0]
                day = date(day=e['date'][8:10], month=int(e['date'][5:7]), year=int(e['date'][:4])).strftime('%A, %d %B %Y')
                text = "The next event is on " + day + ": "
    if not event and not events:
        payload = json.dumps({"text":text,"event":""})
    elif event and not events:
        events.append(event)
        payload = json.dumps({"text":text,"event":events[0]})
    else:
        payload = json.dumps({"text":text,"event":events[0]})

    return makeWebhookResult(payload)


def makeBuildingWebhookPayload(data):
    addressURL = data + "%2C University Park%2C PA"
    addressURL = addressURL.replace(" ", "+")
    key="AIzaSyCeehrTvN-wy1sJUqP5B-D4wRXZsKHE6Fc"
    payload = json.dumps({'text': "Here is the location of "+data+": ", 'link':"https://www.google.com/maps/search/?api=1&query="+addressURL, 'image':"https://maps.googleapis.com/maps/api/staticmap?center="+addressURL+"&zoom=15&size=200x200&key="+key,"location":data})
    return makeWebhookResult(payload)

def makeCourseWebhookPayload(data):
    payload = json.dumps({'text':"Here are your results: " + data,'link':"",'image':''})
    return makeWebhookResult(payload)

def makeMenuWebhookPayload(data):
    foodList = data['food_items'].split(", ")
    speech = "For " + data['menu']+", " + data['location'] + " is serving: "
    payload = json.dumps({'text':speech,'food_items': foodList})
    return makeWebhookResult(payload)

if __name__ == "__main__":
    app.run()

