from slackclient import SlackClient
import json

# instance of API client that can be accessed from other files
api_client = None


# create an instance of the api client and initialize it with a token
def init(token):
    global api_client
    api_client = SlackClient(token)
    return api_client


# example functions

# get_users() returns a list of users in a Slack organization
def get_users():
    return json.loads(api_client.api_call('users.list'))['members']

# get_presence returns if a certain user is active or not in chat
def get_presence(id):
    return json.loads(api_client.api_call('users.getPresence', user=id))
