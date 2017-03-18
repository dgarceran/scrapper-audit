import pymysql
from main.config import *

# Connect to the database
connection = pymysql.connect(host = DB_HOST,
                             user = DB_USER,
                             password = DB_PASS,
                             db = DB_TABLE,
                             charset = 'utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)