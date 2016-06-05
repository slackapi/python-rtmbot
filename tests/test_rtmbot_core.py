# -*- coding: utf-8 -*-
try:
    from unittest.mock import Mock, create_autospec
except ImportError:
    from mock import Mock, create_autospec

from testfixtures import LogCapture
from slackclient import SlackClient, _channel, _server, _util
from rtmbot.core import RtmBot, Plugin

def init_rtmbot():
    ''' Initializes an instance of RTMBot with some default values '''
    rtmbot = RtmBot({
        'SLACK_TOKEN': 'test-12345',
        'BASE_PATH': '/tmp/',
        'LOGFILE': '/tmp/rtmbot.log',
        'DEBUG': True
    })
    return rtmbot

def test_init():
    with LogCapture() as l:
        rtmbot = init_rtmbot()

    assert rtmbot.token == 'test-12345'
    assert rtmbot.directory == '/tmp/'
    assert rtmbot.debug == True

    l.check(
        ('root', 'INFO', 'Initialized in: /tmp/')
    )

def test_output():
    ''' Test that sending a message behaves as expected '''
    rtmbot = init_rtmbot()

    # Mock the slack_client object with Server, Channel objects and needed methods
    slackclient_mock = create_autospec(SlackClient)
    server_mock = create_autospec(_server.Server)

    # Mock Server with channels method and correct return value
    slackclient_mock.server = server_mock
    searchlist_mock = create_autospec(_util.SearchList)
    server_mock.channels = searchlist_mock
    channel_mock = create_autospec(_channel.Channel)
    slackclient_mock.server.channels.find.return_value = channel_mock

    rtmbot.slack_client = slackclient_mock

    # mock the plugin object to return a sample response
    plugin_mock = create_autospec(Plugin)
    plugin_mock.do_output.return_value = [['C12345678', 'test message']]
    rtmbot.bot_plugins.append(plugin_mock)

    rtmbot.output()


    # test that the output matches the expected value
    channel_mock.send_message.assert_called_with('test message')

    # test that emoji messages work as expected
    channel_mock.reset_mock()
    plugin_mock.reset_mock()
    plugin_mock.do_output.return_value = [['C12345678', '🚀 testing']]
    rtmbot.output()

    channel_mock.send_message.assert_called_with('🚀 testing')

    # test that unicode messages work as expected
    channel_mock.reset_mock()
    plugin_mock.reset_mock()
    plugin_mock.do_output.return_value = [['C12345678', 'ù hœø3ö']]
    rtmbot.output()

    channel_mock.send_message.assert_called_with('ù hœø3ö')