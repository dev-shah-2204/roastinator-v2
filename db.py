import os
import psycopg2 as sql

from dotenv import load_dotenv

load_dotenv()

url = os.getenv('DATABASE_URL')

database = sql.connect(url)
db = database.cursor()
