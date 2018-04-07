import os

import MySQLdb


# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db

def insert_menu(date,location,menu,food):
    con = connect_to_cloudsql()
    cur = con.cursor()
    cur.execute("INSERT INTO menus (menu_date,dining_commons,menu,food_items) VALUES (?,?,?,?)", (date,location,menu,food))
    con.commit()
    con.close()


def select_menu(date,location,menu):
    con = connect_to_cloudsql()
    cur = con.cursor()
    string = "SELECT food_items FROM menus WHERE menu_date='"+date+"' AND dining_commons='"+location+"' AND menu='"+menu+"';"
    result = cur.execute(string)
    con.close()
    return result.fetchall()

def update_menu(date, location, menu, food_items):
    con = connect_to_cloudsql()
    cur = con.cursor()
    string = "UPDATE menus SET food_items=? WHERE menu_date=? AND dining_commons=? AND menu=?;"
    vals = [food_items, date, location, menu]
    result = cur.execute(string, vals)
    if(cur.rowcount == 0):
        con.close()
        insert_menu(date, location, menu, food_items)
    con.close()
