from fastapi.responses import JSONResponse
from pydantic import BaseModel


class CustomResponse(BaseModel):
    success: bool
    message: str
    data: dict = None


def response(success: bool = True, message: str = 'success', data: dict = {}, status_code: int = 200):
    if data is None:
        data = {}
    response_data = CustomResponse(success=success, message=message, data=data)
    return JSONResponse(content=response_data.dict(), status_code=status_code)
