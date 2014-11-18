import time
crontable = []
outputs = []

#crontable.append([.5,"add_number"])
crontable.append([5,"say_time"])

def say_time():
    outputs.append(["D030GJLM2", time.time()])
