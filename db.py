import mysql.connector
import os

db_host = os.environ.get('db_host')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_password')
db_db = os.environ.get('db_db')

database = mysql.connector.connect(
    host = db_host, #Enter your host
    user = db_user, #Enter your user
    password = db_password, #Enter your password
    database = db_db #Enter your database name
)

async def get_data(db):
    for row in db:
        return row[0]