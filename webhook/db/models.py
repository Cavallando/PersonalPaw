import sqlite3 as sql

def insert_menu(date,location,menu,food):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO menus (menu_date,dining_commons,menu,food_items) VALUES (?,?,?,?)", (date,location,menu,food))
    con.commit()
    con.close()

def lookup(location):
    
def select_menu(date,location,menu):
    con = sql.connect("database.db")
    cur = con.cursor()
    string = "SELECT food_items FROM menus WHERE menu_date='"+date+"' AND dining_commons='"+location+"' AND menu='"+menu+"';"
    result = cur.execute(string)
    con.close()
    return result.fetchall()

def update_menu(date, location, menu, food_items):
    con = sql.connect("database.db")
    cur = con.cursor()
    string = "UPDATE menus SET food_items='"+food_items+"' WHERE menu_date='"+date+"' AND dining_commons='"+location+"' AND menu='"+menu+"';"
    result = cur.execute(string)
    con.close()
