# file to store properties of different restaurants
from pprint import pprint


# function to add values to dictionary, create new keys if no pre-existing
def add_element(dic, key, val):
    if key in dic:
        dic[key].append(val)
    else:
        dic[key] = [val]
    return dic


# convert properties from restaurants list to a list of dictionaries of properties
def convert_properties():
    seats = {}  # num of seats
    rating = {}  # rating
    price = {}  # price ($, $$, $$$)
    dietary = {}  # dietary considerations
    fastFood = {}  # 'fast-food' or not
    seating = {}  # indoor/outdoor seating
    parking = {}  # vehicular parking, bike rack
    service = {}  # take-out, eat in, delivery
    hours = {}  # open morning, afternoon, evenings, nights

    properties = [seats, rating, price, dietary, fastFood, seating, parking, service, hours]

    for i in restaurants:
        for j in range(len(properties)):
            if type(i[j + 1]) is list:
                for k in i[j + 1]:
                    add_element(properties[j], k, i[0])
            else:
                add_element(properties[j], i[j + 1], i[0])
    return properties


# List of restaurants, format [name, #seats, rating, price, dietary, 'fast-food', seating, parking, service, hours]
restaurants = [
    ["McDonald's", 2, 3, "$", ["veg", "gluten"], True, ["indoor"], ["bike"], ["take-out", "eat-in", "delivery"], [6,
                                                                                                                  22]],
    ["Lone Star", 8, 4, "$$", ["gluten"], False, ["indoor"], ["bike", "vehicle"], ["take-out", "eat-in", "delivery"],
     [11, 22]],
    ["Tommy's", 4, 4, "$", ["gluten"], True, ["indoor", "outdoor"], ["bike", "vehicle"], ["take-out", "eat-in",
                                                                                          "delivery"], [8, 2]]
]

# test
if __name__ == "__main__":
    pprint(convert_properties())
