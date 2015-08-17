from slackclient import SlackClient
import json

api_client = None


def init(token):
    global api_client
    api_client = SlackClient(token)
    return api_client
