from datetime import datetime
from pprint import pprint
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

import properties

# Encoding that will store all of your constraints
E = Encoding()


# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicProposition:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


'''
for i in range(10):
    exec('m' + str(i) + "=BasicProposition('m" + str(i) + "')")
    print(eval("m" + str(i)).__repr__)
'''

# Basic Propositions
ff = BasicProposition("Fast-food")

# Dietary restrictions
veg = BasicProposition("Vegetarian")
dairy = BasicProposition("Dairy-free")
gluten = BasicProposition("Gluten-free")
halal = BasicProposition("Halal")

# Seating location
indoor = BasicProposition("Indoor")
outdoor = BasicProposition("Outdoor")

# Parking
vehicle = BasicProposition("Vehicle")
bike = BasicProposition("Bike")


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html


@proposition(E)
class Rating:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


# Rating
r1 = Rating("1*")
r2 = Rating("2*")
r3 = Rating("3*")
r4 = Rating("4*")
r5 = Rating("5*")


@proposition(E)
class Price:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


# Price ($ or $$ or $$$ or $$$$)
p1 = Price("$")
p2 = Price("$$")
p3 = Price("$$$")
p4 = Price("$$$$")


@proposition(E)
class Weather:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


sunny = Weather("Sunny")
rain = Weather("Raining")
snow = Weather("Snowing")


@proposition(E)
class Service:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


# dine-in, take-out, delivery
eatin = Service("Eat-in")
takeout = Service("Take-out")
delivery = Service("Delivery")


@proposition(E)
class Day:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


mon = Day("Monday")
tue = Day("Tuesday")
wed = Day("Wednesday")
thu = Day("Thursday")
fri = Day("Friday")
sat = Day("Saturday")
sun = Day("Sunday")

days = [mon, tue, wed, thu, fri, sat, sun]


@proposition(E)
class Time:

    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            today = datetime.today()
            hour = today.hour + ((today.minute // 30) / 2)
            self.data = {today.weekday(): [hour, hour + 0.5]}

    def __repr__(self):
        return f"{self.data}"


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def solution():
    # TODO? code for loop to add constraints

    day = None

    if type(day) is int and day in range(7):
        E.add_constraint(days[day])
    else:  # add current day of week
        E.add_constraint(days[datetime.now().weekday()])

    # If a person is willing to eat at a badly-rated restaurant, they would be happy to eat at a well-rated restaurant
    # r1 >> r2 >> r3 >> r4 >> r5
    # constraint.add_implies_all(E, [r1], [r2, r3, r4, r5])
    # constraint.add_implies_all(E, [r2], [r3, r4, r5])
    # constraint.add_implies_all(E, [r3], [r4, r5])
    # constraint.add_implies_all(E, [r4], [r5])

    # If a person is willing to pay $$$, then they would be happy to pay $$ or $ also.
    # # p4 >> p3 >> p2 >> p1
    # constraint.add_implies_all(E, [p4], [p3, p2, p1])
    # constraint.add_implies_all(E, [p3], [p2, p1])
    # constraint.add_implies_all(E, [p2], [p1])

    constraint.add_exactly_one(E, Rating)  # a rating must exist
    constraint.add_exactly_one(E, Price)  # a price must exist
    constraint.add_exactly_one(E, Weather)  # weather must exist
    constraint.add_at_least_one(E, Service)  # service must exist

    E.add_constraint(ff >> takeout)  # 'fast food' restaurants have take-out
    E.add_constraint(eatin | takeout | delivery)
    E.add_constraint(eatin >> (indoor | outdoor))
    E.add_constraint((indoor | outdoor) >> eatin)
    E.add_constraint(((rain | snow) & eatin) >> indoor)

    E.add_constraint(dairy & takeout & p2 & r4)

    return E


def displaySolution():
    if not T.satisfiable():
        return
    result = []
    for key in sol.keys():
        if sol.get(key):  # create list of properties that fulfill all constraints
            result.append(key.__repr__())
    result.sort()
    return result


# trying to write a function to return corresponding restaurant
def getRestaurants():
    props = [0, 0, [], False, [], [], [], [], []]  # rating, price, dietary, fastFood, seating, parking, service, day,
    # hours
    if not T.satisfiable():
        return props

    dietary = ["Vegetarian", "Dairy-free", "Halal", "Gluten-free"]
    seating = ["Indoor", "Outdoor"]
    parking = ["Vehicle", "Bike"]
    service = ["Eat-in", "Take-out", "Delivery"]
    day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    converted = properties.convert_properties()  # get restaurants sorted by properties
    lis = displaySolution()  # get list of all True propositions (solution)
    # for loop to add True propositions to props list
    for element in lis:
        if '*' in element:
            props[0] = (int(element[0]))
        elif '$' in element:
            props[1] = (len(element))
        elif element in dietary:
            props[2].append(element.lower())
        elif element == "Fast-food" and props[3] is False:
            props[3] = True
        elif element in seating:
            props[4].append(element.lower())
        elif element in parking:
            props[5].append(element.lower())
        elif element in service:
            props[6].append(element.lower())
        # elif element in day:
        #     props[7] = day.index(element)
        #     # TODO write proper code to get correct required day and time

    pprint(props)

    restaurants = set()

    for item in converted[0]:
        if props[0] <= item:
            restaurants.update(set(converted[0][item]))

    temp = set()

    for item in converted[1]:
        if props[1] >= item:
            temp.update(set(converted[1][item]))
    restaurants.intersection_update(temp)

    for i in range(2, len(props) - 1):  # -1 for hours
        if type(props[i]) is list and not props[i]:
            continue
        elif type(props[i]) is list:
            temp = set()
            for key in props[i]:
                # if key in converted[i]:
                temp.update(set(converted[i][key]))
            restaurants.intersection_update(temp)
        else:
            restaurants.intersection_update(set(converted[i][props[i]]))
        """
        for item in converted[i]:
            if type(props[i]) is list and item in props[i]:
        
            if props[i] == item:
                temp = temp.update(set(converted[i][item]))
        """
        restaurants.intersection_update(temp)

    return restaurants


if __name__ == "__main__":
    T = solution()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))
    sol = T.solve()
    print("   Solution: %s" % sol)
    print()
    pprint(displaySolution())
    print()
    print(getRestaurants())
    # print("\nVariable likelihoods:")
    #   for v, vn in zip([a, b, c, x, y, z], 'abcxyz'):
    # Ensure that you only send these functions NNF formulas
    # Literals are compiled to NNF here
    #        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
