from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    project_type = Column(String, default="web")
    model = Column(String)  # Store which model was used
    structure = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    files = relationship("ProjectFile", back_populates="project")
    owner = relationship("User", back_populates="projects")
    shares = relationship("ProjectShare", back_populates="project")
    comments = relationship("Comment", back_populates="project")
    versions = relationship("ProjectVersion", back_populates="project")

class ProjectFile(Base):
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    file_path = Column(String(255), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    file_type = Column(String(50))  # frontend/backend
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="files") 