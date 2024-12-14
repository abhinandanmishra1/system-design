import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

def get_connection(db_name = None):
    return mysql.connector.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        user=os.getenv("username"),
        password=os.getenv("password"),
        database=db_name,
    )
