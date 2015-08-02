#!/usr/bin/env python
from argparse import ArgumentParser

import yaml
from rtmbot import RtmBot

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()

# load args with config path
args = parse_args()
config = yaml.load(file(args.config or 'rtmbot.conf', 'r'))
bot = RtmBot(config)
bot.start()
