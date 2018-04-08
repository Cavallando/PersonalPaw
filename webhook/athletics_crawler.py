
from icalendar import Calendar
import urllib
import datetime
import re
#def get_calendar(): 

def search_event(data):
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
            if(data.get('sport') is None):
                if(data.get('date') in dtstart):
                    eventList.append({'sport': sport, 'description':description, 'date':dtstart,'location':location})
            elif(data.get('sport') in summary):
                eventList.append({'sport': sport.encode('utf-8'), 'description':description, 'date':dtstart,'location':location})
        #if eventList:
        #    break
        #else:
        #    date = datetime.strptime(data['date'], fmt)
        #    date += datetime.timedelta(days=1)
        #    data['date'] = date.strftime(fmt)
        return eventList
    ics.close()

if __name__ == "__main__":
    search_event({'date':"2018-10-13"})