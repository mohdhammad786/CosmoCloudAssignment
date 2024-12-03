from typing import Union
from fastapi import Depends, FastAPI
from controllers.student_controller import router as studentRouter
import uvicorn
app = FastAPI()
app.include_router(studentRouter)
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000,  #
        log_level="info",  
        reload=False,
    )

