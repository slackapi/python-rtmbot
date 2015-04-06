#!/usr/bin/env python

import db
from models import Definition

COMMANDS = ['!define', '!whatis']


def whatis(term):
    """
    Try to look up a term; returns a list of 0 or more  definitions
    """
    session = db.get_session()
    definitions = (
        session
        .query(Definition)
        .filter(Definition.term == term)
        .all()
    )

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
    if len(defs) == 0:
        print "I don't have a definition for that."
    elif len(defs) == 1:
        handle_single_defn(defs)
    else:
        handle_multi_defn(defs)


def handle_single_defn(defn):
    """"""
    single_defn = '{term}: {definition}'.format
    print single_defn(term=defn)


def handle_multi_defn(defs):
    """"""
    num_defs = len(defs)
    print "Found {} definitions for, '{}'".format(num_defs, defs[0].term)
    row_template = "{term} ({index}/{total}): {definition}".format
    for i, defn in enumerate(defs):
        print row_template(
            term=defn.term,
            index=i + 1,
            total=num_defs,
            definition=defn.definition
        )


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
