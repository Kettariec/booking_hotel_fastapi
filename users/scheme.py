from pydantic import BaseModel, EmailStr


class SchemeUserAuth(BaseModel):
    email: EmailStr
    password: str
