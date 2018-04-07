import urllib2
from bs4 import BeautifulSoup
from db.models import *
import re

def parse_month(datetext) {
    dateStrip = datetext.replace("\r\n","").strip().encode("utf-8")
    day = re.search("\s\d{1,2}", dateStrip).group().strip()
    month = find_month(str(dateStrip.split()[1]))
    return date(day=int(day), month=month, year=int(dateStrip[-4:])).strftime('%Y-%m-%d')
}    

def find_month(self,strMonth):
    if(strMonth == 'January'):
        return 1
    elif(strMonth == 'February'):
        return 2
    elif(strMonth == 'March'):
        return 3
    elif(strMonth == 'April'):
        return 4
    elif(strMonth == 'May'):
        return 5
    elif(strMonth == 'June'):
        return 6
    elif(strMonth == 'July'):
        return 7
    elif(strMonth == 'August'):
        return 8
    elif(strMonth == 'September'):
        return 9
    elif(strMonth == 'October'):
        return 10
    elif(strMonth == 'November'):
        return 11
    elif(strMonth == 'December'):
        return 12
        

def scrape_menus():
    urls = [
        "http://menu.hfs.psu.edu/shortmenu.aspx?sName=Penn+State+Housing+and+Food+Services&locationNum=11&locationName=East+Food+District&naFlag=1",
        "http://menu.hfs.psu.edu/shortmenu.aspx?sName=Penn+State+Housing+and+Food+Services&locationNum=14&locationName=Pollock+Dining+Commons+&naFlag=1",
        "http://menu.hfs.psu.edu/shortmenu.aspx?sName=Penn+State+Housing+and+Food+Services&locationNum=13&locationName=South+Food+District&naFlag=1",
        "http://menu.hfs.psu.edu/shortmenu.aspx?sName=Penn+State+Housing+and+Food+Services&locationNum=16&locationName=West+Food+District&naFlag=1",
        "http://menu.hfs.psu.edu/shortmenu.aspx?sName=Penn+State+Housing+and+Food+Services&locationNum=17&locationName=North+Food+District&naFlag=1"
    ]
    for i in range(0, len(urls)):
        page = urllib2.urlopen(urls[i])
        soup = BeautifulSoup(page, 'html.parser')
        span = soup.find_all('span', class_='datelinks')
        for datelinks in span.find_all('a', attrs = {'href'}):
            page = urllib2.urlopen(datelinks.get_text())
            # parse the html using beautiful soup and store in variable `soup`
            soup = BeautifulSoup(page, 'html.parser')
            location = soup.find('h1').get_text()
            date = parse_month(soup.find('h4'),get_text())
            for col in soup.find_all('td', class_='colMenu'):
                for meal_time in col.find_all('td',class_='meal-header'):
                    meal = meal_time.get_text()
                    meal = meal.replace(" ","").encode("utf-8")
                    meal = meal.replace("\r\n","")
                    menuStr = ' '
                    if("Breakfast" in meal):
                        menuStr = 'breakfast'
                    elif("Lunch" in meal):
                        menuStr = 'lunch'
                    elif("Dinner" in meal):
                        menuStr = 'dinner'
                    elif("4th Meal" in meal):
                        menuStr = '4th meal'
                    if(menuStr != ' '):
                        items =  col.find_all('div', class_='shortmenurecipes')
                        food_items =""
                        for item in items: 
                            food_items += item.get_text() +","
                    



scrape_menus()