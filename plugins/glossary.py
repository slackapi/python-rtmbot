#!/usr/bin/env python

import db
from models import Definition

COMMANDS = ['!define', '!whatis']

outputs = []

def make_sender(channel_id):
    global outputs
    def sender(msg):
        outputs.append([channel_id, msg])

    return send


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

    try:
        session.add(new_definition)
        session.commit()
        return True, term, definition
    except:
        import sys
        e = sys.exc_info()[0]
        return False, e, None


def handle_whatis_result(defs, send):
    """ Do the Right Thing with zero or more Definitions """
    if len(defs) == 0:
        send("I don't have a definition for that.")
    elif len(defs) == 1:
        handle_single_defn(defs, send)
    else:
        handle_multi_defn(defs, send)


def handle_single_defn(defn, send):
    """"""
    single_defn = '{term}: {definition}'.format
    send(single_defn(term=defn))


def handle_multi_defn(defs, send):
    """"""
    num_defs = len(defs)
    send("Found {} definitions for, '{}'".format(num_defs, defs[0].term))

    row_template = "{term} ({index}/{total}): {definition}".format
    for i, defn in enumerate(defs):
        msg = row_template(
            term=defn.term,
            index=i + 1,
            total=num_defs,
            definition=defn.definition
        )
        send(msg)


def handle_definition_result(result, send):
    """ Return a response, depending on definition result"""
    success = "Okay! {term} is now defined as, '{definition}'".format
    failure = "Erk! Something went wrong :-/ Check the logs? (lol j/k no logs yet -_-)"

    worked, term, definition = result

    if worked:
        send(success(term=term, definition=definition))
    else:
        send(failure)


def process_messages(data):
    """Process an incoming message from Slack"""
    text = data["text"]
    channel_id = data["channel_id"]

    sender = make_sender(channel_id)

    command = text.split(" ")[0]

    if command not in COMMANDS:
        pass
    elif command == '!define':
        term_and_def = text.split(" ", 1)[1]
        term, definition = term_and_def.split(":", 1)
        res = define(term.strip(), definition.strip())
        handle_definition_result(res, sender)
    elif command == '!whatis':
        term = text.split(" ")[1].strip()
        defns = whatis(term)
        handle_whatis_result(defns, sender)
    else:
        print 'butts'
