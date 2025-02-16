from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# 导入其他必要的模块
from models.database import SessionLocal, engine
from models.user import User             # 新增：导入User类型
from services import ai_service, user_service, project_service
from services.ai_service import AIService
from services.user_service import UserService
from services.project_service import ProjectService
from services.auth_service import AuthService, get_current_user
from schemas.project import ProjectCreate, ProjectResponse

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加可信主机中间件
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# 添加压缩中间件
app.add_middleware(GZipMiddleware)

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 请求模型
class GenerateRequest(BaseModel):
    prompt: str
    language: Optional[str] = "python"
    
# 响应模型
class GenerateResponse(BaseModel):
    code: str
    message: Optional[str] = None

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest, db: Session = Depends(get_db)):
    try:
        # 调用 AI 服务生成代码
        generated_code = await ai_service.generate_code(
            prompt=request.prompt,
            language=request.language,
            db=db
        )
        return GenerateResponse(code=generated_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 健康检查接口
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 项目管理路由
@app.post("/api/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await ProjectService.create_project(db, project)

@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await ProjectService.get_project(db, project_id)

# 公开路由
@app.get("/api/projects")
async def read_projects_public(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(Project).offset(skip).limit(limit).all()

# 需要认证的路由
@app.post("/api/generate")
async def generate_code_protected(
    request: GenerateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await ai_service.generate_code(request.prompt, request.language, db)

# 其他路由...