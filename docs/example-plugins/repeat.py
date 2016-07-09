from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return

crontable = []
outputs = []


def process_message(data):
    if data['channel'].startswith("D"):
        outputs.append([data['channel'], "from repeat1 \"{}\" in channel {}".format(
            data['text'], data['channel'])]
        )
