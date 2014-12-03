#!/usr/bin/python

import sys
sys.dont_write_bytecode = True

import glob
import yaml
import json
import os
import sys
import time

from slackclient import SlackClient

def dbg(debug_string):
    if debug:
        print debug_string

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
            self.crons()
            self.output()
            time.sleep(.1)
    def input(self, data):
        if "type" in data:
            function_name = "process_" + data["type"]
            dbg("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.do(function_name, data)
    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel != None and output[1] != None:
                    if limiter == True:
                        time.sleep(1)
                        limiter = False
                    channel.send_message("{}".format(output[1]))
                    limiter = True
                else:
                    raise UnknownChannel
    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
    def load_plugins(self):
        path = os.path.dirname(sys.argv[0])
        for plugin in glob.glob(path+'/plugins/*'):
            sys.path.insert(0, plugin)
            sys.path.insert(0, path+'/plugins/')
        for plugin in glob.glob(path+'/plugins/*.py') + glob.glob(path+'/plugins/*/*.py'):
            print plugin
            name = plugin.split('/')[-1][:-2]
#            try:
            self.bot_plugins.append(Plugin(name))
#            except:
#                print "error loading plugin %s" % name

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
        else:
            self.module.crontable = []
    def do(self, function_name, data):
        if function_name in dir(self.module):
            #this makes the plugin fail with stack trace in debug mode
            if not debug:
                try:
                    eval("self.module."+function_name)(data)
                except:
                    dbg("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module."+function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                dbg("problem in catch all")
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
            else:
                self.module.outputs = []
        return output

class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0
    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)
    def __repr__(self):
        return self.__str__()
    def check(self):
        if self.lastrun + self.interval < time.time():
            if not debug:
                try:
                    self.function()
                except:
                    dbg("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass

class UnknownChannel(Exception):
    pass


if __name__ == "__main__":
    config = yaml.load(file('rtmbot.conf', 'r'))
    debug = config["DEBUG"]
    bot = RtmBot(config["SLACK_TOKEN"])
    bot.start()

