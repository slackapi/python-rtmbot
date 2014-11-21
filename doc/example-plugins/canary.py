import time
outputs = []

def canary():
    #NOTE: you must add a real channel ID for this to work
    outputs.append(["D12345678", "bot started: " + str(time.time())])

canary()
