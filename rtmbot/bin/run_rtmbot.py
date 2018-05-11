#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import os
import yaml
import re

from rtmbot import RtmBot

sys.path.append(os.getcwd())


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


def prefix_from_plugin_name(name):
    basename = name.split('.')[-1]
    # Attribution: https://stackoverflow.com/a/1176023
    splitted = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', basename)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', splitted).upper() + '_'


def load_overrides_from_env(config):
    '''
    Read and apply overrides from environment variables. For plugins, name of the class
    is turned into a prefix. For example:
        YourAwesomePlugin.foo_bar => YOUR_AWESOME_PLUGIN_FOO_BAR
    '''
    def boolish(v):
        return v == '1' or v == 'true'  # bool('false') == True, so do it the hard way

    params = [
        {'name': 'SLACK_TOKEN', 'type': str},
        {'name': 'BASE_PATH', 'type': str},
        {'name': 'LOGFILE', 'type': str},
        {'name': 'DEBUG', 'type': boolish},
        {'name': 'DAEMON', 'type': boolish}
    ]

    # Override the rtmbot-specific variables. Here we can take advantage
    # of the fact that we know what type they are supposed to be in.
    config.update({
        param['name']: param['type'](os.environ[param['name']])
        for param in params
        if param['name'] in os.environ})

    # Override plugin-specific variables. Since we don't know a schema,
    # treat values as string. Leave type conversion for plugins themselves.
    for plugin in config.get('ACTIVE_PLUGINS', []):
        prefix = prefix_from_plugin_name(plugin)
        plugin_configs = [
            var for var in os.environ
            if var.startswith(prefix)]

        # Create if necessary
        if plugin not in config:
            config[plugin] = {}

        config[plugin].update({
            param.split(prefix)[-1].lower(): os.environ[param]
            for param in plugin_configs})


def main(args=None):
    # load args with config path if not specified
    if not args:
        args = parse_args()

    config = yaml.load(open(args.config or 'rtmbot.conf', 'r'))
    load_overrides_from_env(config)
    bot = RtmBot(config)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
