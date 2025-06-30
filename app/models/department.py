# models/department.py
from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255))
    org_id = Column(BigInteger, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="departments")
    users = relationship("User", back_populates="department")
