from fastapi import FastAPI, HTTPException, Depends, Query, Security
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Dict, List
import uvicorn
from sqlalchemy.orm import Session
from models.database import get_db
from services.ai_service import AICodeGenerator
from services.db_service import DatabaseService
from sqlalchemy import desc
from sqlalchemy.sql import func
from services.auth_service import AuthService
from services.user_service import UserService
from models.user import UserRole, User
from services.share_service import ShareService
from models.project_share import SharePermission
from services.collaboration_service import CollaborationService
from services.database_manager import db_manager
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from middleware.error_handler import error_handler

app = FastAPI(
    title="App Magic API",
    description="AI-Powered Application Generation Platform",
    version="1.0.0"
)
ai_generator = AICodeGenerator()

# Add CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.middleware("http")(error_handler)

class ProjectRequirements(BaseModel):
    description: str
    project_type: Optional[str] = "web"
    model: Optional[str] = None

# Add request models
class ProjectUpdate(BaseModel):
    description: Optional[str] = None
    project_type: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    role: Optional[UserRole] = UserRole.USER

class Token(BaseModel):
    access_token: str
    token_type: str

# Add request models
class ShareCreate(BaseModel):
    user_id: int
    permission: SharePermission

class CommentCreate(BaseModel):
    content: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None

class CommentReplyCreate(BaseModel):
    content: str

class VersionCreate(BaseModel):
    version_number: str
    description: str
    files: Dict[str, str]

