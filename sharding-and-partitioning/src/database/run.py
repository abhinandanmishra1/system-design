import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

host=os.environ["host"]
username=os.environ["username"]
password=os.environ["password"]

# List of databases for horizontal partitioning
horizontal_databases = [
    "social_media_na",
    "social_media_eu",
    "social_media_asia",
    "social_media_other",
    "social_media_range_1",
    "social_media_range_2",
    "social_media_range_3",
    "social_media_hash_0",
    "social_media_hash_1",
    "social_media_hash_2",
    "social_media_hash_3"
]

# Queries for the primary database (social_media)
init_database_queries = [
    "DROP DATABASE IF EXISTS social_media;",
    "CREATE DATABASE social_media;",
    "USE social_media;",
    """
    CREATE TABLE users (
        user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(100),
        bio TEXT,
        region VARCHAR(50) NOT NULL,
        profile_picture_url VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_username (username),
        INDEX idx_email (email)
    );
    """,
    """
    CREATE TABLE posts (
        post_id BIGINT PRIMARY KEY AUTO_INCREMENT,
        user_id BIGINT NOT NULL,
        content TEXT,
        media_url VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        likes_count INT DEFAULT 0,
        comments_count INT DEFAULT 0,
        INDEX idx_user_id (user_id),
        INDEX idx_created_at (created_at)
        -- FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );
    """
]

# Queries for vertical partitioning
vertical_partitioning_queries = [
    "USE social_media;",
    """
    CREATE TABLE posts_core (
        post_id BIGINT PRIMARY KEY AUTO_INCREMENT,
        user_id BIGINT NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_user_id (user_id),
        INDEX idx_created_at (created_at)
    );
    """,
    """
    CREATE TABLE posts_media (
        post_id BIGINT PRIMARY KEY,
        media_url VARCHAR(255),
        media_type ENUM('image', 'video', 'audio'),
        media_size INT,
        FOREIGN KEY (post_id) REFERENCES posts_core(post_id)
    );
    """,
    """
    CREATE TABLE posts_metrics (
        post_id BIGINT PRIMARY KEY,
        likes_count INT DEFAULT 0,
        comments_count INT DEFAULT 0,
        shares_count INT DEFAULT 0,
        views_count INT DEFAULT 0,
        FOREIGN KEY (post_id) REFERENCES posts_core(post_id)
    );
    """
]

# Query for creating the posts table in horizontal partitions
create_horizontal_posts_table = """
CREATE TABLE IF NOT EXISTS posts (
    post_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    media_url VARCHAR(255),
    media_type VARCHAR(50),
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
"""

def execute_queries(cursor, queries):
    """Execute a list of SQL queries."""
    for query in queries:
        try:
            cursor.execute(query)
            print(f"Executed query: {query[:50]}...")
        except Error as e:
            print(f"Error executing query: {e}")

def create_horizontal_partitions(cursor):
    """Create horizontal partition databases and their posts table."""
    for db_name in horizontal_databases:
        try:
            # Create the database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database `{db_name}` created or already exists.")
            
            # Use the database
            cursor.execute(f"USE {db_name}")
            
            # Create the posts table
            cursor.execute(create_horizontal_posts_table)
            print(f"Table `posts` created in `{db_name}`.")
        except Error as e:
            print(f"Error occurred for database `{db_name}`: {e}")

def main():
    connection = None
    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host=host,  # Replace with your MySQL host
            user=username,  # Replace with your MySQL username
            password=password  # Replace with your MySQL password
        )
        
        if connection.is_connected():
            print("Connected to MySQL Server")
            cursor = connection.cursor()
            
            # Initialize the primary database and tables
            print("Initializing primary database and tables...")
            execute_queries(cursor, init_database_queries)
            
            # Create vertical partitions
            print("Creating vertical partitions...")
            execute_queries(cursor, vertical_partitioning_queries)
            
            # Create horizontal partitions and their posts tables
            print("Creating horizontal partitions...")
            create_horizontal_partitions(cursor)
            
            # Commit all changes
            connection.commit()
            print("All databases and tables created successfully.")
    
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
