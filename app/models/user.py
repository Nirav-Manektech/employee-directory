# models/user.py
from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(255), index=True)
    position = Column(String(255), index=True)
    department_id = Column(BigInteger, ForeignKey("departments.id"), index=True)
    created_at = Column(DateTime, default=func.now(), index=True)

    department = relationship("Department", back_populates="users")
    user_orgs = relationship("UserOrg", back_populates="user")

    __table_args__ = (
        Index("ix_users_org_department", "department_id"),
    )