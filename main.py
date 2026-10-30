from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from models import User, Article
from schemas import Token
from auth import verify_password, create_access_token
from deps import get_current_user, require_permission

app = FastAPI(title="RBAC权限管理系统")

# 1. 登录接口
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 2. 建文章接口（要求必须登录）
@app.post("/articles")
def create_article(title: str, content: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    article = Article(title=title, content=content, author_id=current_user.id)
    db.add(article)
    db.commit()
    return {"message": "文章创建成功", "article_id": article.id}

# 3. 删文章接口（要求必须有 article:delete 权限）
@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("article:delete"))):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(article)
    db.commit()
    return {"message": f"管理员 {current_user.username} 成功删除了文章 {article_id}"}