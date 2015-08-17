import client

outputs = []

# prints all users who are currently active in the channel
def print_active_users():
    #NOTE: you must add a real channel ID for this to work
    active_users = get_active_users()
    outputs.append([u"XXXXXXXXX", active_users])

# calls the API to get all the users
# then checks the status of each user
# returns a list of the active users joined by spaces
def get_active_users():
    users = client.get_users()
    present_users = []
    # print all_users
    for user in users:
        presence = client.get_presence(user['id'])
        if presence['presence'] == 'active':
            present_users.append(user['real_name'])
    return u', '.join(present_users)

print_active_users()
