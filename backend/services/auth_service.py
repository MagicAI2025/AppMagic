from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from models.user import User, UserRole
from sqlalchemy.orm import Session

class AuthService:
    SECRET_KEY = "your-secret-key"  # 在生产环境中使用环境变量
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)
    
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)
    
    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
    
    @classmethod
    async def get_current_user(
        cls,
        token: str = Security(oauth2_scheme),
        db: Session = None
    ) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
            
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    
    @classmethod
    def check_admin_permission(cls, user: User):
        if user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Admin permission required"
            ) 