from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import SECRET_KEY, ALGORITHM

# 告诉 FastAPI，去请求头里的 Authorization: Bearer xxx 拿 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 1. 解析当前用户（把 token 翻译成具体是谁）
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的凭证或登录已过期",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# 2. 权限拦截器（查这个人有没有这个权限）
def require_permission(permission_code: str):
    def permission_checker(current_user: User = Depends(get_current_user)):
        # 把这个用户所有角色的所有权限拿出来，平铺成一个大列表
        user_permissions = []
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.append(perm.code)

        # 如果所需的权限不在里面，直接 403 打回
        if permission_code not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，缺少 {permission_code} 权限"
            )
        return current_user

    return permission_checker