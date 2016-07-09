from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return

import time
crontable = []
outputs = []

crontable.append([5, "say_time"])


def say_time():
    # NOTE: you must add a real channel ID for this to work
    outputs.append(["D12345678", time.time()])
