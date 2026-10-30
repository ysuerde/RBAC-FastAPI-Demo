# RBAC-FastAPI-Demo

## 项目简介
基于 Python + FastAPI + MySQL 实现的轻量级 RBAC（基于角色的访问控制）后台系统。实现了 JWT 身份认证与细粒度的接口级权限拦截，并配有 Pytest 自动化回归测试。

## 技术栈
- 后端框架：FastAPI
- 数据库：MySQL + SQLAlchemy (ORM)
- 身份认证：JWT (python-jose) + Bcrypt (passlib)
- 自动化测试：Pytest + HTTPX

## 核心功能
1. **JWT 登录认证**：密码采用 bcrypt 加盐哈希存储，登录返回 JWT 鉴权 Token，服务端无状态。
2. **RBAC 权限模型**：基于 User、Role、Permission 的五表关联设计，支持灵活的角色权限分配。
3. **细粒度越权拦截**：封装 `require_permission` 依赖注入，实现接口级权限校验。普通用户越权请求管理员接口时直接返回 403 Forbidden。
4. **自动化回归测试**：覆盖登录成功、未认证拦截(401)、越权拦截(403)三大核心业务场景。

## 快速启动
1. 安装依赖：`pip install -r requirements.txt`
2. 导入数据库：执行 `init.sql` 建库建表
3. 启动服务：`uvicorn main:app --reload`
4. 访问接口文档：`http://127.0.0.1:8000/docs`