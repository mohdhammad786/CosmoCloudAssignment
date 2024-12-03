from typing import List, Optional
from bson import ObjectId
from fastapi import Depends
from database.mongo_db_connection import MongoDBManager
from models.students.create_student_request_body import Student
from exceptions.recordNotFoundException import RecordNotFoundException
from models.students.update_student_request_body import StudentUpdate
from models.students.getStudentListReponse import Student as LStudent

class StudentsRepo:
    def __init__(self,db:MongoDBManager):
        self.mongoDbWrapper:MongoDBManager = db
    
    async def createStudent(self,student:Student) ->str:
        insertedId = await self.mongoDbWrapper.insertInCollection("student",student.model_dump())
        return str(insertedId )
    
    async def deleteStudentById(self,id:str):
        result = await self.mongoDbWrapper.deleteInCollection("student",id)
        return result
    
    async def fetchStudentById(self,id:str) -> Student:
        document = await self.mongoDbWrapper.fetchRecordInCollection("student",id=id)
        if document is None :
            raise RecordNotFoundException(record_id=id)
        document.pop("_id", None)
        return Student.model_validate(document)
    
    async def patchUpdateStudentById(self,id:str,update_student:StudentUpdate):
        try:
            student:Student = await self.fetchStudentById(id=id)
            if(update_student.name is not None):
                student.name = update_student.name
            if(update_student.age is not None):
                student.age = update_student.age
            if(update_student.address is not None and update_student.address.city is not None):
                student.address.city = update_student.address.city
            if(update_student.address is not None and update_student.address.country is not None):
                student.address.country = update_student.address.country
        except RecordNotFoundException as e:
            raise e
        except Exception as e:
            raise e
        result = await self.mongoDbWrapper.updateRecordInCollection(collectionName="student",query={"_id": ObjectId(id)}, update={"$set":student.model_dump(exclude_unset=True) })
        if result.modified_count == 0:
            raise RecordNotFoundException(record_id=id)
        
    async def getStudentList(self,country:Optional[str],age:Optional[int]) ->List[LStudent]:
        query = {}
        if country is not None:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age}
        result = await self.mongoDbWrapper.fetchRecordsInCollection(collectionName="student",query=query)
        studentList:List = []
        for document in result:
            document.pop("_id",None)
            document.pop("address",None)
            studentList.append(LStudent.model_validate(document))
        return studentList

        


def getStudentRepo(db:MongoDBManager = Depends(MongoDBManager)) -> MongoDBManager:
    return StudentsRepo(db=db)