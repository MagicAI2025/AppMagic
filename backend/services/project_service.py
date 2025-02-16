from sqlalchemy.orm import Session
from models.project import Project
from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

class ProjectService:
    @staticmethod
    def get_project(db: Session, project_id: int) -> ProjectResponse:
        project = db.query(Project).filter(Project.id == project_id).first()
        return ProjectResponse.from_orm(project)

    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Project).offset(skip).limit(limit).all()

    @staticmethod
    def create_project(db: Session, project: ProjectCreate) -> ProjectResponse:
        db_project = Project(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return ProjectResponse.from_orm(db_project)

    @staticmethod
    def update_project(db: Session, project_id: int, project: ProjectUpdate):
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            for field, value in project:
                setattr(db_project, field, value)
            db.commit()
            db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, project_id: int):
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            db.delete(db_project)
            db.commit()
        return db_project 