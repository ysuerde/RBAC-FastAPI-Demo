from pydantic import BaseModel

# 登录请求体：只要账号密码
class UserLogin(BaseModel):
    username: str
    password: str

# Token响应体
class Token(BaseModel):
    access_token: str
    token_type: str