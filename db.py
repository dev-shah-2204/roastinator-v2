import os
import psycopg2 as sql

url = os.getenv('DATABASE_URL')

database = sql.connect(url)
db = database.cursor()
