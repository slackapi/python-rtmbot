import time
crontable = []
outputs = []

def process_message(data):
    if data['channel'].startswith("D"):
        outputs.append([data['channel'], "from repeat1 \"{}\" in channel {}".format(data['text'], data['channel']) ])

