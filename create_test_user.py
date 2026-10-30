from database import SessionLocal
from models import User, Role
from auth import get_password_hash

db = SessionLocal()
# 看看有没有 admin 这个用户
user = db.query(User).filter(User.username == "admin").first()
if not user:
    # 造个账号，密码是 123456
    new_user = User(username="admin", password_hash=get_password_hash("123456"))
    # 把数据库里的管理员角色给他
    admin_role = db.query(Role).filter(Role.code == "admin").first()
    new_user.roles.append(admin_role)

    db.add(new_user)
    db.commit()
    print("测试账号 admin 创建成功，密码 123456")
else:
    print("admin 账号已存在，不用重复创建")
db.close()