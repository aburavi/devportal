from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Date,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import ARRAY, Interval
from .db import Base

class EntityUser(Base):
    __tablename__ = "users"
    db_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(String(100), index=True)
    username = Column(String(50))
    firstname = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(50))
    phone = Column(String(30))
    company = Column(String(30))
    address = Column(String(200))
    isactive = Column(Boolean, default=True)
    avatar = Column(String(200))
    rolecode = Column(String(5))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) if getattr(self, c.name) is not None else None for c in self.__table__.columns}
    
class EntityApps(Base):
    __tablename__ = "apps"
    db_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(String(100), index=True)
    name = Column(String(50))
    consumer_key = Column(String(100))
    consumer_secret = Column(String(200))
    type = Column(String(15))
    src_accounts = Column(ARRAY(String))
    max_rate = Column(String(10))
    products = Column(ARRAY(String))
    expired_at = Column(DateTime)
    isactive = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) if getattr(self, c.name) is not None else None for c in self.__table__.columns}

class EntityBaseCrypto(Base):
    __tablename__ = "basecrypto"
    db_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(String(100), index=True)
    public_key = Column(String(5000))
    private_key = Column(String(5000))
    expired_at = Column(DateTime)
    isactive = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) if getattr(self, c.name) is not None else None for c in self.__table__.columns}

class EntityProducts(Base):
    __tablename__ = "products"
    db_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(100), index=True)
    deskripsi = Column(String(500))
    type = Column(String(15))
    code = Column(String(3))
    uripath = Column(String(100))
    method = Column(String(10))
    version = Column(String(10))
    isactive = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) if getattr(self, c.name) is not None else None for c in self.__table__.columns}

class EntityProductionRequest(Base):
    __tablename__ = "production_request"
    db_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(String(100), index=True)
    requested_by = Column(String(50))
    request_type = Column(String(50))
    status = Column(String(50))
    template_file = Column(String(500))
    final_file = Column(String(500))
    approved_at = Column(DateTime)
    approved_by = Column(String(50))
    isactive = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) if getattr(self, c.name) is not None else None for c in self.__table__.columns}

class EntityAppsHistory(Base):
    __tablename__ = "app_history"
    db_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(String(100), index=True)
    content = Column(String(50))
    content_type = Column(String(50))
    description = Column(String(200))
    status = Column(String(50))
    approved_by = Column(String(50))
    approved_at = Column(DateTime)
    isactive = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) if getattr(self, c.name) is not None else None for c in self.__table__.columns}
