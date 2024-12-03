from fastapi import HTTPException

class RecordNotFoundException(HTTPException):
    def __init__(self, record_id: str, detail: str = "Record not found"):
        super().__init__(status_code=404, detail=f"{detail}: {record_id}")