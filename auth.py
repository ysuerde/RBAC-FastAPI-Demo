from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

# 1. 配置密钥和算法（本地开发随便写个字符串，线上必须配在环境变量里）
SECRET_KEY = "your-super-secret-key-123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 2. 密码哈希工具（bcrypt算法）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密码验证（验证用户输入的明文密码和数据库里的哈希是否匹配）
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 密码加密（把明文变成哈希）
def get_password_hash(password):
    return pwd_context.hash(password)

# 3. 生成 JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()
    # 设置过期时间
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # 加密生成 token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt