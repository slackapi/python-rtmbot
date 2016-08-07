from slackclient import SlackClient
from rtmbot import RtmBot

slack_client = None

def init(config):
    global client
    bot = RtmBot(config)
    slack_client = bot.slack_client
    return bot
