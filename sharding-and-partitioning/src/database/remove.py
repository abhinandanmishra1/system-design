import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

host=os.environ["host"]
username=os.environ["username"]
password=os.environ["password"]
port = os.environ["port"]

def delete_databases(cursor, database_names=None, pattern=None):
    """
    Deletes databases based on a list of names or a pattern.
    
    Args:
        cursor: MySQL cursor object.
        database_names (list): List of database names to delete.
        pattern (str): Pattern to match database names (e.g., 'social_media_%').
    """
    try:
        # If a pattern is provided, fetch databases matching the pattern
        if pattern:
            cursor.execute(f"SHOW DATABASES LIKE '{pattern}'")
            database_names = [row[0] for row in cursor.fetchall()]
        
        if not database_names:
            print("No databases to delete.")
            return
        
        # Drop each database in the list
        for db_name in database_names:
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            print(f"Database `{db_name}` deleted.")
    
    except Error as e:
        print(f"Error deleting databases: {e}")

def main():
    connection = None
    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host=host,  
            user=username,  
            password=password,
            port=port
        )

        if connection.is_connected():
            print("Connected to MySQL Server")
            cursor = connection.cursor()
            
            # Delete databases based on a pattern
            print("Deleting databases...")
            delete_databases(cursor, pattern="social_media")
            
            # Commit changes
            connection.commit()
            print("Databases deleted successfully.")
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        # Close the connection
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    main()