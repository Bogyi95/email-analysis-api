from sqlalchemy import Column, Integer, String
from database import Base

class EmailRecord(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    body = Column(String)
    category = Column(String)
    priority = Column(String)
    summary = Column(String)