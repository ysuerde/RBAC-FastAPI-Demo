from database import SessionLocal
from models import Role

db = SessionLocal()
roles = db.query(Role).all()
for r in roles:
    print(f"角色ID: {r.id}, 名称: {r.name}, 代码: {r.code}")
db.close()