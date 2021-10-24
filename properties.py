# file to store properties of different restaurants

# num of seats
seats = {}

# rating
rating = {}

# price ($, $$, $$$)
price = {}

# dietary considerations
dietary = {}

# 'fast-food' or not
fastFood = {}

# indoor/outdoor seating
seating = {}

# vehicular parking, bike rack
parking = {}

# take-out, eat in, delivery
service = {}

# open morning, afternoon, evenings, nights
hours = {}

restaurants = [
    ["McDonald's", 2, 3, "$", ["veg", "gluten"], True, ["indoor"], ["bike"], ["take-out", "eat-in", "delivery"], [6,
                                                                                                                  22]],
    ["Lone Star", 8, 4, "$$", ["gluten"], False, ["indoor"], ["bike", "vehicle"], ["take-out", "eat-in", "delivery"],
     [11, 22]],
    ["Tommy's", 4, 4, "$", ["gluten"], True, ["indoor", "outdoor"], ["bike", "vehicle"], ["take-out", "eat-in",
                                                                                          "delivery"], [8, 2]]
]

def getProperties():
    for restaurant in restaurants:

    return
