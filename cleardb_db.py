"""
Credentials for database
"""
import os
import mysql.connector

db_host = os.environ.get('db_host') #Enter your host
db_user = os.environ.get('db_user') #Enter your user
db_password = os.environ.get('db_password') #Enter your password
db_db = os.environ.get('db_db') #Enter your database name

database = mysql.connector.connect(
    host = db_host,
    user = db_user,
    password = db_password,
    database = db_db
)
