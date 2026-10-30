from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 这里：root是你的账号，冒号后面是你的密码，3306是端口，rbac_demo是库名
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:0000@localhost:3306/rbac_demo"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()