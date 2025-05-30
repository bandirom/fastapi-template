from pydantic import BaseModel, EmailStr, Field


class UserSignUpSchema(BaseModel):
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    password: str = Field(..., min_length=8, description="User password")
    password_confirm: str = Field(..., min_length=8, description="Password confirmation", exclude=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SignUpResponse(BaseModel):
    id: int
