from core.database import Base
from sqlalchemy import Boolean, Column, Integer, String,Text, DateTime, func


class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text,default="")
    is_completed = Column(Boolean,default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, is_done={self.is_done!r})"