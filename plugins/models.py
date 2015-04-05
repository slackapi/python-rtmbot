#!/usr/bin/env python

from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Definition(Base):
    """"""
    __tablename__ = 'definition'
    id = Column(Integer, primary_key=True)
    term = Column(String(50), nullable=False)
    definition = Column(String(1000), nullable=False)
