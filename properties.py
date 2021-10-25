# file to store properties of different restaurants

# num of seats
from pprint import pprint

def add_element(dic, key, val):
    if key in dic:
        dic[key].append(val)
    else:
        dic[key] = [val]
    return dic

def decode_hours(time_dict):
    '''
       so the system has to handle half-hours.
       don't really care about having too many data points in storage
       mostly worried about trawling through the relevant slots
        which have to be a list/keylist of some sort
       
       need to check for entire duration of use. do not forget.

       return a days list holding lists spanning half hours


       i changed my mind we use a dict for this too but gotta strip it
       dictionary with integer keys from 0 to 7.
    '''

    #might need input val here. TODO?

    length = len(time_dict)
    if length == 0:
        return None
    
    time_list = []
    first = next(iter(time_dict.values()))
    
    for i in range(7):
        time_list += [time_dict[i] if i in time_dict else first]

    return time_list


def fill_in_hours(hours_sh):
    '''
        from a shorthand list, generates full list of half hours
        from [0.0 to 24.0), where each half hour is a 0.5?
        not ideal but easier for math

        should assume that businesses are not open after midnight
        parity flipflop
        if is open, then add an extra 0 to flop

        because leading 0 and trailing 24 can be omitted,
        if even then times following that time are open hours
        if odd position then following times are closed
        

        returns the expanded list of True/False
        
    '''
    time_bools = []
    open_bool = False #default is starts closed at midnight
    for i in range(48):
        half_hour = i / 2 #hope this compiles to  i >> 1

        #flops if current time is in input list, else repeats prev
        open_bool = not open_bool if half_hour in hours_sh else open_bool
        time_bools.append(open_bool)

    return time_bools    
        
        

def convert_properties():

    seats = {}
    rating = {} # rating
    price = {} # price ($, $$, $$$)
    dietary = {} # dietary considerations
    fastFood = {} # 'fast-food' or not
    seating = {} # indoor/outdoor seating
    parking = {} # vehicular parking, bike rack
    service = {} # take-out, eat in, delivery
    hours = {0:{}, # one for each day of week
             1:{}, # True if open during that
             2:{}, #  half-hour, False if not
             3:{},
             4:{},
             5:{},
             6:{},}

    properties = [seats, rating, price, dietary, fastFood, seating, parking, service, hours]
    
    for restaurant in restaurants:
        for prop in range(len(properties) - 1): # reduce by one so hours is not handled
            # (prop + one) offsets as Name needs no property dict
            if type(restaurant[prop + 1]) is list: # handles all eles in list, does not make key from list
                for list_trawl in restaurant[prop + 1]:
                    add_element(properties[prop], list_trawl, restaurant[0])
            else: #else ok
                add_element(properties[prop], restaurant[prop + 1], restaurant[0])
        days_dict = decode_hours(restaurant[9]) #do hours separately because it's special
        for day in range(7): # days per week
            hours_list = fill_in_hours(days_dict[day])
            for half_hour_index in range(48):
                half_hour = half_hour_index / 2
                if hours_list[half_hour_index]:
                    add_element(hours[day], half_hour, restaurant[0])
                #add_element(hours[day], half_hour, [restaurant[0], hours_list[half_hour_index]])
            
    return properties

restaurants = [
    ["McDonald's", 2, 3, 1, ["veg", "gluten"], True, ["indoor"], ["bike"]
     , ["take-out", "eat-in", "delivery"], {0:[6,22]}],
    ["Lone Star", 8, 4, 2, ["gluten"], False, ["indoor"], ["bike", "vehicle"]
     , ["take-out", "eat-in", "delivery"],{0:[11, 22], 4:[11, 23], 5:[11, 23]}],
    ["Tommy's", 4, 4, 1, ["gluten"], True, ["indoor", "outdoor"], ["bike", "vehicle"]
     , ["take-out", "eat-in", "delivery"], {0:[0, 2, 8]}]
]


if __name__ == "__main__":
    pprint(convert_properties())
