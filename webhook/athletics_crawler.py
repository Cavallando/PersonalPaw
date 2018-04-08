
from icalendar import Calendar
import urllib
import datetime
#def get_calendar(): 

def search_event(data):
    data = open('files/events.ics','rb')
    cal = Calendar.from_ical(data.read())
    for component in cal.walk():
        if component.name == "VEVENT":
            print(component.get('summary'))
            print(component.get('dtstart').dt)
    data.close()

if __name__ == "__main__":
    search_event("M BBALL")