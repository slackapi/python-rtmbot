from __future__ import unicode_literals
from client import client as sc

for user in sc.api_call("users.list")["members"]:
    print(user["name"], user["id"])
