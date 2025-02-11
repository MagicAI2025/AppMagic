from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    project_type = Column(String, default="web")
    model = Column(String)  # Store which model was used
    structure = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    files = relationship("ProjectFile", back_populates="project")
    owner = relationship("User", back_populates="projects")
    shares = relationship("ProjectShare", back_populates="project")
    comments = relationship("Comment", back_populates="project")
    versions = relationship("ProjectVersion", back_populates="project")

class ProjectFile(Base):
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    file_path = Column(String, nullable=False)
    content = Column(String, nullable=False)
    file_type = Column(String)  # frontend/backend
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="files") 