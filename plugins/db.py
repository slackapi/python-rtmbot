#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


DB_URI = "sqlite:///doyle_owl.db"


def make_tables():
    """Creates tables for known record types"""
    engine = create_engine(DB_URI)
    Base.metadata.bind = engine
    Base.metadata.create_all()


def get_session():
    """"""
    engine = create_engine(DB_URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
