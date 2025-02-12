from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="owner")
    shared_projects = relationship("ProjectShare", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    comment_replies = relationship("CommentReply", back_populates="user")
    created_versions = relationship("ProjectVersion", back_populates="creator")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    file_path = Column(String, nullable=True)  # Optional, for file-specific comments
    line_number = Column(Integer, nullable=True)  # Optional, for line-specific comments
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("CommentReply", back_populates="parent_comment")

class CommentReply(Base):
    __tablename__ = "comment_replies"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    parent_comment = relationship("Comment", back_populates="replies")
    user = relationship("User", back_populates="comment_replies")

class ProjectVersion(Base):
    __tablename__ = "project_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    version_number = Column(String, nullable=False)  # 如 "1.0.0"
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="versions")
    files = relationship("VersionFile", back_populates="version")
    creator = relationship("User", back_populates="created_versions")

class VersionFile(Base):
    __tablename__ = "version_files"
    
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("project_versions.id", ondelete="CASCADE"))
    file_path = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    
    version = relationship("ProjectVersion", back_populates="files") 