python-rtmbot
=============

[![Build Status](https://travis-ci.org/slackhq/python-rtmbot.png)](https://travis-ci.org/slackhq/python-rtmbot)
[![Coverage Status](https://coveralls.io/repos/github/slackhq/python-rtmbot/badge.svg?branch=master)](https://coveralls.io/github/slackhq/python-rtmbot?branch=master)

A Slack bot written in Python that connects via the RTM API.

Python-rtmbot is a bot engine. The plugins architecture should be familiar to anyone with knowledge of the [Slack API](https://api.slack.com) and Python. The configuration file format is YAML.

This project is currently pre-1.0. As such, you should plan for it to have breaking changes from time to time. For any breaking changes, we will bump the minor version while we are pre-1.0. (e.g. 0.2.4 -> 0.3.0 implies breaking changes). If stabiilty is important, you'll likely want to lock in a specific minor version)

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

1. Create your project

        mkdir myproject
        cd myproject

2. Install rtmbot (ideally into a [virtualenv](https://virtualenv.readthedocs.io/en/latest/))

        pip install rtmbot

3. Create an rtmbot.conf file and [create a bot for your team](https://api.slack.com/bot-users)

        # Add the following to rtmbot.conf
        DEBUG: True # make this False in production
        SLACK_TOKEN: "xoxb-11111111111-222222222222222"
        ACTIVE_PLUGINS:
            - plugins.repeat.RepeatPlugin

```DEBUG``` will adjust logging verbosity and cause the runner to exit on exceptions, generally making debugging more pleasant.

```SLACK_TOKEN``` is needed to [authenticate with your Slack team.](https://api.slack.com/web#authentication)

```ACTIVE_PLUGINS``` RTMBot will attempt to import any Plugin specified in `ACTIVE_PLUGINS` (relative to your python path) and instantiate them as plugins. These specified classes should inherit from the core Plugin class.

For example, if your python path includes '/path/to/myproject' and you include `plugins.repeat.RepeatPlugin` in ACTIVE_PLUGINS, it will find the RepeatPlugin class within /path/to/myproject/plugins/repeat.py and instantiate it, then attach it to your running RTMBot.

A Word on Structure
-------
To give you a quick sense of how this library is structured, there is a RtmBot class which does the setup and handles input and outputs of messages. It will also search for and register Plugins within the specified directory(ies). These Plugins handle different message types with various methods and can also register periodic Jobs which will be executed by the Plugins.
```
RtmBot
├── Plugin
|      ├── Job
|      └── Job
├── Plugin
└── Plugin
       └── Job
```

Add Plugins
-------
Plugins can live within any python module, but we recommend just putting them in ./plugins. (Don't forget to add an `__init__.py` file to your directory to make it a module -- use `touch __init__.py` within your plugin directory to create one)

To add a plugin, create a file within your plugin directory (./plugins is a good place for it).

    mkdir plugins
    touch plugins/__init__.py
    cd plugins
    vi myplugin.py

Add your plugin content into this file. Here's an example that will just print all of the requests it receives to the console. See below for more information on available methods.

    from __future__ import print_function
    from rtmbot.core import Plugin

    class MyPlugin(Plugin):

        def catch_all(self, data):
            print(data)

You can install as many plugins as you like, and each will handle every event received by the bot indepentently.

To create an example 'repeat' plugin:

Open `plugins/repeat.py`

Add the following:

    from __future__ import print_function
    from __future__ import unicode_literals

    from rtmbot.core import Plugin


    class RepeatPlugin(Plugin):

        def process_message(self, data):
            if data['channel'].startswith("D"):
                self.outputs.append(
                    [data['channel'], 'from repeat1 "{}" in channel {}'.format(
                        data['text'], data['channel']
                    )]
                )

The repeat plugin will now be loaded by the bot on startup. Run `rtmbot` from console to start your RtmBot.

    rtmbot

Create Plugins
--------

#### Incoming data
All events from the RTM websocket are sent to the registered plugins. To act on an event, create a function definition, inside your Plugin class, called process_(api_method) that accepts a single arg for data. For example, to handle incoming messages:

    def process_message(self, data):
        print data

This will print the incoming message json (dict) to the screen where the bot is running.

Plugins having a method defined as ```catch_all(self, data)``` will receive ALL events from the websocket. This is useful for learning the names of events and debugging.

For a list of all possible API Methods, look here: https://api.slack.com/rtm

Note: If you're using Python 2.x, the incoming data should be a unicode string, be careful you don't coerce it into a normal str object as it will cause errors on output. You can add `from __future__ import unicode_literals` to your plugin file to avoid this.

#### Outgoing data

##### RTM Output
Plugins can send messages back to any channel or direct message. This is done by appending a two item array to the Plugin's output array (```myPluginInstance.output```). The first item in the array is the channel or DM ID and the second is the message text. Example that writes "hello world" when the plugin is started:

    class myPlugin(Plugin):

        def process_message(self, data):
            self.outputs.append(["C12345667", "hello world"])

##### SlackClient Web API Output
Plugins also have access to the connected SlackClient instance for more complex output (or to fetch data you may need).

    def process_message(self, data):
        self.slack_client.api_call(
            "chat.postMessage", channel="#general", text="Hello from Python! :tada:",
            username="pybot", icon_emoji=":robot_face:"


#### Timed jobs
Plugins can also run methods on a schedule. This allows a plugin to poll for updates or perform housekeeping during its lifetime. Jobs define a run() method and return any outputs to be sent to channels. They also have access to a SlackClient instance that allows them to make calls to the Slack Web API.

For example, this will print "hello world" every 10 seconds. You can output multiple messages two the same or different channels by passing multiple pairs of [Channel, Message] combos.

    from core import Plugin, Job


    class myJob(Job):

        def run(self, slack_client):
            return [["C12345667", "hello world"]]


    class myPlugin(Plugin):

        def register_jobs(self):
            job = myJob(10, debug=True)
            self.jobs.append(job)


#### Plugin misc
The data within a plugin persists for the life of the rtmbot process. If you need persistent data, you should use something like sqlite or the python pickle libraries.
