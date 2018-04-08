
from icalendar import Calendar
import urllib
import datetime
import re
#def get_calendar(): 

def get_events():
    ics = open('files/events.ics','rb')
    cal = Calendar.from_ical(ics.read())
    eventList = []
    fmt = '%Y-%m-%d'
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            dtstart = component.get('dtstart').dt.strftime(fmt)
            location = component.decoded('location')
            description =  component.decoded('description')
            if("Ticket Office:" in description):
                description = description[:-190]
            else:
                description = description[:-150]
            description =  description.replace("\n","")
            sport = summary[summary.find("(")+1:summary.find(")")]
            eventList.append({'summary': summary.replace("("+sport+")",""),'sport': sport, 'description':description, 'date':dtstart,'location':location})
        #if eventList:
        #    break
        #else:
        #    date = datetime.strptime(data['date'], fmt)
        #    date += datetime.timedelta(days=1)
        #    data['date'] = date.strftime(fmt)
    ics.close()
    return eventList

def next_event(data):
    event_list = get_events()
    date = data['date']
    while True:
        for event in event_list:
            if(date in event['date']):
                return event
        date = datetime.strptime(date, '%Y-%m-%d')
        date += datetime.timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        if date[:4] == "2019":
            return None

def next_few_events(data):
    event_list = get_events()
    events=[]
    for event in event_list:
        if(data['date'] in event['date']):
            if(len(events)==3):
                break
            events.append(event)
            date = datetime.strptime(date, '%Y-%m-%d')
            date += datetime.timedelta(days=1)
            date = date.strftime('%Y-%m-%d')
    return events

def next_event_by_sport(data):
    event_list = get_events()
    sport = data['sport']
    for event in event_list:
        if(sport in event['sport']):
            return event
    return None

def search_events_by_date(data):
    event_list = get_events()
    date = data['date']
    for event in event_list:
        if(date in event['date']):
            return event
    return None

def search_event_by_sport(data):
    event_list = get_events()
    sport = data['sport']
    for event in event_list:
        if(sport in event['sport']):
            return event
    return None

if __name__ == "__main__":
    search_event({'date':"2018-10-13"})