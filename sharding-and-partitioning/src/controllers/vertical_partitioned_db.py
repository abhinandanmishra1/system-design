import mysql.connector
from ..utils import get_connection

class VerticalPartitionedDB:
    def __init__(self):
        self.conn = get_connection("social_media")
        self.cursor = self.conn.cursor()

    def create_post(self, user_id, content, media_url=None):
        try:
            # Start transaction
            self.conn.start_transaction()

            # Insert core post data
            core_query = """
            INSERT INTO posts_core (user_id, content)
            VALUES (%s, %s)
            """
            self.cursor.execute(core_query, (user_id, content))
            post_id = self.cursor.lastrowid

            # Insert media data if provided
            if media_url:
                media_query = """
                INSERT INTO posts_media (post_id, media_url)
                VALUES (%s, %s, %s)
                """
                self.cursor.execute(media_query, (post_id, media_url))

            # Initialize metrics
            metrics_query = """
            INSERT INTO posts_metrics (post_id)
            VALUES (%s)
            """
            self.cursor.execute(metrics_query, (post_id,))

            # Commit transaction
            self.conn.commit()
            return post_id

        except Exception as e:
            self.conn.rollback()
            raise e

    def get_post_complete(self, post_id):
        query = """
        SELECT c.*, m.media_url, m.media_type, mt.likes_count, mt.comments_count, mt.shares_count, mt.views_count
        FROM posts_core c
        LEFT JOIN posts_media m ON c.post_id = m.post_id
        LEFT JOIN posts_metrics mt ON c.post_id = mt.post_id
        WHERE c.post_id = %s
        """
        self.cursor.execute(query, (post_id,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

