import json
import math

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
    drivers = sorted(json.load(f)["Data"], key=get_time)[:10]

# gets list of riders ordered by start time
with open('backend/rider_data.json') as f:
    riders = sorted(json.load(f)["Data"], key=get_time)[:5]


for d in drivers:
    start_d_loc = d["start_location"].split(",")
    start_d_x = float(start_d_loc[0])
    start_d_y = float(start_d_loc[1])
    end_d_loc = d["destination_location"].split(",")
    end_d_x = float(end_d_loc[0])
    end_d_y = float(end_d_loc[1])
    for r in riders:
        start_r_loc = r["start_location"].split(",")
        start_r_x = float(start_r_loc[0])
        start_r_y = float(start_r_loc[1])
        end_r_loc = r["destination_location"].split(",")
        end_r_x = float(end_r_loc[0])
        end_r_y = float(end_r_loc[1])
        dist_rider = ((end_r_x - start_r_x) ** 2 + (end_r_y - start_r_y) ** 2)
        print(start_r_loc, start_r_x, start_r_y)
        # du_s = r[]
    print(d["name"], d["time_of_travel"])
    
