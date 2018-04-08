import sqlite3 as sql
from db import DB_NAME

def insert_menu(date,location,menu,food):
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT INTO menus (menu_date,dining_commons,menu,food_items) VALUES (?,?,?,?)", (date,location,menu,food))
    con.commit()
    con.close()

def select_menu(date,location,menu):
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    string = "SELECT food_items FROM menus WHERE menu_date=? AND dining_commons=? AND menu=?;"
    paramList = [date,location,menu]
    result = cur.execute(string, paramList)
    fetched = result.fetchone()[0]
    con.close()
    return fetched

def update_menu(date, location, menu, food):
    con = sql.connect(DB_NAME)
    cur = con.cursor()
    string = "UPDATE menus SET food_items=? WHERE menu_date=? AND dining_commons=? AND menu=?;"
    paramList = [food, date,location,menu]
    result = cur.execute(string, paramList)
    if(cur.rowcount==0):
        con.close()
        insert_menu(date,location,menu,food_items)
    con.close()