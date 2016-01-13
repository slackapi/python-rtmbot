import time
import re
import random
import logging
crontable = []
outputs = []
typing_sleep = 0

greetings = ['Hi friend!', 'Hello there.', 'Howdy!', 'Wazzzup!!!', 'Hi!', 'Hey.']
help_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
    "I will respond to the following messages: ",
    "`pybot hi` for a random greeting.",
    "`pybot joke` for a question, typing indicator, then answer style joke.",
    "`pybot attachment` to see a Slack attachment message.",
    "`@<your bot's name>` to demonstrate detecting a mention.",
    "`pybot help` to see this again.")

# regular expression patterns for string matching
p_bot_hi = re.compile("pybot[\s]*hi")
p_bot_joke = re.compile("pybot[\s]*joke")
p_bot_attach = re.compile("pybot[\s]*attachment")
p_bot_help = re.compile("pybot[\s]*help")

def process_message(data):
    logging.debug("process_message:data: {}".format(data))
    if p_bot_hi.match(data['text']):
        outputs.append([data['channel'], "{}".format(random.choice(greetings))])
    elif p_bot_joke.match(data['text']):
        outputs.append([data['channel'], "Why did the python cross the road?"])
        outputs.append([data['channel'], "__typing__", 5])
        outputs.append([data['channel'], "To eat the chicken on the other side! :laughing:"])
    elif p_bot_attach.match(data['text']):
        outputs.append([data['channel'], "Sorry, I can't do this yet. :disappointed:"])
    elif p_bot_help.match(data['text']):
        outputs.append([data['channel'], "{}".format(help_text)])
    elif data['text'].startswith("pybot"):
        outputs.append([data['channel'], "I'm sorry, I don't know how to: `{}`".format(data['text'])])
    elif data['channel'].startswith("D"):  # direct message channel to the bot
        outputs.append([data['channel'], "Hello, I'm the BeepBoop python starter bot.\n{}".format(help_text)])

def process_mention(data):
    logging.debug("process_mention:data: {}".format(data))
    outputs.append([data['channel'], "You really do care about me. :heart:"])
