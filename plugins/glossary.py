#!/usr/bin/env python

import db
from models import Definition


def process_messages(data):
    """Process an incoming message from Slack"""
    pass


def define(term, definition):
    """Define a term"""
    session = db.get_session()
    new_definition = Definition(term, definition)
    try:
        session.add(new_definition)
        session.commit()
        return True
    except:
        import sys
        e = sys.exc_info()[0]
        return False, e
