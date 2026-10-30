from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id'), primary_key=True),
    Column('role_id', BigInteger, ForeignKey('roles.id'), primary_key=True)
)

role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', BigInteger, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', BigInteger, ForeignKey('permissions.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(SmallInteger, default=1)
    created_at = Column(DateTime, server_default=func.now())
    roles = relationship("Role", secondary=user_roles, backref="users")

class Role(Base):
    __tablename__ = "roles"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    permissions = relationship("Permission", secondary=role_permissions, backref="roles")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(50), unique=True, nullable=False)

class Article(Base):
    __tablename__ = "articles"
    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    author_id = Column(BigInteger, ForeignKey("users.id"))
    status = Column(SmallInteger, default=1)
    created_at = Column(DateTime, server_default=func.now())