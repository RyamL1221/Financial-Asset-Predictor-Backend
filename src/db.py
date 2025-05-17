import pymysql
from dotenv import load_dotenv
import os

def get_connection():
    """
    Returns a connection to the MySQL database.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Set the timeout for the connection
    timeout = 10

    # Get the database connection parameters from environment variables
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
    MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")

    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db = MYSQL_DATABASE,
        host=MYSQL_HOST,
        password=MYSQL_PASSWORD,
        read_timeout=timeout,
        port=MYSQL_PORT,
        user=MYSQL_USERNAME,
        write_timeout=timeout,
    )

    return connection

