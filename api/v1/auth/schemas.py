from pydantic import BaseModel, EmailStr, Field


class UserSignUpSchema(BaseModel):
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    password: str = Field(..., min_length=8, description="User password")
    password_confirm: str = Field(
        ..., min_length=8, description="Password confirmation", exclude=True
    )

    # class Config:
    #     orm_mode = True

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserSignInSchema(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")
