from rtmbot import RtmBot

slack_client = None


def init(config):
    global slack_client
    bot = RtmBot(config)
    slack_client = bot.slack_client
    return bot
