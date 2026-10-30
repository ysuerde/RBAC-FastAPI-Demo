from database import SessionLocal
from models import User, Role
from auth import get_password_hash

db = SessionLocal()
if not db.query(User).filter(User.username == "testuser").first():
    new_user = User(username="testuser", password_hash=get_password_hash("123456"))
    # 绑定普通用户角色（之前 init.sql 里插了 role code 为 'user' 的角色）
    user_role = db.query(Role).filter(Role.code == "user").first()
    new_user.roles.append(user_role)
    db.add(new_user)
    db.commit()
    print("普通测试账号 testuser 创建成功，密码 123456")
else:
    print("testuser 已存在，不用重复造")
db.close()