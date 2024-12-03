from typing import List, Optional
from repositories.students_repo import StudentsRepo,getStudentRepo
from models.students.create_student_request_body import Student
from models.students.create_student_response_body import CreateStudentResponseBody
from fastapi import Depends, HTTPException
from exceptions.recordNotFoundException import RecordNotFoundException
from models.students.update_student_request_body import StudentUpdate
from models.students.getStudentListReponse import Student as LStudent


class StudentService:
    _instance = None
    def __new__(cls, studentsRepo: StudentsRepo = Depends(getStudentRepo)):
        if cls._instance is None:
            cls._instance = super(StudentService, cls).__new__(cls)
            cls._instance.studentsRepo = studentsRepo
        return cls._instance
    def __init__(self, studentsRepo: StudentsRepo):
        if not hasattr(self, "studentsRepo"):  
            self.studentsRepo = studentsRepo

    async def createStudent(self, student: Student) -> str:
        try:
            student_id = await self.studentsRepo.createStudent(student=student)
            return student_id
        except Exception as e:
            raise HTTPException(status_code=500, detail="Something went wrong")
    async def deleteStudent(self,id:str):
        try:
            deleteStudentResult = await self.studentsRepo.deleteStudentById(id)
            if deleteStudentResult.deleted_count == 0:
                raise  RecordNotFoundException(record_id=id)
        except RecordNotFoundException:
            raise
        except Exception as e:
            raise e 
    async def fetchStudent(self,id:str) -> Student:
        try:
            student  = await self.studentsRepo.fetchStudentById(id)
            return student
        except RecordNotFoundException:
            raise
        except Exception as e:
            raise e 
    async def patchUpdateStudent(self,id:str,studentUpdate:StudentUpdate):
        try:
            await self.studentsRepo.patchUpdateStudentById(id= id, update_student=studentUpdate)
        except RecordNotFoundException:
            raise
        except Exception as e:
            raise e 
    async def getStudentsList(self,county:Optional[str],age:Optional[int])-> List[LStudent]:
        try:
            studentList = await self.studentsRepo.getStudentList(country=county,age=age)
            return studentList
        except Exception as e:
            raise e 


