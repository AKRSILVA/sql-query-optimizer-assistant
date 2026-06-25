import os

import psycopg

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

os.environ["PGCLIENTENCODING"] = "UTF8"


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
