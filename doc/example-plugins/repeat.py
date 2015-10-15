import time
crontable = []
outputs = []

def process_message(data):
    if data['channel'].startswith("D") and 'text' in data:
        outputs.append([data['channel'], "from repeat1 \"{t}\" in channel {c}".format(t=data['text'], c=data['channel'])])
