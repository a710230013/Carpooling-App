import json

riders = []
drivers = []
drv_by_time = []


def get_time(u):
    # need to do this, otherwise "17:35" comes before "2:10"
    timestr = u["time_of_travel"].split(":")
    time = int(timestr[0]) * 100 + int(timestr[1])
    return time

# gets list of drivers ordered by start time
with open('backend/driver_data.json') as f:
    drivers = sorted(json.load(f)["Data"], key=get_time)

# gets list of riders ordered by start time
with open('backend/rider_data.json') as f:
    riders = sorted(json.load(f)["Data"], key=get_time)


for d in drivers:
    print(d["name"], d["time_of_travel"])
    
