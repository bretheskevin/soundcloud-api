from pydantic import BaseModel

class CheckTokenResponse(BaseModel):
    is_valid: bool
