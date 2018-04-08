import re
import requests
import json
#from db.menu_models import *


def search_building(buildingName):
    buildingName = buildingName.replace(" ","%20")
    fis_search_url = ("https://apps.opp.psu.edu/fis-api/v1/buildings?campus.id=UP&name:ilike=*"+buildingName+"*")
    r = requests.get((fis_search_url))
    data = json.loads(r.text)
    city = data[0]['city'].encode('utf-8')
    address = data[0]['address'].encode('utf-8')
    zipCode = data[0]['zipCode'].encode('utf-8')
    longitude = data[0]['latLong']['longitude'].encode('utf-8')
    longitude = data[0]['latLong']['latitude'].encode('utf-8')
    print(data[0]['city'].encode('utf-8'))


def search_program(program):
    pass

if __name__ == "__main__":
    search_building("Old Main")
    # search_program("philosophy")