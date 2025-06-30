# models/configuration.py
from sqlalchemy import Column, BigInteger, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(BigInteger, primary_key=True, index=True)
    user_search_columns = Column(JSON)  # stores column names like ["name", "email", "position"]
    org_id = Column(BigInteger, ForeignKey("organizations.id"), unique=True)

    organization = relationship("Organization", back_populates="configuration")
