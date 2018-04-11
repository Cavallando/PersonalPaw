# -*- coding:utf8 -*-
# !/usr/bin/env python
import time
import json
import os
import re
import datetime

from flask import Flask, request, make_response

from icalendar import Calendar
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup

import courses_crawler as courses
import athletics_crawler as athletics
import menu_crawler as menus


#Google Maps API
#AIzaSyB4iA2SBVcos3SO0NHJp8v7zqEhLZFxf5c


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
        return makeMenuWebhookPayload(parameters)
    elif req.get("result").get("action") in "course.lookup":
        parameters = req.get("result").get("parameters")
        searchString = parameters['course_list'] + "+" + str(parameters['number-integer'])
        return makeCourseWebhookPayload({'course':courses.search_course(searchString)})
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
        "displayText": payload,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    }

def makeAthleticEventPayload(data):
    event = {}
    payload=""
    text =""
    if ("NEXT" in data['query'].upper()):
        if data['sport']:
            event = athletics.search_event_by_sport(data)
        else:
            data['date'] = datetime.date.today().strftime('%Y-%m-%d')
            event = athletics.next_event(data)
        if not event:
            text = "I'm sorry, I couldn't locate any event from your search. The full calendar of events can be found "
        else:
            data['date'] = datetime.date(day=int(event['date'][8:10]), month=int(event['date'][5:7]), year=int(event['date'][:4])).strftime('%A, %d %B %Y')
                
            text = "The next "+shortSport(event['sport'])+ " event is on "+ data['date'] +""
    else:
        if data['date']:
            event = athletics.search_events_by_date(data)
            if not event:
                text = "I'm sorry, I couldn't locate any event from your search. The full calendar of events can be found "
            else:
                data['date'] = datetime.date(day=int(data['date'][8:10]), month=int(data['date'][5:7]), year=int(data['date'][:4])).strftime('%A, %d %B %Y')
                text = "This event is on "+data['date']+": "
        elif data['sport']:
            event = athletics.search_event_by_sport(data)
            if not event:
                text = "I'm sorry, I couldn't locate any event from your search. The full calendar of events can be found "
            else:
                data['date'] = datetime.date(day=int(event['date'][8:10]), month=int(event['date'][5:7]), year=int(event['date'][:4])).strftime('%A, %d %B %Y')
                text = "The next event is on " + data['date']+ ": "
    if not event:
        payload = json.dumps({"text":text,"event":{"summary":"","date":"","sport":"","location":"","description":"http://www.gopsusports.com/calendar/events/"}})
    else:
        event['sport']=shortSport(event['sport'].strip())
        payload = json.dumps({"text":text,"event":event})

    return makeWebhookResult(payload)

def shortSport(data):
    sports = {"Baseball":"Baseball","FBALL":"Football","Hockey":"Hockey","BBALL":"Basketball","Cross Country":"Cross Country","Fence":"Fencing","Golf":"Golf","GYM":"Gymnastics","LAX":"Lacrosse","SWIM":	"Swimming & Diving","TNNS":"Tennis","Track":"Track & Field","VB":"Volleyball","Men's Wrestling":"Wrestling","SB":"Softball"}
    return sports[data]

def makeBuildingWebhookPayload(data):
    addressURL = data + "%2C University Park%2C PA"
    addressURL = addressURL.replace(" ", "+")
    key="AIzaSyB4iA2SBVcos3SO0NHJp8v7zqEhLZFxf5c"
    payload = json.dumps({'text': "Here is the location of "+data+": ", 'link':"https://www.google.com/maps/search/?api=1&query="+addressURL, 'image':"https://maps.googleapis.com/maps/api/staticmap?center="+addressURL+"&zoom=15&size=200x200&key="+key,"location":data})
    return makeWebhookResult(payload)

def makeCourseWebhookPayload(data):
    payload = json.dumps({'text':data,'link':"",'image':''})
    return makeWebhookResult(payload)

def makeMenuWebhookPayload(data):
    foodList = menus.scrape_menus(data).split(', ')[:7]
    speech = "For " + data['menu']+", " + data['dining_commons'] + " is serving: "
    payload = json.dumps({'text':speech,'food_items': foodList})
    return makeWebhookResult(payload)


if __name__ == "__main__":
    app.run(debug=True)

