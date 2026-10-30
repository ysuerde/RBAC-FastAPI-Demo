from fastapi.testclient import TestClient
from main import app

# 创建测试客户端，相当于不用起服务就能直接测
client = TestClient(app)


# 测试 1：管理员登录拿 Token
def test_login_success():
    response = client.post("/login", data={"username": "admin", "password": "123456"})
    assert response.status_code == 200
    assert "access_token" in response.json()


# 测试 2：未登录直接删文章（拦截 401）
def test_delete_without_token():
    response = client.delete("/articles/1")
    assert response.status_code == 401


# 测试 3：普通用户越权删文章（拦截 403）
def test_delete_insufficient_permission():
    # 先登录拿普通用户的 Token
    login_res = client.post("/login", data={"username": "testuser", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 带着普通 Token 去删文章
    response = client.delete("/articles/1", headers=headers)

    # 断言：状态码必须是 403，且报错信息对得上
    assert response.status_code == 403
    assert "权限不足" in response.json()["detail"]