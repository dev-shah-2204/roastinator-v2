import mysql.connector
import os 

host = os.getenv('db_host')
user = os.getenv('db_user')
passw = os.getenv('db_password')
name = os.getenv('db_db')

database = mysql.connector.connect(
    host = host,
    user = user,
    password = passw,
    database = name
)
db = database.cursor()
