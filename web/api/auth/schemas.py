from pydantic import BaseModel, EmailStr


class SignInSchema(BaseModel):
    email: EmailStr
    password: str
