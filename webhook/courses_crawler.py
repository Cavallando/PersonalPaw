import re

from bs4 import BeautifulSoup
import requests

#from db.menu_models import *

course_search_url = "http://undergraduate.bulletins.psu.edu/search/?scontext=courses&search="
program_search_url = "http://undergraduate.bulletins.psu.edu/search/?scontext=programs&search="

course_search_data = []
program_search_data = []

def search_course(course):
    r = requests.get(course_search_url + course)
    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    search_results = soup.find_all("div", class_="searchresult")
    
    for result in search_results:
        class_name = result.find("h2").get_text()
        return class_name

def search_program(program):
    pass

if __name__ == "__main__":
    search_course("philosophy")
    # search_program("philosophy")