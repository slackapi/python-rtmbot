import time
import re
import random
import logging
crontable = []
outputs = []
typing_sleep = 0

greetings = ['Hi friend!', 'Hello there.', 'Howdy!', 'Wazzzup!!!', 'Hi!', 'Hey.']
starter_text = "{}  {}\n{}\n{}\n{}\n{}".format(
    "Hello, I'm the BeepBoop python starter bot.",
    "I don't do much yet, but I would like if you talked to me anyway: ",
    "`pybot hi`",
    "`pybot joke`",
    "`pybot attachment`",
    "`@<your bot's name>`")

# regular expression patterns for string matching
p_bot_hi = re.compile("pybot[\s]*hi")
p_bot_joke = re.compile("pybot[\s]*joke")
p_bot_mention = re.compile("")

def process_message(data):
    logging.debug("process_message:data: {}".format(data))
    if p_bot_hi.match(data['text']):
        outputs.append([data['channel'], "{}".format(random.choice(greetings))])
    elif p_bot_joke.match(data['text']):
        outputs.append([data['channel'], "Why did the python cross the road?"])
        outputs.append([data['channel'], "__typing__", 5])
        outputs.append([data['channel'], "To eat the chicken on the other side! :laughing:"])
    elif data['text'].startswith("pybot"):
        outputs.append([data['channel'], "I'm sorry, I don't know how to: `{}`".format(data['text'])])
    elif data['channel'].startswith("D"):  # direct message channel to the bot
        outputs.append([data['channel'], starter_text])

def process_mention(data):
    logging.debug("process_mention:data: {}".format(data))
    outputs.append([data['channel'], "You really do care about me. :heart:"])
