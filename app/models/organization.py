# models/organization.py
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from app.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(BigInteger, primary_key=True, index=True)
    org_name = Column(String(255))

    user_orgs = relationship("UserOrg", back_populates="organization")
    departments = relationship("Department", back_populates="organization")
    configuration = relationship("Configuration", back_populates="organization", uselist=False)
