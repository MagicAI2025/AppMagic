from sqlalchemy.orm import Session
from models.collaboration import Comment, CommentReply, ProjectVersion, VersionFile
from models.user import User
from models.project import Project
from fastapi import HTTPException
from typing import List, Optional
import semver

class CollaborationService:
    @staticmethod
    async def add_comment(
        db: Session,
        project_id: int,
        user_id: int,
        content: str,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None
    ) -> Comment:
        comment = Comment(
            project_id=project_id,
            user_id=user_id,
            content=content,
            file_path=file_path,
            line_number=line_number
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    
    @staticmethod
    async def add_reply(
        db: Session,
        comment_id: int,
        user_id: int,
        content: str
    ) -> CommentReply:
        reply = CommentReply(
            comment_id=comment_id,
            user_id=user_id,
            content=content
        )
        db.add(reply)
        db.commit()
        db.refresh(reply)
        return reply
    
    @staticmethod
    async def get_project_comments(
        db: Session,
        project_id: int,
        file_path: Optional[str] = None
    ) -> List[Comment]:
        query = db.query(Comment).filter(Comment.project_id == project_id)
        if file_path:
            query = query.filter(Comment.file_path == file_path)
        return query.order_by(Comment.created_at.desc()).all()
    
    @staticmethod
    async def create_version(
        db: Session,
        project_id: int,
        version_number: str,
        description: str,
        created_by: int,
        files: dict
    ) -> ProjectVersion:
        # Validate version number format
        try:
            semver.parse(version_number)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid version number format, please use semantic versioning (e.g. 1.0.0)"
            )
        
        # Check if version number already exists
        existing_version = db.query(ProjectVersion).filter(
            ProjectVersion.project_id == project_id,
            ProjectVersion.version_number == version_number
        ).first()
        
        if existing_version:
            raise HTTPException(
                status_code=400,
                detail="Version number already exists"
            )
        
        version = ProjectVersion(
            project_id=project_id,
            version_number=version_number,
            description=description,
            created_by=created_by
        )
        db.add(version)
        db.flush()
        
        # Save files
        for file_path, content in files.items():
            version_file = VersionFile(
                version_id=version.id,
                file_path=file_path,
                content=content
            )
            db.add(version_file)
        
        db.commit()
        db.refresh(version)
        return version
    
    @staticmethod
    async def get_project_versions(
        db: Session,
        project_id: int
    ) -> List[ProjectVersion]:
        return db.query(ProjectVersion).filter(
            ProjectVersion.project_id == project_id
        ).order_by(ProjectVersion.created_at.desc()).all()
    
    @staticmethod
    async def get_version_files(
        db: Session,
        version_id: int
    ) -> List[VersionFile]:
        return db.query(VersionFile).filter(
            VersionFile.version_id == version_id
        ).all() 