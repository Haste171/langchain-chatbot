from pymongo import MongoClient
import os

class MongoDBHandler:
    def __init__(self, database_name):
        self.client = MongoClient(os.environ.get('MONGO_URI'))
        self.db = self.client[database_name]

    def create_user_credentials(self, user_id, user_name, openai_api_key):
        credentials_collection = self.db['credentials']
        user_data = {
            'user_id': user_id,
            'user_name': user_name,
            'credentials': {
                'openai_api_key': openai_api_key
            }
        }
        credentials_collection.replace_one({'user_id': user_id}, user_data, upsert=True)

        
    def get_user_credentials(self, user_id):
        credentials_collection = self.db['credentials']
        user = credentials_collection.find_one({'user_id': user_id})
        if user:
            if 'credentials' in user:
                return {
                    'user_id': user['user_id'],
                    'user_name': user['user_name'],
                    'credentials': user['credentials']
                }
            else:
                return {
                    'user_id': user['user_id'],
                    'user_name': user['user_name'],
                    'credentials': None
                }
        else:
            return None

    def handle_data(self, user_id, user_name, space_name, space_id, ingest_url, ingested_time):
        user_collection = self.db['users']
        user = user_collection.find_one({'user_id': user_id})

        if not user:
            # Initialize the user section if it doesn't exist
            user_collection.insert_one({
                'user_id': user_id,
                'user_name': user_name,
                'data': []
            })

        # Add to the space array
        data = {
            'space': {
                'space_name': space_name,
                'space_id': space_id,
                'ingested_url': ingest_url,
                'ingested_time': ingested_time
            }
        }
        user_collection.update_one(
            {'user_id': user_id},
            {'$push': {'data': data}}
        )

    def list_spaces(self, user_id):
        user_collection = self.db['users']
        user = user_collection.find_one({'user_id': user_id})

        if user:
            spaces = []
            for entry in user['data']:
                space_data = {
                    'space_name': entry['space']['space_name'],
                    'space_id': entry['space']['space_id'],
                    'ingested_url': entry['space']['ingested_url'],
                    'ingested_time': entry['space']['ingested_time']
                }
                spaces.append(space_data)

            if spaces:
                return spaces
            else:
                return "You have no spaces"
        else:
            return "User not found"
        
    def delete_space(self, user_id, space_id):
        user_collection = self.db['users']
        result = user_collection.update_one(
            {'user_id': user_id, 'data.space.space_id': space_id},
            {'$pull': {'data': {'space.space_id': space_id}}}
        )

        if result.modified_count > 0:
            return True
        else:
            raise ValueError(f"Space with ID {space_id} not found.")

    def get_space_name(self, user_id, space_id):
        user_collection = self.db['users']
        user = user_collection.find_one({'user_id': user_id, 'data.space.space_id': space_id})

        if user:
            for entry in user['data']:
                if entry['space']['space_id'] == space_id:
                    return entry['space']['space_name']
            
            raise ValueError(f"Space with ID {space_id} not found.")
        else:
            raise ValueError("No user found with the provided space ID.")
        
    def check_ownership(self, user_id, space_id):
        user_collection = self.db['users']
        user = user_collection.find_one({'user_id': user_id, 'data.space.space_id': space_id})

        if user:
            for entry in user['data']:
                if entry['space']['space_id'] == space_id:
                    return True
            return False
        else:
            return False