@app.post("/api/generate")
async def generate_project(
    requirements: ProjectRequirements,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Generate new project"""
    try:
        # Allow model selection in request
        model = requirements.model if hasattr(requirements, 'model') else None
        
        # Analyze requirements
        project_structure = await ai_generator.analyze_requirements(
            requirements.description,
            model=model
        )
        
        # Generate code
        generated_code = await ai_generator.generate_code(
            project_structure,
            model=model
        )
        
        # Save to database
        project = await DatabaseService.create_project(
            db=db,
            description=requirements.description,
            project_type=requirements.project_type,
            structure=project_structure,
            generated_files=generated_code,
            owner_id=current_user.id,
            model=requirements.model
        )
        
        return {
            "status": "success",
            "message": "Project generated successfully",
            "project_id": project.id,
            "files": {f.file_path: f.content for f in project.files}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate project: {str(e)}")

@app.get("/api/projects/{project_id}")
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project details"""
    project = await DatabaseService.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    files = await DatabaseService.get_project_files(db, project_id)
    return {
        "project": {
            "id": project.id,
            "description": project.description,
            "project_type": project.project_type,
            "structure": project.structure,
            "created_at": project.created_at
        },
        "files": [
            {
                "path": f.file_path,
                "content": f.content,
                "type": f.file_type
            } for f in files
        ]
    }

@app.get("/api/projects")
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    project_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get projects list"""
    projects = await DatabaseService.list_projects(
        db, skip, limit, project_type
    )
    return {
        "total": len(projects),
        "projects": [
            {
                "id": p.id,
                "description": p.description,
                "project_type": p.project_type,
                "created_at": p.created_at
            } for p in projects
        ]
    }

@app.put("/api/projects/{project_id}")
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    project = await DatabaseService.update_project(
        db,
        project_id,
        project_update.description,
        project_update.project_type
    )
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return {
        "status": "success",
        "message": "Project updated successfully",
        "project": {
            "id": project.id,
            "description": project.description,
            "project_type": project.project_type,
            "updated_at": project.updated_at
        }
    }

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    success = await DatabaseService.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return {
        "status": "success",
        "message": "Project deleted successfully"
    }

@app.get("/api/projects/search")
async def search_projects(
    keyword: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    projects = await DatabaseService.search_projects(db, keyword, limit)
    return {
        "total": len(projects),
        "projects": [
            {
                "id": p.id,
                "description": p.description,
                "project_type": p.project_type,
                "created_at": p.created_at
            } for p in projects
        ]
    }

@app.get("/api/projects/stats")
async def get_project_stats(db: Session = Depends(get_db)):
    """Get project statistics"""
    total_projects = db.query(Project).count()
    projects_by_type = db.query(
        Project.project_type,
        func.count(Project.id)
    ).group_by(Project.project_type).all()
    
    recent_projects = db.query(Project).order_by(
        desc(Project.created_at)
    ).limit(5).all()
    
    return {
        "total_projects": total_projects,
        "projects_by_type": dict(projects_by_type),
        "recent_projects": [
            {
                "id": p.id,
                "description": p.description,
                "created_at": p.created_at
            } for p in recent_projects
        ]
    }

@app.post("/api/auth/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """User registration"""
    try:
        created_user = await UserService.create_user(
            db,
            email=user.email,
            username=user.username,
            password=user.password,
            role=user.role
        )
        return {
            "status": "success",
            "message": "Registration successful",
            "user_id": created_user.id
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/api/auth/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = await UserService.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/admin/users")
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    AuthService.check_admin_permission(current_user)
    users = db.query(User).all()
    return {
        "total": len(users),
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "username": u.username,
                "role": u.role,
                "is_active": u.is_active
            } for u in users
        ]
    }

@app.post("/api/projects/{project_id}/share")
async def share_project(
    project_id: int,
    share: ShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    project_share = await ShareService.share_project(
        db,
        project_id,
        share.user_id,
        share.permission,
        current_user
    )
    return {
        "status": "success",
        "message": "Project shared successfully",
        "share": {
            "id": project_share.id,
            "project_id": project_share.project_id,
            "user_id": project_share.user_id,
            "permission": project_share.permission
        }
    }

@app.delete("/api/projects/{project_id}/share/{user_id}")
async def remove_share(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    success = await ShareService.remove_share(
        db,
        project_id,
        user_id,
        current_user
    )
    if not success:
        raise HTTPException(status_code=404, detail="Share record not found")
    return {
        "status": "success",
        "message": "Share removed successfully"
    }

@app.get("/api/projects/{project_id}/shares")
async def get_project_shares(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    shares = await ShareService.get_project_shares(db, project_id, current_user)
    return {
        "shares": [
            {
                "id": share.id,
                "user": {
                    "id": share.user.id,
                    "username": share.user.username,
                    "email": share.user.email
                },
                "permission": share.permission,
                "created_at": share.created_at
            } for share in shares
        ]
    }

@app.get("/api/users/me/shared-projects")
async def get_my_shared_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    projects = await ShareService.get_shared_projects(db, current_user.id)
    return {
        "projects": [
            {
                "id": p.id,
                "description": p.description,
                "project_type": p.project_type,
                "owner": {
                    "id": p.owner.id,
                    "username": p.owner.username
                },
                "created_at": p.created_at
            } for p in projects
        ]
    }

# 评论相关端点
@app.post("/api/projects/{project_id}/comments")
async def add_comment(
    project_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    new_comment = await CollaborationService.add_comment(
        db,
        project_id,
        current_user.id,
        comment.content,
        comment.file_path,
        comment.line_number
    )
    return {
        "status": "success",
        "comment": {
            "id": new_comment.id,
            "content": new_comment.content,
            "user": {
                "id": current_user.id,
                "username": current_user.username
            },
            "created_at": new_comment.created_at
        }
    }

@app.post("/api/comments/{comment_id}/replies")
async def add_reply(
    comment_id: int,
    reply: CommentReplyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    new_reply = await CollaborationService.add_reply(
        db,
        comment_id,
        current_user.id,
        reply.content
    )
    return {
        "status": "success",
        "reply": {
            "id": new_reply.id,
            "content": new_reply.content,
            "user": {
                "id": current_user.id,
                "username": current_user.username
            },
            "created_at": new_reply.created_at
        }
    }

@app.get("/api/projects/{project_id}/comments")
async def get_project_comments(
    project_id: int,
    file_path: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    comments = await CollaborationService.get_project_comments(
        db, project_id, file_path
    )
    return {
        "comments": [
            {
                "id": c.id,
                "content": c.content,
                "file_path": c.file_path,
                "line_number": c.line_number,
                "user": {
                    "id": c.user.id,
                    "username": c.user.username
                },
                "created_at": c.created_at,
                "replies": [
                    {
                        "id": r.id,
                        "content": r.content,
                        "user": {
                            "id": r.user.id,
                            "username": r.user.username
                        },
                        "created_at": r.created_at
                    } for r in c.replies
                ]
            } for c in comments
        ]
    }

# Version control endpoints
@app.post("/api/projects/{project_id}/versions")
async def create_version(
    project_id: int,
    version: VersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    new_version = await CollaborationService.create_version(
        db,
        project_id,
        version.version_number,
        version.description,
        current_user.id,
        version.files
    )
    return {
        "status": "success",
        "version": {
            "id": new_version.id,
            "version_number": new_version.version_number,
            "description": new_version.description,
            "created_at": new_version.created_at
        }
    }

@app.get("/api/projects/{project_id}/versions")
async def get_project_versions(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    versions = await CollaborationService.get_project_versions(db, project_id)
    return {
        "versions": [
            {
                "id": v.id,
                "version_number": v.version_number,
                "description": v.description,
                "created_by": {
                    "id": v.creator.id,
                    "username": v.creator.username
                },
                "created_at": v.created_at
            } for v in versions
        ]
    }

@app.get("/api/versions/{version_id}/files")
async def get_version_files(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    files = await CollaborationService.get_version_files(db, version_id)
    return {
        "files": [
            {
                "id": f.id,
                "file_path": f.file_path,
                "content": f.content
            } for f in files
        ]
    }

@app.get("/api/health")
async def health_check():
    """Check system health status"""
    db_healthy = await db_manager.health_check()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": datetime.utcnow()
    }

@app.post("/api/projects/{project_id}/backup")
async def backup_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Backup project data"""
    backup_data = await DatabaseService.backup_project(db, project_id)
    return {
        "status": "success",
        "message": "Project backup successful",
        "backup_data": backup_data
    }

@app.post("/api/projects/{project_id}/files")
async def save_project_files(
    project_id: int,
    files: Dict[str, str],
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Save project files"""
    saved_files = await DatabaseService.save_project_files(db, project_id, files)
    return {
        "status": "success",
        "message": "Files saved successfully",
        "files": [
            {
                "path": f.file_path,
                "type": f.file_type
            } for f in saved_files
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 