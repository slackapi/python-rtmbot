#!/usr/bin/python

import glob
import yaml
import json
import os
import sys
import time

from slackclient import SlackClient

class RtmBot(object):
    def __init__(self, token):
        self.token = token
        self.bot_plugins = []
        self.slack_client = None
    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client = SlackClient(self.token)
        self.slack_client.connect()
    def start(self):
        self.connect()
        self.load_plugins()
        while True:
            for reply in self.slack_client.read():
                self.input(reply)
                #print self.bot_plugins
            self.crons()
            self.output()
            time.sleep(.1)
    def input(self, data):
        if "type" in data:
            function_name = "process_" + data["type"]
            for plugin in self.bot_plugins:
                plugin.do(function_name, data)
    def output(self):
        for plugin in self.bot_plugins:
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                channel.send_message("%s" % output[1])
            #plugin.do_output()
            pass
            #print self.bot_plugins[plugin].replies()
    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
            pass
                #print job
    def load_plugins(self):
        path = os.path.dirname(sys.argv[0])
        sys.path.insert(0, path + "/plugins")
        for plugin in glob.glob(path+'/plugins/*.py'):
            name = plugin.split('/')[-1].rstrip('.py')
#            try:
            self.bot_plugins.append(Plugin(name))
#            except:
#                print "error loading plugins"

class Plugin(object):
    def __init__(self, name):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module."+function)))
            print self.module.crontable
    def do(self, function_name, data):
        if function_name in dir(self.module):
            eval("self.module."+function_name)(data)
    def do_jobs(self):
        for job in self.jobs:
            job.check()
    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    output.append(self.module.outputs.pop(0))
                else:
                    break
        return output

class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0
    def __str__(self):
        return "%s %s %s" % (self.function, self.interval, self.lastrun)
    def __repr__(self):
        return self.__str__()
    def check(self):
        if self.lastrun + self.interval < time.time():
            self.function()
            self.lastrun = time.time()
            pass


if __name__ == "__main__":
    proc = {k[8:]: v for k, v in globals().items() if k.startswith("process_")}
    config = yaml.load(file('rtmbot.conf', 'r'))

    bot = RtmBot(config["SLACK_TOKEN"])
    bot.start()

