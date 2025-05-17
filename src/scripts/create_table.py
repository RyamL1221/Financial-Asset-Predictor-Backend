import pymysql
from src.db import get_connection

def main():
    # Get a connection to the database
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Create a new table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id   SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                email     VARCHAR(100)    UNIQUE NOT NULL,
                password  VARCHAR(30)     NOT NULL,
                first_name VARCHAR(50)    NOT NULL,
                last_name    VARCHAR(50)    NOT NULL
            )
        """)
        print("Table 'users' created successfully.")
    except pymysql.MySQLError as e:
        print(f"Error creating table: {e}")
    finally:
        connection.close()
    
if __name__ == "__main__":
    main()