import mysql.connector
from datetime import datetime
from ..utils import get_connection

class SocialMediaDB:
    def __init__(self):
        self.conn = get_connection("social_media")
        self.cursor = self.conn.cursor()

    def create_user(self, username, email, password_hash, region, full_name=None, bio=None, profile_picture_url=None):
        query = """
        INSERT INTO users (username, email, password_hash, region, full_name, bio, profile_picture_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (username, email, password_hash, region, full_name, bio, profile_picture_url))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_user(self, user_id):
        query = """
        SELECT * FROM users
        WHERE user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def get_all_users(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def create_post(self, user_id, content, media_url=None):
        query = """
        INSERT INTO posts (user_id, content, media_url)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (user_id, content, media_url))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_post(self, post_id):
        query = "SELECT * FROM posts WHERE post_id = %s"
        self.cursor.execute(query, (post_id,))
        return self.cursor.fetchone()

    def get_user_posts(self, user_id):
        query = "SELECT * FROM posts WHERE user_id = %s ORDER BY created_at DESC"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

