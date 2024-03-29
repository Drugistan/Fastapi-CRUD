from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    password: str
