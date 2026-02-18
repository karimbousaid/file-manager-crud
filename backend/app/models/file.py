from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..database import Base

class FileModel(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    owner_username = Column(String, nullable=False)