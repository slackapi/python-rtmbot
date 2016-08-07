#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import os
import yaml
import client

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

# load args with config path
args = parse_args()
config = yaml.load(open(args.config or 'rtmbot.conf', 'r'))
bot = client.init(config)
try:
    bot.start()
except KeyboardInterrupt:
    sys.exit(0)
