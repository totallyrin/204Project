# file to store properties of different restaurants

# num of seats
from pprint import pprint

prompts_dict = {"Name of the Establishment >> ":str,
               "Number of Seats at Largest Table >> ":int,
               "Number of Stars in Rating >> ":int,
               "Number of Dollars of Cost >> ":int,
               "List of Dietary Restrictions Serviced:":[str],
               "Is the Establishment Fast Food? >> ":bool,
               "List of Seating Options ('indoor', 'outdoor'):":[str],
               "List of Transit Options ('bike', 'vehicle'):":[str],
               "List of Dining Options ('takeout', 'eatin', 'delivery'):":[str],
               #hours needs to be last to get special treatment
               "Dict of Hours of Operation {day_index:[open_float,close_float]}":dict}


''' not bad, but the convenience of not needing special characters
      is heavily outweighed by no longer being able to copy Mon hours

               "Dict of Hours of Operation {day_index:[open_float,close_float]}":{
                   "Monday":float,
                   "Tuesday":float,
                   "Wednesday":float,
                   "Thursday":float,
                   "Friday":float,
                   "Saturday":float,
                   "Sunday":float}}
'''


restaurants_dict = {
    "McDonald's":[2, 3, 1, ["veg", "gluten"], True, ["indoor"], ["bike"]
     , ["takeout", "eatin", "delivery"], {0:[6,22]}],
        #they're actually only 6-22 inside, 24h drivethru
    "Lone Star":[8, 4, 2, ["gluten"], False, ["indoor"], ["bike", "vehicle"]
     , ["takeout", "eatin", "delivery"],{0:[11, 22], 4:[11, 23], 5:[11, 23]}],
    "Tommy's":[4, 4, 1, ["gluten"], True, ["indoor", "outdoor"], ["bike", "vehicle"]
     , ["takeout", "eatin", "delivery"], {0:[0, 2, 8]}]
}

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
        default is that businesses are not open after midnight
        if it is open, then add an extra 0 to flip.

        because leading 0 and trailing 24 can be omitted,
        if even list index then times following that time are open hours
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

def restrict_input_type(prompt, input_type):

    '''
        prompt is a text prompt that is provided in input
        
        input_type can be a type singleton,
          or a dict or list of singletons
          
        if so, the dict can take strings as individual prompts
          and the list will not contain prompts
        note that dict is to allow unique prompts, and so is
          inherently a null-term input list, and so expect to
          use singletons for values.
        

    '''
    if type(input_type) is dict:
        print(prompt)
        output_list = []
        for k in input_type:
            output_per_type = []
            while True:
                temp = restrict_input_type(k + str(" >> "), input_type[k])
                if temp is not None: #stop adding if empty input
                    output_per_type += [temp]
                else:
                    break
            output_list += [output_per_type]
        
        #print(output_list) #but also do want to separate diff lists
        #if only one element in list then don't need extra wrapping list
        return output_list[0] if len(output_list) == 1 else output_list
    elif type(input_type) is list: # converts to dict, assumes prompt works for all
        #needs a unique index or else dict overwrites. ALSO NEEDS A RETURN STATEMENT ARGHHHHHH
        return restrict_input_type(prompt, {(str(i)):input_type[i] for i in range(len(input_type))})
    else:
        while True:
            temp = input(prompt) #eval doesn't like EOFs, so need protection
            #if '' then None, else don't eval/keep str if str expected
            temp = None if not temp else temp if input_type is str else eval(temp)
            if type(temp) is input_type:
                return temp
            elif temp is None: #breaks multi-input as needed
                return None
            elif input_type is float and type(temp) is int:
                return float(temp)
            # else continue
            print("uhoh! that didn't match the type", input_type)

def split_input_type_dict(type_dict):
    '''uses dict structure to pass prompt string as well'''
    inputs = []
    for k in type_dict:
        inputs += [restrict_input_type(k, type_dict[k])]
    return inputs

        
def define_restaurant(restaurants = restaurants_dict, prompts = prompts_dict):


    #'''need to append/overwrite if already existing'''
    print("When a property can take multiple entries, an empty line terminates.")
    restaurant = split_input_type_dict(prompts)
    
    if restaurant[0] in restaurants:
        k = restaurant[0]
        p = restaurant[1:]
        for i in range(len(p)):
            #if bool(p[i]) is False:
            if type(p[i]) is dict:
                for j in p[i]:
                    #r_dict[name] > v_list[index] > old_h_dict[key]
                    # = i_list[index] > new_h_dict[key]
                    restaurants[k][i][j] = p[i][j]
            #pass through set to remove repeats, doesn't remove values
            elif type(p[i]) is list:
                restaurants[k][i] = list(set(restaurants[k][i] + p[i]))
            #replaces current value unless is None entry
            elif p[i] is not None:
                restaurants[k][i] = p[i]
            #None entry, prompts whether simply no new value or want to erase.
            else: 
                restaurants[k][i] = None if input(
                    "Enter '' to preserve current value "
                    + str(restaurants[k][i]) + " >> ") else restaurants[k][i]
                    
    else:
        restaurants[restaurant[0]] = restaurant[1:]
    return restaurants


def convert_properties(restaurants = restaurants_dict):

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
             6:{}}

    properties = [seats, rating, price, dietary, fastFood, seating, parking, service, hours]
    
    for r in restaurants:
        r_props = restaurants[r]
        for prop in range(len(properties) - 1): # reduce by one so hours is not handled
            # handles all eles in list, does not make key from list
            if type(r_props[prop]) is list: 
                for list_trawl in r_props[prop]:
                    add_element(properties[prop], list_trawl, r)
            else: #else ok
                add_element(properties[prop], r_props[prop], r)
        days_dict = decode_hours(r_props[-1]) #do hours separately because it's special
        for day in range(7): # days per week
            hours_list = fill_in_hours(days_dict[day])
            for half_hour_index in range(48):
                half_hour = half_hour_index / 2
                if hours_list[half_hour_index]:
                    add_element(hours[day], half_hour, r)
            
    return properties


if __name__ == "__main__":
    #pprint(convert_properties(restaurantsDict))
    conved = convert_properties()
