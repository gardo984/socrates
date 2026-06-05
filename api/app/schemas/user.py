from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    current_password: str | None = None
    new_password: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True