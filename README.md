python-rtmbot
=============

[![Build Status](https://travis-ci.org/slackhq/python-rtmbot.png)](https://travis-ci.org/slackhq/python-rtmbot)
[![Coverage Status](https://coveralls.io/repos/github/slackhq/python-rtmbot/badge.svg?branch=master)](https://coveralls.io/github/slackhq/python-rtmbot?branch=master)

A Slack bot written in python that connects via the RTM API.

Python-rtmbot is a callback based bot engine. The plugins architecture should be familiar to anyone with knowledge to the [Slack API](https://api.slack.com) and Python. The configuration file format is YAML.

Some differences to webhooks:

1. Doesn't require a webserver to receive messages
2. Can respond to direct messages from users
3. Logs in as a slack user (or bot)
4. Bot users must be invited to a channel

Dependencies
----------
* websocket-client https://pypi.python.org/pypi/websocket-client/
* python-slackclient https://github.com/slackhq/python-slackclient

Installation
-----------

1. Download the python-rtmbot code

        git clone https://github.com/slackhq/python-rtmbot.git
        cd python-rtmbot

2. Install dependencies ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)

        pip install -r requirements.txt

3. Configure rtmbot (https://api.slack.com/bot-users)

        cp docs/example-config/rtmbot.conf .
        vi rtmbot.conf
          SLACK_TOKEN: "xoxb-11111111111-222222222222222"

*Note*: At this point rtmbot is ready to run, however no plugins are configured.

Add Plugins
-------

Plugins can be installed as .py files in the ```plugins/``` directory OR as a .py file in any first level subdirectory. If your plugin uses multiple source files and libraries, it is recommended that you create a directory. You can install as many plugins as you like, and each will handle every event received by the bot indepentently.

To install the example 'repeat' plugin

    mkdir plugins/repeat
    cp docs/example-plugins/repeat.py plugins/repeat/

The repeat plugin will now be loaded by the bot on startup.

    ./rtmbot.py

Create Plugins
--------

####Incoming data
Plugins are callback based and respond to any event sent via the rtm websocket. To act on an event, create a function definition called process_(api_method) that accepts a single arg. For example, to handle incoming messages:

    def process_message(data):
        print data

This will print the incoming message json (dict) to the screen where the bot is running.

Plugins having a method defined as ```catch_all(data)``` will receive ALL events from the websocket. This is useful for learning the names of events and debugging.

Note: If you're using Python 2.x, the incoming data should be a unicode string, be careful you don't coerce it into a normal str object as it will cause errors on output. You can add `from __future__ import unicode_literals` to your plugin file to avoid this.

####Outgoing data
Plugins can send messages back to any channel, including direct messages. This is done by appending a two item array to the outputs global array. The first item in the array is the channel ID and the second is the message text. Example that writes "hello world" when the plugin is started:

    outputs = []
    outputs.append(["C12345667", "hello world"])

*Note*: you should always create the outputs array at the start of your program, i.e. ```outputs = []```

####Timed jobs
Plugins can also run methods on a schedule. This allows a plugin to poll for updates or perform housekeeping during its lifetime. This is done by appending a two item array to the crontable array. The first item is the interval in seconds and the second item is the method to run. For example, this will print "hello world" every 10 seconds.

    outputs = []
    crontable = []
    crontable.append([10, "say_hello"])
    def say_hello():
        outputs.append(["C12345667", "hello world"])

####Plugin misc
The data within a plugin persists for the life of the rtmbot process. If you need persistent data, you should use something like sqlite or the python pickle libraries.

####Todo:
Some rtm data should be handled upstream, such as channel and user creation. These should create the proper objects on-the-fly.
