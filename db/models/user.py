from db.base_class import Base
from sqlalchemy import Boolean,Column,Integer,String,DateTime,ForeignKey,JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user_account_table'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable = True)
    address = Column(String, nullable = True)
    phone = Column(String, nullable = True, unique = True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=True)
    secret_key=Column(String, nullable=True, unique=True)
    is_active = Column(Boolean(), default=True)
    is_delete = Column(Boolean(), default=False)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())
    updated_by = Column(Integer,nullable=True)


