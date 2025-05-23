from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import config
import pytz
from typing import List, Dict, Optional, Union
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URI)
            self.db = self.client[config.DATABASE_NAME]
            self.files_collection = self.db.files
            self.users_collection = self.db.users
            self.batch_collection = self.db.batches
            self.settings = self.db.settings
            self.messages_collection = self.db.messages
            self.admin_collection = self.db.admins
            
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

    async def add_user(self, user_id: int, username: str = None, first_name: str = None) -> bool:
        try:
            if not await self.users_collection.find_one({"user_id": user_id}):
                user_data = {
                    "user_id": user_id,
                    "username": username,
                    "first_name": first_name,
                    "join_date": datetime.now(pytz.UTC),
                    "total_files": 0,
                    "total_downloads": 0
                }
                await self.users_collection.insert_one(user_data)
                logger.info(f"New user added: {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding user: {str(e)}")
            return False

    async def get_all_users(self) -> List[Dict]:
        try:
            return await self.users_collection.find({}).to_list(None)
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []

    async def add_file(self, file_data: dict) -> str:
        try:
            file_data.update({
                "uuid": str(uuid.uuid4()),
                "upload_time": datetime.now(pytz.UTC),
                "downloads": 0,
                "last_accessed": datetime.now(pytz.UTC),
                "active_copies": []
            })
            await self.files_collection.insert_one(file_data)
            await self.users_collection.update_one(
                {"user_id": file_data["uploader_id"]},
                {"$inc": {"total_files": 1}}
            )
            logger.info(f"New file added: {file_data['uuid']}")
            return file_data["uuid"]
        except Exception as e:
            logger.error(f"Error adding file: {str(e)}")
            raise

    async def update_file_message_id(self, file_uuid: str, message_id: int, chat_id: int) -> bool:
        try:
            message_data = {
                "file_uuid": file_uuid,
                "message_id": message_id,
                "chat_id": chat_id,
                "created_at": datetime.now(pytz.UTC)
            }
            await self.messages_collection.insert_one(message_data)
            
            await self.files_collection.update_one(
                {"uuid": file_uuid},
                {
                    "$push": {"active_copies": {"chat_id": chat_id, "message_id": message_id}},
                    "$set": {"last_accessed": datetime.now(pytz.UTC)}
                }
            )
            logger.info(f"Added message copy for file {file_uuid}: {message_id} in chat {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating file message ID: {str(e)}")
            return False

    async def get_file(self, file_uuid: str) -> Optional[dict]:
        try:
            file_data = await self.files_collection.find_one({"uuid": file_uuid})
            if file_data:
                await self.files_collection.update_one(
                    {"uuid": file_uuid},
                    {"$set": {"last_accessed": datetime.now(pytz.UTC)}}
                )
            return file_data
        except Exception as e:
            logger.error(f"Error getting file: {str(e)}")
            return None

    async def delete_file(self, file_uuid: str) -> bool:
        try:
            file_data = await self.get_file(file_uuid)
            if file_data:
                result = await self.files_collection.delete_one({"uuid": file_uuid})
                if result.deleted_count > 0:
                    await self.users_collection.update_one(
                        {"user_id": file_data["uploader_id"]},
                        {"$inc": {"total_files": -1}}
                    )
                    await self.messages_collection.delete_many({"file_uuid": file_uuid})
                    logger.info(f"File deleted: {file_uuid}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False

    async def increment_downloads(self, file_uuid: str) -> int:
        try:
            result = await self.files_collection.find_one_and_update(
                {"uuid": file_uuid},
                {
                    "$inc": {"downloads": 1},
                    "$set": {"last_accessed": datetime.now(pytz.UTC)}
                },
                return_document=True
            )
            if result:
                await self.users_collection.update_one(
                    {"user_id": result["uploader_id"]},
                    {"$inc": {"total_downloads": 1}}
                )
                return result["downloads"]
            return 0
        except Exception as e:
            logger.error(f"Error incrementing downloads: {str(e)}")
            return 0

    async def add_batch(self, batch_data: dict) -> str:
        try:
            for file_uuid in batch_data["files"]:
                file_data = await self.get_file(file_uuid)
                if not file_data:
                    raise ValueError(f"File {file_uuid} not found")
                    
            batch_data.update({
                "uuid": str(uuid.uuid4()),
                "created_at": datetime.now(pytz.UTC),
                "downloads": 0,
                "last_accessed": datetime.now(pytz.UTC),
                "active_copies": []
            })
            await self.batch_collection.insert_one(batch_data)
            logger.info(f"New batch created: {batch_data['uuid']}")
            return batch_data["uuid"]
        except Exception as e:
            logger.error(f"Error creating batch: {str(e)}")
            raise

    async def get_batch(self, batch_uuid: str) -> Optional[dict]:
        try:
            batch_data = await self.batch_collection.find_one({"uuid": batch_uuid})
            if batch_data:
                valid_files = []
                for file_uuid in batch_data["files"]:
                    file_data = await self.get_file(file_uuid)
                    if file_data:
                        valid_files.append(file_uuid)
                
                if valid_files:
                    await self.batch_collection.update_one(
                        {"uuid": batch_uuid},
                        {"$set": {
                            "last_accessed": datetime.now(pytz.UTC),
                            "files": valid_files
                        }}
                    )
                    batch_data["files"] = valid_files
                    return batch_data
            return None
        except Exception as e:
            logger.error(f"Error getting batch: {str(e)}")
            return None

    async def delete_batch(self, batch_uuid: str) -> bool:
        try:
            result = await self.batch_collection.delete_one({"uuid": batch_uuid})
            success = result.deleted_count > 0
            if success:
                logger.info(f"Batch deleted: {batch_uuid}")
            return success
        except Exception as e:
            logger.error(f"Error deleting batch: {str(e)}")
            return False

    async def increment_batch_downloads(self, batch_uuid: str) -> int:
        try:
            result = await self.batch_collection.find_one_and_update(
                {"uuid": batch_uuid},
                {
                    "$inc": {"downloads": 1},
                    "$set": {"last_accessed": datetime.now(pytz.UTC)}
                },
                return_document=True
            )
            return result["downloads"] if result else 0
        except Exception as e:
            logger.error(f"Error incrementing batch downloads: {str(e)}")
            return 0

    async def get_setting(self, key: str, default=None):
        try:
            doc = await self.settings.find_one({"key": key})
            return doc["value"] if doc else default
        except Exception as e:
            logger.error(f"Error getting setting '{key}': {str(e)}")
            return default

    async def set_setting(self, key: str, value):
        try:
            await self.settings.update_one(
                {"key": key},
                {"$set": {"value": value}},
                upsert=True
            )
            logger.info(f"Setting '{key}' updated to: {value}")
        except Exception as e:
            logger.error(f"Error setting '{key}': {str(e)}")

    async def get_stats(self) -> dict:
        try:
            total_users = await self.users_collection.count_documents({})
            total_files = await self.files_collection.count_documents({})
            total_batches = await self.batch_collection.count_documents({})
            
            downloads_agg = await self.files_collection.aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$downloads"}}}
            ]).to_list(1)
            total_downloads = downloads_agg[0]["total"] if downloads_agg else 0
            
            batch_downloads_agg = await self.batch_collection.aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$downloads"}}}
            ]).to_list(1)
            total_batch_downloads = batch_downloads_agg[0]["total"] if batch_downloads_agg else 0
            
            active_files = await self.files_collection.count_documents({"active_copies": {"$ne": []}})
            
            return {
                "total_users": total_users,
                "total_files": total_files,
                "total_batches": total_batches,
                "total_downloads": total_downloads,
                "total_batch_downloads": total_batch_downloads,
                "active_files": active_files
            }
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {
                "total_users": 0,
                "total_files": 0,
                "total_batches": 0,
                "total_downloads": 0,
                "total_batch_downloads": 0,
                "active_files": 0
            }
