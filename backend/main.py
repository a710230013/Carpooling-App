import json
import math
from layer import create_layers

riders = []
drivers = []
# drv_by_time = []

driver_dict = {}
rider_dict = {}

ret_drivers = {}

def get_rider(rider_id):
    return [r for r in riders if r["user_id"] == rider_id][0]

def get_driver(driver_id):
    return [d for d in drivers if d["user_id"] == driver_id][0]

def get_layer_est(dist):
    if dist > 80:
        return int(dist // 33)
    else:
        return int(dist // 20)

def get_distance(p1, p2):
    dist_deg = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return dist_deg * 111


def get_locations(r):
    s = [float(loc) for loc in r["start_location"].split(",")]
    e = [float(loc) for loc in r["destination_location"].split(",")]
    return [s, e]


# def get_new_ride_info(points, ):
# def best_path(d, riders):
#     d



def add_ride(r, d, cur_layer):
    r_s, r_e = get_locations(r)
    d_s, d_e = get_locations(d)

    r_lay = get_layer_est(get_distance(r_s, r_e))
    
    dict_entry = driver_dict[d["user_id"]]
    pos = [[dict_entry[0][0], dict_entry[0][1], d["user_id"], d_s]]
    for i in range(len(dict_entry)):
        e = dict_entry[i]
        if len(e) == 3:
            # print(dict_entry, i)
            a, b = get_locations(get_rider(e[2]))
            if dict_entry[i][0] < dict_entry[i-1][0]:
                pos.append([e[0], e[1], e[2], a])
            else:
                pos.append([e[0], e[1], e[2], b])
    
    pos.append([dict_entry[-1][0], dict_entry[-1][1], d["user_id"], d_e])
    # print(pos)
    
    people = int(r["no_of_persons"])
    ind = [0, len(pos) + 1]
    for i in range(len(pos)):
        if pos[i][1] > cur_layer:
            pos.insert(i, [pos[i-1][0] - people, cur_layer, r["user_id"], r_s])
            ind[0] = i
            break
    
    
    set = 0
    for i in range(ind[0] + 1, len(pos)):
        if pos[i][1] >= cur_layer + r_lay:
            pos.insert(i, [pos[i-1][0] + people, (cur_layer + r_lay), r["user_id"], r_e])
            ind[1] = i
            set = 1
            break
    
    if not set:
        pos.insert(len(pos) - 1, [pos[i-1][0] + people, (cur_layer + r_lay), r["user_id"], r_e])
    
    for i in range(ind[0], ind[1]):
        pos[i][0] -= people



    new_detour = -get_distance(d_s, d_e)
    for i in range(1, len(pos)):
        new_detour  += (get_distance(pos[i][3], pos[i-1][3]))
        # print(new_detour)
        if new_detour > int(d["max_detour_distance"]):
            return 1
    
    total_layers = dict_entry[0][1]
    insert = []
    for i in range(len(pos)):
        if i > 0:
            total_layers += get_layer_est(get_distance(pos[i][3], pos[i-1][3]))
        insert.append([pos[i][0], total_layers, pos[i][2]])
    
    insert[0].pop()
    insert[-1].pop()

    for i in insert:
        if i[0] < 0:
            return 1


    # for i in range(len(pos - 1)):
        # insert.append([get_layer_est(get_distance(3, r_s)])
    # leg1 = get_layer_est(get_distance(d_s, r_s))
    # leg2 = get_layer_est(get_distance(r_s, r_e))
    # leg3 = get_layer_est(get_distance(r_e, d_e))
    


    # leg1 += dict_entry[0][1]
    # print(dict_entry, leg1, leg2, leg3, people)
    # dict_entry[-1][1] = leg1 + leg2 + leg3
    # i = 0
    # insert = [[leg1, people, r["user_id"]], [leg1 + leg2, -people, r["user_id"]]]
    # print("RIDER ADDED\n", d["name"], dict_entry, "\n", insert)
    # new_dict_entry = []

    # while i < len(dict_entry) and len(insert) > 0:
    #     if insert[0][0] < dict_entry[i][1] and dict_entry[i-1][0] >= insert[0][1]:
    #         print(i)
    #         dict_entry.insert(i, [dict_entry[i-1][0] - insert[0][1], insert[0][0], insert[0][2]])
    #         insert.pop(0)
    #     i += 1
    # if (len(insert) == 1):
    #     dict_entry.insert(-1, [dict_entry[-2][0] - insert[0][1], insert[0][0], insert[0][2]])
    
    driver_dict[d["user_id"]] = insert
    # print("DIC: ", insert)
    if d["user_id"] not in ret_drivers:
        ret_drivers[d["user_id"]] = [d, []]
    ret_drivers[d["user_id"]][1].append(r["user_id"])
    return 0



    # LATER: if more than one rider, find optimal configuration


def get_time(u):
    # need to do this, otherwise "17:35" comes before "2:10"
    timestr = u["time_of_travel"].split(":")
    time = int(timestr[0]) * 100 + int(timestr[1])
    return time

# gets list of drivers ordered by start time
with open('backend/driver_data.json') as f:
    # ld = json.load(f)["Data"]
    drivers = sorted(json.load(f)["Data"], key=get_time)
    # rng = [g for g in range(len(drivers))]
    # driver_dict = dict(zip(ld[rng]["user_id"], ld[rng]))

# gets list of riders ordered by start time
with open('backend/rider_data.json') as f:
    riders = [r for r in (sorted(json.load(f)["Data"], key=get_time)) if r["start_location"] != r["destination_location"]]


# i = 0
# for r in riders:
#     if r["start_location"] == r["destination_location"]:
#         print(r["name"], r["user_id"], r["start_location"], r["destination_location"])
#         i += 1
# print(i)
layers = create_layers(drivers, riders)
driver_ids = []
rider_ids = []

# rider dict (rider_id: [[driver ids, detour, max_detour, seats, urgency, carbon]])
# driver dict (driver_id: [[available seats, time of update, rid], []])
# start with [[avail, layer count], [0, layer count + est_dist]]
def score(d):
    s = 1/d[1] * 20
    s += 1/d[2] * 5
    s += d[3] * 0.5
    s += d[4] // 200
    return 1 - s




def calc():
    layer_count = 0
    for driver_ids_new, rider_ids_new in layers:
        # print("adding:", len(rider_ids_new))
        # if layer_count == 10:
        #     break
        layer_count += 1
        # get_time = 1
        driver_ids.extend(driver_ids_new)
        rider_ids.extend(rider_ids_new)
        drivers_to_delete = []
        for dv in driver_dict:
            if driver_dict[dv][-1][1] == layer_count:
                drivers_to_delete.append(dv)
                # print("driver arrived")
        for dvs in drivers_to_delete:
            del driver_dict[dvs]
            # if len(driver_dict[dv]) > 1:
            #     for c in range(1, len(driver_dict[dv])):
            #         if c >= len(driver_dict[dv]):
            #             break
            #         if driver_dict[dv][c][1] == layer_count:
            #             driver_dict[dv][0][0] += driver_dict[dv][c][0]
            #             driver_dict[dv].pop(c)

        for rid in rider_ids:
            if rid not in rider_dict:
                rider_dict[rid] = []
            r = get_rider(rid)
            # if get_time:
            #     print(f"\nTIME START FOR LAYER {layer_count}: ", r["time_of_travel"])
            #     get_time = 0
            num_riders = int(r["no_of_persons"])
            start_r_loc, end_r_loc = get_locations(r)# = [float(loc) for loc in r["start_location"].split(",")]
            # end_r_loc = [float(loc) for loc in r["destination_location"].split(",")]
            dist_rider = get_distance(start_r_loc, end_r_loc)
            
            # print(r["name"], start_r_loc, end_r_loc, dist_rider, num_riders, len(driver_ids), rider_dict[rid])
            ride_est = get_layer_est(dist_rider)
            for did in driver_ids:
                # driver_dict.update()
                # print("DIDS", len(driver_ids))

                d = get_driver(did)

                start_d_loc = [float(loc) for loc in d["start_location"].split(",")]
                end_d_loc = [float(loc) for loc in d["destination_location"].split(",")]
                dist_driver = get_distance(start_d_loc, end_d_loc)
                driv_est = get_layer_est(dist_driver)

                if did not in driver_dict:
                    avail_seats = int(d["no_free_seats"])
                    driver_dict[did] = [[]]
                    driver_dict[did][0] = ([avail_seats, layer_count])
                    driver_dict[did].append([0, layer_count + driv_est])
                    # print(d["name"])
                else:
                    # print("DDDDD", did, driver_dict[did])
                    avail_seats = driver_dict[did][0][0]

                # check if seats available
                if num_riders > avail_seats:
                    continue

                # check if detour is small enough
                max_detour = float(d["max_detour_distance"])
                dist_dr_start = get_distance(start_r_loc, start_d_loc)
                dist_dr_end = get_distance(end_r_loc, end_d_loc)
                total_dist = dist_rider + dist_dr_start + dist_dr_end
                detour = total_dist - dist_driver
                # print(r["name"], start_r_loc, end_r_loc, start_d_loc, end_d_loc, dist_rider, dist_dr_start, dist_dr_end)
                # print(dist_rider, dist_dr_start, dist_dr_end, dist_driver)
                # print(total_dist, dist_driver, detour, max_detour)

                # check if gender preferences match
                if (r["same_gender"] == "TRUE" or d["same_gender"] == "TRUE") and (r["gender"] != d["gender"]):
                        continue
                
                # check if smoking preferences match
                if r["non_smoking"] != d["non_smoking"]:
                        continue

                if (detour <= max_detour):
                    rdic = rider_dict[rid]
                    #d.consumption
                    cons = 250 #c/km
                    rdic.append([did, int(d["max_detour_distance"]), int(d["no_free_seats"]), 1, cons])
                    rdic.sort(key=score)
                    rider_dict[rid] = rdic
                    # if d["name"] == "Barbara Gross":
                    # print("GOOD: ", d["name"], start_d_loc, end_d_loc, num_riders, rider_dict[rid], driver_dict[did])
                    # print("GOOD: ", d["name"], start_d_loc, end_d_loc, dist_driver, detour, max_detour, avail_seats, (avail_seats - num_riders))
                    # driver_dict[did].append(rid)
            
            if len(rider_dict[rid]) == 1:
                drid = rider_dict[rid][0][0]
                
                # print("Adding Rider")
                if (add_ride(get_rider(rid), get_driver(drid), layer_count) == 0):
                    rider_ids.remove(rid)
                    # driver_ids.remove(did)
                    for rd in rider_dict:
                        if drid in rider_dict[rd]:
                            rider_dict[rd].remove(drid)
                    # if drid == "470d083d-8185-4222-bf1d-3f33af261385":
                    #     print("BARBARA")
                    # driver_dict[drid].append([num_riders, layer_count + ride_est, ])
                    # driver_dict[drid][0][0] -= num_riders
                    # print(r["name"], "with", drid, driver_dict[drid])
                    # dict.update(driver_dict)
                    del rider_dict[rid]
                # else:
                    # print("ERROR: rider could not be added")
            elif len(rider_dict) > 1:
                for i in range(len(rider_dict[rid])):
                    drid = rider_dict[rid][i][0]
                    if (add_ride(get_rider(rid), get_driver(drid), layer_count) == 0):
                        rider_ids.remove(rid)
                    # driver_ids.remove(did)
                    for rd in rider_dict:
                        if drid in rider_dict[rd]:
                            rider_dict[rd].remove(drid)
                    # print(r["name"], "with", drid, driver_dict[drid])
                    # dict.update(driver_dict)
                    del rider_dict[rid]
                    break
                    
        
        
        print("leftover:", len(rider_ids))
            
    return ret_drivers

print(calc())

