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
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
            
        # 检查是否有权限共享
        if project.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="没有权限共享此项目")
            
        # 检查目标用户是否存在
        target_user = db.query(User).filter(User.id == user_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="用户不存在")
            
        # 检查是否已经共享
        existing_share = db.query(ProjectShare).filter(
            ProjectShare.project_id == project_id,
            ProjectShare.user_id == user_id
        ).first()
        
        if existing_share:
            existing_share.permission = permission
            db.commit()
            return existing_share
            
        # 创建新的共享
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
            
        # 检查权限
        project = db.query(Project).filter(Project.id == project_id).first()
        if project.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="没有权限取消共享")
            
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
            raise HTTPException(status_code=404, detail="项目不存在")
            
        if project.owner_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="没有权限查看共享信息")
            
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