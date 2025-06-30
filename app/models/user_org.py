# models/user_org.py
from sqlalchemy import Column, BigInteger, ForeignKey,Integer
from sqlalchemy.orm import relationship
from app.database import Base


class UserOrg(Base):
    __tablename__ = "user_orgs"

    id = Column(BigInteger, primary_key=True, index=True)
    org_id = Column(BigInteger, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="user_orgs")
    organization = relationship("Organization", back_populates="user_orgs")
