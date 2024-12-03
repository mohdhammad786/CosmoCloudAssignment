from fastapi import APIRouter, Depends,HTTPException
from models.students.create_student_request_body import Student
from services.studentService import StudentService
from models.students.create_student_response_body import CreateStudentResponseBody
from exceptions.recordNotFoundException import RecordNotFoundException
from fastapi.responses import JSONResponse,Response
from models.students.update_student_request_body import StudentUpdate
from models.students.getStudentListReponse import GetStudentListResponse
from typing import Optional
router = APIRouter()
class StudentController:
    def __init__(self,service:StudentService):
        self.service = service
    @router.post("/students")
    async def createStudent(student:Student,service:StudentService = Depends(StudentService)) -> JSONResponse:
        try:
            student_id = await service.createStudent(student=student)
            reponse = CreateStudentResponseBody(id=student_id)
            return JSONResponse(status_code=201,content=reponse.model_dump())
        except Exception as e:
            raise HTTPException(status_code=500,detail="something went wrong")
    @router.delete("/students/{id}")
    async def deleteStudentById(id:str,service:StudentService = Depends(StudentService))->JSONResponse :
        try: 
            await service.deleteStudent(id=id)
            return JSONResponse(status_code=200,content={})
        except RecordNotFoundException as e :
            raise e
        except Exception as e:
            raise e
    @router.get("/students/{id}")
    async def fetchStudent(id:str,service:StudentService = Depends(StudentService)) -> JSONResponse:
        try: 
            student = await service.fetchStudent(id=id)
            return JSONResponse(status_code=200,content= student.model_dump())
        except RecordNotFoundException as e :
            raise e
        except Exception as e:
            raise e
    @router.patch("/students/{id}")
    async def patchUpdateStudent(id:str,studentUpdate:StudentUpdate,service:StudentService = Depends(StudentService)) -> JSONResponse:
        try: 
            await service.patchUpdateStudent(id,studentUpdate=studentUpdate)
            return Response(status_code=204)
        except RecordNotFoundException as e :
            raise e
        except Exception as e:
            raise e
    @router.get("/students")
    async def getStudentsList(country:Optional[str] = None,age:Optional[int] = None,service:StudentService = Depends(StudentService)):
        try: 
            studentList = await service.getStudentsList(county=country,age=age)
            response = GetStudentListResponse(data = studentList)
            return JSONResponse(status_code=200,content= response.model_dump())
        except Exception as e:
            raise e
