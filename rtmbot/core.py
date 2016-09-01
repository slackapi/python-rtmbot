#!/usr/bin/env python
from __future__ import unicode_literals
import sys
import glob
import os
import time
import logging

from slackclient import SlackClient

from utils.module_loading import import_string

sys.dont_write_bytecode = True


class RtmBot(object):
    def __init__(self, config):
        '''
            Params:
                - config (dict):
                    - SLACK_TOKEN: your authentication token from Slack
                    - BASE_PATH (optional: defaults to execution directory) RtmBot will
                        look in this directory for plugins.
                    - LOGFILE (optional: defaults to rtmbot.log) The filename for logs, will
                        be stored inside the BASE_PATH directory
                    - DEBUG (optional: defaults to False) with debug enabled, RtmBot will
                        break on errors
        '''
        # set the config object
        self.config = config

        # set slack token
        self.token = config.get('SLACK_TOKEN', None)
        # TODO: Raise an exception if no SLACK_TOKEN is specified

        # get list of directories to search for loading plugins
        self.active_plugins = config.get('ACTIVE_PLUGINS', None)

        # set base directory for logs and plugin search
        working_directory = os.path.abspath(os.path.dirname(sys.argv[0]))

        self.directory = self.config.get('BASE_PATH', working_directory)
        if not self.directory.startswith('/'):
            path = os.path.join(os.getcwd(), self.directory)
            self.directory = os.path.abspath(path)

        # establish logging
        log_file = config.get('LOGFILE', 'rtmbot.log')
        logging.basicConfig(filename=log_file,
                            level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logging.info('Initialized in: {}'.format(self.directory))
        self.debug = self.config.get('DEBUG', False)

        # initialize stateful fields
        self.last_ping = 0
        self.bot_plugins = []
        self.slack_client = SlackClient(self.token)

    def _dbg(self, debug_string):
        if self.debug:
            logging.info(debug_string)

    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client.rtm_connect()

    def _start(self):
        self.connect()
        self.load_plugins()
        while True:
            for reply in self.slack_client.rtm_read():
                self.input(reply) # <<<<------------------------
            self.crons()
            self.output()
            self.autoping()
            time.sleep(.1)

    def start(self):
        if 'DAEMON' in self.config:
            if self.config.get('DAEMON'):
                import daemon
                with daemon.DaemonContext():
                    self._start()
        self._start()

    def autoping(self):
        # hardcode the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.slack_client.server.ping()
            self.last_ping = now

    def input(self, data):
        if "type" in data:
            function_name = "process_" + data["type"]
            self._dbg("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)

    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel is not None and output[1] is not None:
                    if limiter:
                        time.sleep(.1)
                        limiter = False
                    channel.send_message(output[1])
                    limiter = True

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()

    def load_plugins(self):
        ''' Given a set of plugin_path strings (directory names on the python path),
        load any classes with Plugin in the name from any files within those dirs.
        '''
        self._dbg("Loading plugins")
        for plugin_path in self.active_plugins:
            self._dbg("Importing {}".format(plugin_path))

            if self.debug is True:
                # this makes the plugin fail with stack trace in debug mode
                cls = import_string(plugin_path)
            else:
                # otherwise we log the exception and carry on
                try:
                    cls = import_string(plugin_path)
                except ImportError:
                    logging.exception("Problem importing {}".format(plugin_path))

            plugin_config = self.config.get(cls.__name__, {})
            plugin = cls(slack_client=self.slack_client, plugin_config=plugin_config)  # instatiate!
            self.bot_plugins.append(plugin)
            self._dbg("Plugin registered: {}".format(plugin))


class Plugin(object):

    def __init__(self, name=None, slack_client=None, plugin_config=None):
        '''
        A plugin in initialized with:
            - name (str)
            - slack_client - a connected instance of SlackClient - can be used to make API
                calls within the plugins
            - plugin config (dict) - (from the yaml config)
                Values in config:
                - DEBUG (bool) - this will be overridden if debug is set in config for this plugin
        '''
        if name is None:
            self.name = type(self).__name__
        else:
            self.name = name
        if plugin_config is None:
            self.plugin_config = {}
        else:
            self.plugin_config = plugin_config
        self.slack_client = slack_client
        self.jobs = []
        self.debug = self.plugin_config.get('DEBUG', False)
        self.register_jobs()
        self.outputs = []

    def register_jobs(self):
        # if 'crontable' in dir(self.module):
        #     for interval, function in self.module.crontable:
        #         self.jobs.append(Job(interval, eval("self.module." + function), self.debug))
        #     logging.info(self.module.crontable)
        #     self.module.crontable = []
        # else:
        #     self.module.crontable = []
        pass

    def do(self, function_name, data):
        try:
            func = getattr(self, function_name)
        except AttributeError:
            pass
        else:
            if self.debug is True:
                # this makes the plugin fail with stack trace in debug mode
                func(data)
            else:
                # otherwise we log the exception and carry on
                try:
                    func(data)
                except Exception:
                    logging.exception("Problem in Plugin Class: {}: {} \n{}".format(
                        self.name, function_name, data)
                    )

        try:
            func = getattr(self, 'catch_all')
        except AttributeError:
            return
        else:
            if self.debug is True:
                # this makes the plugin fail with stack trace in debug mode
                self.catch_all(data)
            else:
                try:
                    self.catch_all(data)
                except Exception:
                    logging.exception("Problem in catch all: {}: {} {}".format(
                        self.name, self.module, data)
                    )

    def do_jobs(self):
        for job in self.jobs:
            job.check()

    def do_output(self):
        output = []
        while True:
            if len(self.outputs) > 0:
                logging.info("output from {}".format(self.name))
                output.append(self.outputs.pop(0))
            else:
                break
        return output


class Job(object):
    def __init__(self, interval, function, debug):
        self.function = function
        self.interval = interval
        self.lastrun = 0
        self.debug = debug

    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)

    def __repr__(self):
        return self.__str__()

    def check(self):
        if self.lastrun + self.interval < time.time():
            if self.debug is True:
                # this makes the plugin fail with stack trace in debug mode
                self.function()
            else:
                # otherwise we log the exception and carry on
                try:
                    self.function()
                except Exception:
                    logging.exception("Problem in job check: {}".format(self.function))
            self.lastrun = time.time()


class UnknownChannel(Exception):
    pass
