from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Dict, List, Optional
from models.project import Project, ProjectFile
from models.user import User, UserRole
from fastapi import HTTPException
from models.project_share import ProjectShare
from services.database_manager import db_manager
import json
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    @staticmethod
    async def create_project(
        db: Session,
        description: str,
        project_type: str,
        structure: Dict,
        generated_files: Dict[str, str],
        owner_id: int
    ) -> Project:
        try:
            # 创建项目记录
            project = Project(
                description=description,
                project_type=project_type,
                structure=structure,
                owner_id=owner_id
            )
            db.add(project)
            db.flush()
            
            # 保存生成的文件
            for file_path, content in generated_files.items():
                file_type = "frontend" if "frontend/" in file_path else "backend"
                project_file = ProjectFile(
                    project_id=project.id,
                    file_path=file_path,
                    content=content,
                    file_type=file_type
                )
                db.add(project_file)
            
            db.commit()
            db.refresh(project)
            
            # 记录项目创建日志
            logger.info(f"Project created: {project.id} by user {owner_id}")
            
            return project
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating project: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="项目创建失败"
            )
    
    @staticmethod
    async def save_project_files(
        db: Session,
        project_id: int,
        files: Dict[str, str]
    ) -> List[ProjectFile]:
        try:
            # 删除现有文件
            db.query(ProjectFile).filter(
                ProjectFile.project_id == project_id
            ).delete()
            
            # 保存新文件
            saved_files = []
            for file_path, content in files.items():
                file_type = "frontend" if "frontend/" in file_path else "backend"
                project_file = ProjectFile(
                    project_id=project_id,
                    file_path=file_path,
                    content=content,
                    file_type=file_type
                )
                db.add(project_file)
                saved_files.append(project_file)
            
            db.commit()
            return saved_files
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving project files: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="文件保存失败"
            )
    
    @staticmethod
    async def backup_project(
        db: Session,
        project_id: int
    ) -> str:
        """备份项目数据"""
        try:
            project = await DatabaseService.get_project(db, project_id)
            if not project:
                raise HTTPException(status_code=404, detail="项目不存在")
                
            files = await DatabaseService.get_project_files(db, project_id)
            
            backup_data = {
                "project": {
                    "id": project.id,
                    "description": project.description,
                    "project_type": project.project_type,
                    "structure": project.structure,
                    "created_at": str(project.created_at)
                },
                "files": [
                    {
                        "path": f.file_path,
                        "content": f.content,
                        "type": f.file_type
                    } for f in files
                ]
            }
            
            # TODO: 将备份数据保存到对象存储
            return json.dumps(backup_data, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error backing up project: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="项目备份失败"
            )
    
    @staticmethod
    async def get_project(
        db: Session,
        project_id: int,
        user: Optional[User] = None
    ) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if user and not await DatabaseService.check_project_access(db, project_id, user):
            raise HTTPException(status_code=403, detail="没有访问权限")
        return project
    
    @staticmethod
    async def get_project_files(db: Session, project_id: int) -> List[ProjectFile]:
        return db.query(ProjectFile).filter(
            ProjectFile.project_id == project_id
        ).all()
    
    @staticmethod
    async def list_projects(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        project_type: Optional[str] = None
    ) -> List[Project]:
        query = db.query(Project).order_by(desc(Project.created_at))
        
        if project_type:
            query = query.filter(Project.project_type == project_type)
            
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    async def update_project(
        db: Session,
        project_id: int,
        description: Optional[str] = None,
        project_type: Optional[str] = None
    ) -> Optional[Project]:
        project = await DatabaseService.get_project(db, project_id)
        if not project:
            return None
            
        if description:
            project.description = description
        if project_type:
            project.project_type = project_type
            
        db.commit()
        db.refresh(project)
        return project
    
    @staticmethod
    async def delete_project(db: Session, project_id: int) -> bool:
        project = await DatabaseService.get_project(db, project_id)
        if not project:
            return False
            
        # 首先删除相关的文件
        db.query(ProjectFile).filter(
            ProjectFile.project_id == project_id
        ).delete()
        
        # 然后删除项目
        db.delete(project)
        db.commit()
        return True
    
    @staticmethod
    async def search_projects(
        db: Session,
        keyword: str,
        limit: int = 10
    ) -> List[Project]:
        return db.query(Project).filter(
            Project.description.ilike(f"%{keyword}%")
        ).limit(limit).all()
    
    @staticmethod
    async def check_project_access(
        db: Session,
        project_id: int,
        user: User
    ) -> bool:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False
            
        # 检查是否是所有者或管理员
        if project.owner_id == user.id or user.role == UserRole.ADMIN:
            return True
            
        # 检查是否有共享权限
        share = db.query(ProjectShare).filter(
            ProjectShare.project_id == project_id,
            ProjectShare.user_id == user.id
        ).first()
        
        return share is not None 