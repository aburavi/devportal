from sqlalchemy import MetaData, Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)
