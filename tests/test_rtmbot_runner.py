import os

from contextlib import contextmanager
from rtmbot.bin.run_rtmbot import load_overrides_from_env

@contextmanager
def override_env(env):
    _environ = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(env)
        yield
    finally:
        os.environ.clear()
        os.environ.update(_environ)

def test_normal_overrides():
    config = {
        'SLACK_TOKEN': 'xoxb-foo-bar',
        'BASE_PATH': os.getcwd(),
        'LOGFILE': 'foobar.log',
        'DEBUG': True,
        'DAEMON': True
    }

    override = {
        'SLACK_TOKEN': 'xoxb-this-should-change',
        'BASE_PATH': '/opt/nope',
        'LOGFILE': 'awesome.log',
        'DEBUG': 'false',
        'DAEMON': 'false'
    }

    with override_env(override):
        load_overrides_from_env(config)
        expected = {
            'SLACK_TOKEN': 'xoxb-this-should-change',
            'BASE_PATH': '/opt/nope',
            'LOGFILE': 'awesome.log',
            'DEBUG': False,
            'DAEMON': False
        }
        assert config == expected

def test_plugin_overrides():
    config = {
        'ACTIVE_PLUGINS': ['plugins.AwesomePlugin']}

    override = {
        'AWESOME_PLUGIN_FOO': '1',
        'AWESOME_PLUGIN_BAR_BAR': 'some_awesome_value'
    }

    with override_env(override):
        load_overrides_from_env(config)
        expected = {
            'foo': '1',
            'bar_bar': 'some_awesome_value'
        }
        assert config['plugins.AwesomePlugin'] == expected

def test_plugin_config_already_exists():
    config = {
        'ACTIVE_PLUGINS': ['plugins.AwesomePlugin'],
        'plugins.AwesomePlugin': {
            'some_credential': 'foo'
        }
    }

    override = {
        'AWESOME_PLUGIN_SOME_CREDENTIAL': 'bar'
    }

    with override_env(override):
        load_overrides_from_env(config)
        expected = {
            'some_credential': 'bar'
        }
        assert config['plugins.AwesomePlugin'] == expected
