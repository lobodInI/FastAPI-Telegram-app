import uuid
import enum

from sqlalchemy import Column, String, ForeignKey, UUID, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(str, enum.Enum):
    Admin = "admin"
    Manager = "manager"
    User = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=UserRole.User)
    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    manager = relationship(
        "User",
        remote_side=[id],
        backref="subordinate"
    )
    requests = relationship(
        "Request",
        back_populates="owner",
    )


class Request(Base):
    __tablename__ = "requests"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    bot_token = Column(String(250), nullable=False)
    chat_id = Column(String(250), nullable=False)
    message = Column(String(550))
    response = Column(JSON)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship(
        "User",
        back_populates="requests",
    )
