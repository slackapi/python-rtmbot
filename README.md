python-rtmbot
=============
A Slack bot written in python that connects via the RTM API.

Python-rtmbot is a callback based bot engine. The plugins architecture should be familiar to anyone with knowledge to the [Slack API](https://api.slack.com) and Python. The configuration file format is YAML.

Dependencies
----------
* websocket-client https://pypi.python.org/pypi/websocket-client/
* python-slackclient https://github.com/slackhq/python-slackclient

Installation
-----------

1. Download and install the python-slackclient and websocket-client libraries

        git clone https://github.com/liris/websocket-client.git
        cd websocket-client
        sudo python setup.py install
        cd ..
        git clone git@github.com:slackhq/python-slackclient.git
        cd python-slackclient
        sudo python setup.py install
        cd ..

2. Download the python-rtmbot code

        git clone git@github.com:slackhq/python-rtmbot.git
        cd python-rtmbot


3. Configure rtmbot
        
        cp doc/example-config/rtmbot.conf .
        vi rtmbot.conf
          SLACK_TOKEN: "xoxb-11111111111-222222222222222"

*Note*: At this point rtmbot is ready to run, however no plugins are configured.

Plugins
-------

Each plugin should create a directory under ```plugins/``` with .py files for the code you would like to load. libraries can be kept in a subdirectory.

To install the example 'repeat' plugin

    mkdir plugins/repeat
    cp doc/example-plugins/repeat.py plugins/repeat

The repeat plugin will now be loaded by the bot on startup.

    ./rtmbot.py
