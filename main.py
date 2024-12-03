from fastapi import FastAPI
from controllers.student_controller import router as studentRouter
import uvicorn

app = FastAPI()

# Include the student router
app.include_router(studentRouter)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",  # Change from "127.0.0.1" to "0.0.0.0"
        port=8000,  
        log_level="info",  
        reload=False,
    )
