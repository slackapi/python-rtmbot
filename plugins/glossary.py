#!/usr/bin/env python

import db
from models import Definition

COMMANDS = ['!define', '!whatis']


def whatis(term):
    """ Try to look up a term """
    session = db.get_session()
    definitions = session \
        .query(Definition) \
        .filter(Definition.term == term) \
        .all() \

    return definitions


def define(term, definition):
    """Define a term"""
    session = db.get_session()
    new_definition = Definition(term=term, definition=definition)
    print session
    try:
        session.add(new_definition)
        session.commit()
        return True, term, definition
    except:
        import sys
        e = sys.exc_info()[0]
        return False, e, None


def handle_whatis_result(defs):
    """ Do the Right Thing with zero or more Definitions """
    single_defn = '{term}: {definition}'.format
    for defn in defs:
        print single_defn(term=defn.term, definition=defn.definition)


def handle_definition_result(result):
    """ Return a response, depending on definition result"""
    success = "Okay! {term} is now defined as, '{definition}'".format
    failure = "Erk! Something went wrong :-/ Check the logs?"

    worked, term, definition = result

    if worked:
        print success(term=term, definition=definition)
    else:
        print failure
        print term


def process_messages(data):
    """Process an incoming message from Slack"""
    text = data["text"]
    command = text.split(" ")[0]
    print command
    if command not in COMMANDS:
        print "Command {} not recognized".format(command)
    elif command == '!define':
        term_and_def = text.split(" ", 1)[1]
        term, definition = term_and_def.split(":", 1)
        res = define(term.strip(), definition.strip())
        handle_definition_result(res)
    elif command == '!whatis':
        term = text.split(" ")[1].strip()
        defns = whatis(term)
        handle_whatis_result(defns)
    else:
        print 'butts'
