from slackclient import SlackClient
import json

api_client = None


def init(token):
    global api_client
    api_client = SlackClient(token)
    return api_client


def get_users():
    return json.loads(api_client.api_call('users.list'))['members']


def get_presence(id):
    return json.loads(api_client.api_call('users.getPresence', user=id))
