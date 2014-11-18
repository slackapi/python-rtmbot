import time
crontable = []
outputs = []

def process_message(data):
    print data
    if data['channel'].startswith("D"):
        outputs.append([data['channel'], "from repeat1: " + data['text']])

