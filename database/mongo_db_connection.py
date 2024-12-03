from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from urllib.parse import quote_plus
from bson import ObjectId
import os
from pymongo.results import UpdateResult

class MongoDBManager:
    def __init__(self):
        load_dotenv()
        username = os.getenv("MONGO_USER") 
        password = os.getenv("MONGO_PASSWORD")
        username = quote_plus(username)
        password = quote_plus(password)
        self.mongo_url = f"mongodb+srv://{username}:{password}@cosmocloudcluster.4ttfw.mongodb.net/?retryWrites=true&w=majority&appName=cosmoCloudCluster"
        self.client = None
        self.db = None
        self.connect("cosmoCloudAssignment")

    def connect(self, database_name: str):
        if not self.client:
            self.client = AsyncIOMotorClient(self.mongo_url)
            self.db = self.client.get_database("cosmoCloudAssignment")
        return self.db
    async def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
    async def insertInCollection(self,collectionName:str,dataEntry:dict) ->str:
        result = await self.db[collectionName].insert_one(dataEntry)
        return result.inserted_id
    async def deleteInCollection(self,collectionName:str,id:str):
        objectid = ObjectId(id)
        delete_result = await self.db[collectionName].delete_one({"_id": objectid})
        return delete_result
    async def fetchRecordInCollection(self,collectionName:str,id:str):
        objectid = ObjectId(id)
        document = await self.db[collectionName].find_one({"_id":objectid})
        return document
    async def updateRecordInCollection(self,collectionName:str,query:dict,update:dict)-> UpdateResult:
        result = await self.db[collectionName].update_one(query,update)
        return result
    async def fetchRecordsInCollection(self,collectionName:str,query:dict) -> any:
        cursor = self.db[collectionName].find(query)
        result = []
        async for document in cursor:
            result.append(document)
        return result



