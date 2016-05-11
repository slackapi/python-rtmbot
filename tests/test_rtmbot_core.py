from testfixtures import LogCapture
from rtmbot.core import RtmBot


def test_init():
    with LogCapture() as l:
        rtmbot = RtmBot({
            'SLACK_TOKEN': 'test-12345',
            'BASE_PATH': '/tmp/',
            'LOGFILE': '/tmp/rtmbot.log',
            'DEBUG': True
        })

    assert rtmbot.token == 'test-12345'
    assert rtmbot.directory == '/tmp/'
    assert rtmbot.debug == True

    l.check(
        ('root', 'INFO', 'Initialized in: /tmp/')
    )
