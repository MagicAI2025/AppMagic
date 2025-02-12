from sqlalchemy.orm import Session
from models.project_share import ProjectShare, SharePermission
from models.user import User
from models.project import Project
from fastapi import HTTPException
from typing import List, Optional

class ShareService:
    @staticmethod
    async def share_project(
        db: Session,
        project_id: int,
        user_id: int,
        permission: SharePermission,
        current_user: User
    ) -> ProjectShare:
        # Check if project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        # Check sharing permissions
        if project.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="No permission to share this project")
            
        # Check if target user exists
        target_user = db.query(User).filter(User.id == user_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Check if already shared
        existing_share = db.query(ProjectShare).filter(
            ProjectShare.project_id == project_id,
            ProjectShare.user_id == user_id
        ).first()
        
        if existing_share:
            existing_share.permission = permission
            db.commit()
            return existing_share
            
        # Create new share
        share = ProjectShare(
            project_id=project_id,
            user_id=user_id,
            permission=permission
        )
        db.add(share)
        db.commit()
        db.refresh(share)
        return share
    
    @staticmethod
    async def remove_share(
        db: Session,
        project_id: int,
        user_id: int,
        current_user: User
    ) -> bool:
        share = db.query(ProjectShare).filter(
            ProjectShare.project_id == project_id,
            ProjectShare.user_id == user_id
        ).first()
        
        if not share:
            return False
            
        # Check permissions
        project = db.query(Project).filter(Project.id == project_id).first()
        if project.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="No permission to remove share")
            
        db.delete(share)
        db.commit()
        return True
    
    @staticmethod
    async def get_project_shares(
        db: Session,
        project_id: int,
        current_user: User
    ) -> List[ProjectShare]:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        if project.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="No permission to view share information")
            
        return db.query(ProjectShare).filter(
            ProjectShare.project_id == project_id
        ).all()
    
    @staticmethod
    async def get_shared_projects(
        db: Session,
        user_id: int
    ) -> List[Project]:
        shares = db.query(ProjectShare).filter(
            ProjectShare.user_id == user_id
        ).all()
        return [share.project for share in shares] 