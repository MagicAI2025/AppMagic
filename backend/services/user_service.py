from sqlalchemy.orm import Session
from models.user import User, UserRole
from .auth_service import AuthService
from fastapi import HTTPException
from typing import Optional

class UserService:
    @staticmethod
    async def create_user(
        db: Session,
        email: str,
        username: str,
        password: str,
        role: UserRole = UserRole.USER
    ) -> User:
        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="邮箱已被注册")
            
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="用户名已被使用")
            
        hashed_password = AuthService.get_password_hash(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            role=role
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    async def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user 