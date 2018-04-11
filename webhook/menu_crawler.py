import requests
from bs4 import BeautifulSoup
import re
from datetime import date

import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
def getLocationNumber(location):
    if(location=="Pollock Dining Commons"):
        return 14
    elif(location=="East Food District"):
        return 11
    elif(location=="South Food District"):
        return 13
    elif(location=="West Food District"):
        return 16
    elif(location=="North Food District"):
        return 17
    return 0

def scrape_menus(data):
    locURL = data["dining_commons"].replace(" ","+")
    locNum = getLocationNumber(data["dining_commons"])
    dayStr = data["date"][8:10]
    monthStr = data["date"][5:7]
    if(dayStr[0:1]=="0"):
        dayStr=dayStr[1:2]
    if(monthStr[0:1]=="0"):
        monthStr=monthStr[1:2]
    dateURL = "&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate="+monthStr+"%2f"+dayStr+"%2f"+data["date"][0:4]
    url = "http://menu.hfs.psu.edu/shortmenu.aspx?sName=Penn+State+Housing+and+Food+Services&locationNum="+str(locNum)+"&locationName=+"+locURL+"&naFlag=1"+dateURL
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    for col in soup.find_all('td', class_='colMenu'):
        for meal_time in col.find_all('td',class_='meal-header'):
            meal = meal_time.get_text()
            meal = meal.replace(" ","").encode("utf-8")
            meal = meal.replace("\r\n","")
            isMenu = False
            if(data["menu"] in meal):
                isMenu = True
            else:
                isMenu = False
            if(isMenu):
                items =  col.find_all('div', class_='shortmenurecipes')
                food_items =""
                for item in items: 
                    food = item.get_text().strip()
                    food_items += food +", "
                return food_items

scrape_menus({"dining_commons":"Pollock Dining Commons","date":"2018-04-09","menu":"Breakfast"})