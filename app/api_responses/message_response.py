from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str

class ApiResponse(BaseModel):
    success: bool
    message: str
