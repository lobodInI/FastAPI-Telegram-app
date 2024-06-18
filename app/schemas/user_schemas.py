from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.db.models.models import UserRole


class BaseUser(BaseModel):
    id: UUID
    username: str
    role: UserRole


class SignInUser(BaseModel):
    email: str
    password: str


class SignUpUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.User
    manager_id: UUID = None


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None


class UsersList(BaseUser):
    pass


class UserDetail(BaseUser):
    email: EmailStr
