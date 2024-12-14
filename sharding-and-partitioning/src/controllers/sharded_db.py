import mysql.connector
from mysql.connector import Error
from enum import Enum
from typing import Dict, Any, Tuple, Optional
from ..utils import get_connection

class ShardingStrategy(Enum):
    GEOGRAPHIC = "GEOGRAPHIC"
    RANGE = "RANGE"
    HASH = "HASH"

class ShardedDB:
    def __init__(self):
        self.connections: Dict[str, mysql.connector.MySQLConnection] = {}
        self.init_connections()

    def init_connections(self):
        main_db = self._create_connection('social_media')
        self.connections['social_media'] = main_db
        # Initialize connections for geographic sharding
        geo_dbs = ['NA', 'EU', 'ASIA', 'OTHER']
        for region in geo_dbs:
            shard_id = f'geo_{region}'
            # region should be lowercased
            database_name = f'social_media_{region.lower()}'
            self.connections[shard_id] = self._create_connection(database_name)

        # Initialize connections for range-based sharding
        for i in range(1, 4):
            shard_id = f'range_{i}'
            database_name = f'social_media_range_{i}'
            self.connections[shard_id] = self._create_connection(database_name)

        # Initialize connections for hash-based sharding
        for i in range(4):
            shard_id = f'hash_{i}'
            database_name = f'social_media_hash_{i}'
            self.connections[shard_id] = self._create_connection(database_name)

    def _create_connection(self, database: str) -> mysql.connector.MySQLConnection:
        try:
            return get_connection(database)
        except Error as e:
            print(f"Error connecting to database {database}: {e}")
            raise

    def get_connection_by_strategy(
        self, 
        strategy: str, 
        user_id: int, 
        post_id: Optional[int] = None
    ) -> Tuple[mysql.connector.MySQLConnection, str]:
        if strategy == ShardingStrategy.GEOGRAPHIC.value:
            region = self._get_user_region(user_id)
            print("region", region)
            return self.connections[f'geo_{region}'], f'geo_{region}'
        
        elif strategy == ShardingStrategy.RANGE.value:
            shard_number = self._get_range_shard(post_id if post_id else user_id)
            return self.connections[f'range_{shard_number}'], f'range_{shard_number}'
        
        elif strategy == ShardingStrategy.HASH.value:
            shard_number = self._get_hash_shard(user_id)
            return self.connections[f'hash_{shard_number}'], f'hash_{shard_number}'
        
        raise ValueError(f"Invalid sharding strategy: {strategy}")

    def _get_user_region(self, user_id: int) -> str:
        # Mock implementation - in practice, you'd look up user's region from a user table
        region = self.connections['social_media'].cursor().execute("SELECT region FROM users WHERE user_id = %s", (user_id,))

        return region if region else 'NA'

    def _get_range_shard(self, id_value: int) -> int:
        if id_value <= 1000000:
            return 1
        elif id_value <= 2000000:
            return 2
        return 3

    def _get_hash_shard(self, user_id: int) -> int:
        return user_id % 4

    def create_post(self, strategy: str, user_id: int, content: str) -> Dict[str, Any]:
        conn, shard_id = self.get_connection_by_strategy(strategy, user_id)
        print("Connection established for user_id:", user_id)
        cursor = conn.cursor()
        
        try:
            query = """
            INSERT INTO posts (user_id, content)
            VALUES (%s, %s)
            """
            cursor.execute(query, (user_id, content))
            print("Post created successfully")
            post_id = cursor.lastrowid
            conn.commit()
            print("Post ID:", post_id)
            
            # Fetch the created post
            cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
            post = cursor.fetchone()
            
            response = {
                'post_id': post[0],
                'user_id': post[1],
                'content': post[2],
                'created_at': str(post[3]),
                'shard_id': shard_id
            }
            
            return response
        except Error as e:
            conn.rollback()
            raise Exception(f"Error creating post: {str(e)}")
        finally:
            cursor.close()

    def get_post(self, post_id: int, shard_id) -> Optional[Dict[str, Any]]:
        conn = self.connections[shard_id]
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return None
                
            return {
                'post_id': post[0],
                'user_id': post[1],
                'content': post[2],
                'created_at': str(post[3]),
                'shard_id': shard_id
            }
        finally:
            cursor.close()

    def close(self):
        for conn in self.connections.values():
            try:
                conn.close()
            except Error:
                pass