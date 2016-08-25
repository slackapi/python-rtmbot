python-rtmbot
=============

[![Build Status](https://travis-ci.org/slackhq/python-rtmbot.png)](https://travis-ci.org/slackhq/python-rtmbot)
[![Coverage Status](https://coveralls.io/repos/github/slackhq/python-rtmbot/badge.svg?branch=master)](https://coveralls.io/github/slackhq/python-rtmbot?branch=master)

A Slack bot written in Python that connects via the RTM API.

Python-rtmbot is a bot engine. The plugins architecture should be familiar to anyone with knowledge to the [Slack API](https://api.slack.com) and Python. The configuration file format is YAML.

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

2. Install rtmbot (ideally into a virtualenv https://virtualenv.readthedocs.io/en/latest/)

        pip install rtmbot

3. Create conf file and configure rtmbot (https://api.slack.com/bot-users)

        vi rtmbot.conf

            DEBUG: True # make this False in production
            SLACK_TOKEN: "xoxb-11111111111-222222222222222"
            ACTIVE_PLUGINS:
                - plugins.repeat.RepeatPlugin
                - plugins.test.TestPlugin

```DEBUG``` will adjust logging verbosity and cause the runner to exit on exceptions, generally making dubugging more pleasant.

```SLACK_TOKEN``` is needed to authenticate with your Slack team. More info at https://api.slack.com/web#authentication

```ACTIVE_PLUGINS``` RTMBot will attempt to import any Plugin specified in `ACTIVE_PLUGINS` (relative to your python path) and instantiate them as plugins. These specified classes should inherit from the core Plugin class.

For example, if your python path includes '/path/to/myproject' and you include `plugins.repeat.RepeatPlugin` in ACTIVE_PLUGINS, it will find the RepeatPlugin class within /path/to/myproject/plugins/repeat.py and instantiate it then attach it to your running RTMBot.

A Word on Structure
-------
To give you a quick sense of how this library is structured, there is a RtmBot class which does the setup and handles input and outputs of messages. It will also search for and register Plugins within the specified directory(ies). These Plugins handle different message types with various methods and can also register periodic Jobs which will be executed by the Plugins.
```
RtmBot
|--> Plugin
       |---> Job
       |---> Job
|--> Plugin
|--> Plugin
       |---> Job
```

Add Plugins
-------

To add a plugin, create a file within your plugin directory (./plugins is a good place for it).

    cd plugins
    vi myplugin.py

Add your plugin content into this file. Here's an example that will just print all of the requests it receives. See below for more information on available methods.

    from future import print_function
    from rtmbot.core import Plugin

    class MyPlugin(Plugin):

        def catch_all(self, data):
            print(data)

You can install as many plugins as you like, and each will handle every event received by the bot indepentently.

To install the example 'repeat' plugin

    mkdir plugins/
    cp docs/example-plugins/repeat.py plugins/repeat.py

The repeat plugin will now be loaded by the bot on startup.

    ./rtmbot.py

Create Plugins
--------

####Incoming data
All events from the RTM websocket are sent to the registered plugins. To act on an event, create a function definition called process_(api_method) that accepts a single arg. For example, to handle incoming messages:

    def process_message(self, data):
        print data

This will print the incoming message json (dict) to the screen where the bot is running.

Plugins having a method defined as ```catch_all(data)``` will receive ALL events from the websocket. This is useful for learning the names of events and debugging.

For a list of all possible API Methods, look here: https://api.slack.com/rtm

Note: If you're using Python 2.x, the incoming data should be a unicode string, be careful you don't coerce it into a normal str object as it will cause errors on output. You can add `from __future__ import unicode_literals` to your plugin file to avoid this.

####Outgoing data

#####RTM Output
Plugins can send messages back to any channel or direct message. This is done by appending a two item array to the Plugin's output array (```myPluginInstance.output```). The first item in the array is the channel or DM ID and the second is the message text. Example that writes "hello world" when the plugin is started:

    class myPlugin(Plugin):

        def process_message(self, data):
            self.outputs.append(["C12345667", "hello world"])

#####SlackClient Web API Output
Plugins also have access to the connected SlackClient instance for more complex output (or to fetch data you may need).

    def process_message(self, data):
        self.slack_client.api_call(
            "chat.postMessage", channel="#general", text="Hello from Python! :tada:",
            username='pybot', icon_emoji=':robot_face:'


####Timed jobs
Plugins can also run methods on a schedule. This allows a plugin to poll for updates or perform housekeeping during its lifetime. This is done by appending a two item array to the crontable array. The first item is the interval in seconds and the second item is the method to run. For example, this will print "hello world" every 10 seconds.

    from core import Plugin, Job


    class myJob(Job):

        def say_hello(self):
            self.outputs.append(["C12345667", "hello world"])


    class myPlugin(Plugin):

        def register_jobs(self):
            job = myJob(10, 'say_hello', self.debug)
            self.jobs.append(job)


####Plugin misc
The data within a plugin persists for the life of the rtmbot process. If you need persistent data, you should use something like sqlite or the python pickle libraries.

####Direct API Calls
You can directly call the Slack web API in your plugins by including the following import:

    from client import slack_client

You can also rename the client on import so it can be easily referenced like shown below:

    from client import slack_client as sc

Direct API calls can be called in your plugins in the following form:
    
    sc.api_call("API.method", "parameters")

####Todo:
Some rtm data should be handled upstream, such as channel and user creation. These should create the proper objects on-the-fly.
