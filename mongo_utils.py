import pymongo
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection details - use existing environment variable
MONGO_URI = os.getenv("mongo_uri")  # Match the lowercase in your .env file
DB_NAME = "ai_agent_sales"  # Database name
COLLECTION_NAME = "user_sessions"  # Collection name

class MongoManager:
    """Manages MongoDB operations for the application."""
    
    def __init__(self):
        """Initialize the MongoDB connection."""
        try:
            # Connect to MongoDB using the URI from .env
            self.client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            # Check the connection
            self.client.server_info()
            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            self.connected = True
            print(f"Connected to MongoDB: {DB_NAME}.{COLLECTION_NAME}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.connected = False
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
    
    def save_session(self, session_data):
        """Save session data to MongoDB."""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")
        
        try:
            # Add timestamp if not present
            if "updated_at" not in session_data:
                session_data["updated_at"] = datetime.now()
            
            # Check if document already exists with this session_id
            existing = self.collection.find_one({"session_id": session_data["session_id"]})
            
            if existing:
                # Update existing document
                result = self.collection.update_one(
                    {"session_id": session_data["session_id"]},
                    {"$set": session_data}
                )
                success = result.modified_count > 0 or result.matched_count > 0
            else:
                # Insert new document
                result = self.collection.insert_one(session_data)
                success = result.inserted_id is not None
                
            if success:
                print(f"Successfully saved session {session_data['session_id']} to MongoDB")
            else:
                print(f"Warning: MongoDB operation completed but may not have modified data for session {session_data['session_id']}")
                
            return success
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")
            raise e
    
    def get_session(self, session_id):
        """Retrieve session data by session_id."""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")
        
        try:
            return self.collection.find_one({"session_id": session_id}, {'_id': 0})
        except Exception as e:
            print(f"Error retrieving session from MongoDB: {e}")
            raise e 