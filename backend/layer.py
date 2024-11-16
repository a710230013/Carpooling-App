import json

riders = []
drivers = []
drv_by_time = []
layer_stack = []

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

# disect the dataset into layers, create layers based on start times, current layer time = 10mins
def create_layers():
    layer_stack =[] #only stores ids of drivers and riders in the given layer
    for i in range(0, 2400, 20): 
        layer = [[],[]]
        for d in drivers:
            if i <= get_time(d) < i + 20:
                layer[0].append(d["user_id"])
        for r in riders:
            if i <= get_time(r) < i + 20:
                layer[1].append(r["user_id"])
        if layer[0] or layer[1]:
            layer_stack.append(layer)
    return layer_stack

layer_stack = create_layers()

print(layer_stack)
print(f"Number of layers: {len(layer_stack)}")
for i, layer in enumerate(layer_stack):
    print(f"Layer {i} (Driver) size: {len(layer[0])}, Layer {i} (Rider) size: {len(layer[1])}")

    
