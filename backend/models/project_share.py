from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class SharePermission(str, enum.Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

class ProjectShare(Base):
    __tablename__ = "project_shares"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    permission = Column(Enum(SharePermission), default=SharePermission.READ)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="shares")
    user = relationship("User", back_populates="shared_projects") 