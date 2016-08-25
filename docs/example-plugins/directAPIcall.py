from __future__ import unicode_literals
from client import slack_client as sc


def process_message(data):
    '''If a user passes 'print users' in a message, print the users in the slack
    team to the console. (Don't run this in production probably)'''

    if 'print users' in data['text']:
        for user in sc.api_call("users.list")["members"]:
            print(user["name"], user["id"])
