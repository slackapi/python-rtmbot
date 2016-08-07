from slackclient import SlackClient
from rtmbot import RtmBot

client = None

def init(config):
    global client
    bot = RtmBot(config)
    client = bot.slack_client
    return bot
