import psycopg2
import mysql.connector
from dotenv import load_dotenv
import os
import logging


load_dotenv('./setup/.env')
logger = logging.getLogger(__name__)

def connect_postgressql():
    # connection for postgressSQL
    try:
        return psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host="localhost",  # Use static value
            port="5432"       # Use static value
        )
    except Exception as e:
        logger.exception("An exception occurred: %s", str(e))

def connect_mysql():
    # connection for mySQL
    try:
        return mysql.connector.connect(
            database=os.environ.get("MYSQL_DATABASE"),  # Use database instead of dbname
            user=os.environ.get("MYSQL_user"),
            password=os.environ.get("MYSQL_ROOT_PASSWORD"),
            # Uncomment below if you have MYSQL_HOST and MYSQL_PORT as env variables
            host="localhost",  # Use static value
            port="3306"       # Use static value
        )
    except Exception as e:
        logger.exception("An exception occurred: %s", str(e))
