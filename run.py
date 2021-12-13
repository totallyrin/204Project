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


''' # successful test to produce runtime-evaluated propositions.
    # retained as a reference model
for i in range(10):
    exec('m' + str(i) + "=BasicProposition('m" + str(i) + "')")
    print(eval("m" + str(i)).__repr__)
'''

# Basic Propositions
ff = BasicProposition("Fast-food")


@proposition(E)
class Dietary:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"
    
# Dietary restrictions
dv = Dietary("Vegetarian")
dd = Dietary("Dairy-free")
dg = Dietary("Gluten-free")
dh = Dietary("Halal")

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

def hour_float(hour, minute):
    return hour + (round(minute / 30) / 2) # round at 15m

@proposition(E)
class Time:
    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            today = datetime.today()
            day = today.weekday()
            # hour = today.hour + ((today.minute // 30) / 2) + 0.5  # floors to next half hour
            hour =  hour_float(today.hour, today.minute)
            if hour == 24.0 or hour + 0.5 == 24.0:  # convert to next day if > 24
                day = (day + 1) % 7
                hour = 0.0
            self.data = {day: [hour, hour + 0.5]}

    def __repr__(self):
        return f"{self.data}"


time = Time()


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def solution():
    # TODO: User input to add constraints below

    props = ['Rating (1-5): ', 'Price (1-4): ', 'Dietary restrictions(d/g/h/v): ', 'Fast-food (y/n): ',
             'Seating (in/out): ', 'Parking ([b]ike/[v]ehicle): ', 'Service (eat-[in]/take-[out]/[d]elivery): ',
             'Day Mon-Sun (0-6): ', 'Time ([00:00~23:59],[xx:xx],[xx]): ', 'Weather ([r]ain/[sn]ow/[su]n): ']

    print("Input specific requirements below. Leave empty for any/not constrained.\n"
          + "    Separate multiple inputs with a space character.\n")

    '''performs input validation, so that constraints can be freely added
        without worrying about exec() accessing something it shouldn't'''
    for i in range(len(props)):
        props[i] = input(props[i]).lower()
        # if rating or price (numerical) try get int except choose random
        if i < 2:
            try:
                props[i] = int(props[i])
            except ValueError:
                props[i] = None
        # dietary
        elif i == 2:
            temp = set()
            for letter in props[i]:
                if letter in ('d', 'g', 'h', 'v'):
                    temp.add(letter)
            props[i] = temp
        # ff
        elif i == 3:
            if 'y' in props[i]:
                props[i] = True
            elif 'n' in props[i]:
                props[i] = False
            else:
                props[i] = None
        # seating - can't specify not indoor/not outdoor yet
        elif i == 4:
            temp = []
            if 'in' in props[i]:
                temp.append('indoor')
            if 'out' in props[i]:
                temp.append('outdoor')
            props[i] = temp
        # parking
        elif i == 5:
            if 'v' or 'c' in props[i]:
                props[i] = 'v'
            elif 'b' in props[i]:
                props[i] = 'b'
            else:
                props[i] = None
        # service
        elif i == 6:
            props[i] = props[i].split()
            svc = ('in', 'out', 'd') # might grab the d in [in/out]doors
            temp = set()
            for ser in props[i]:
                for s in svc:
                    if s in props[i]:
                        temp.add(s)
            props[i] = temp
        # day
        elif i == 7:
            try:
                props[i] = int(props[i])
                if 0 > props[i] > 6:
                    props[i] = None
            except ValueError:
                props[i] = None
        # time
        elif i == 8:
            try:
##                props[i] = [int(j) for j in props[i].split(':')]
                props[i] = [j.split(':') for j in props[i].split('~')]
##                print(props[i])
                for j in props[i]:
                    if len(j) == 1:
                        j.append(0)
                    if 0 > int(j[0]) > 23 or 0 > int(j[1]) > 59:
                        props[i] = None
                        
                global time
                # if hour isn't specified, the day probably doesn't matter either, so default to now
                time = Time({props[7] if props[7] is not None else datetime.today().weekday():
                             [hour_float(int(props[8][0][0]), int(props[8][0][1])),
                              hour_float(int(props[8][1][0]), int(props[8][1][1])) if len(props[8]) > 1 else
                              hour_float(int(props[8][0][0]), int(props[8][0][1])) + 0.5]
                             })
            except ValueError:
                props[i] = None
        
        # weather
        elif i == 9:
            if props[i] not in ('r', 'sn', 'su'):
                props[i] = None

##    print(props)

    # for con in props

    # If no rating specified, set lowest rating
    E.add_constraint(r1 if props[0] is None else eval('r'+str(props[0])))
    # If no price specified, set most expensive price
    E.add_constraint(p4 if props[1] is None else eval('p'+str(props[1])))
    
    for restriction in props[2]:
        E.add_constraint(eval('d'+restriction))
    # fast food
    if props[3] is True:
        E.add_constraint(ff)
    elif props[3] is False:
        E.add_constraint(~ff)
        
    # If seating specified, eat-in is required
    if props[4] is not None:
        for r in props[4]:
            E.add_constraint(eval(r))
        E.add_constraint(eatin)
        
    # If no service preference specified, set any
    if props[6] is None:
        E.add_constraint(eatin | takeout | delivery)
    else:
        if 'in' in props[6]:
            E.add_constraint(eatin)
            # If eat-in, then there must be seating
            E.add_constraint(eatin >> (indoor | outdoor))
        if 'out' in props[6]:
            E.add_constraint(takeout)
        if 'd' in props[6]:
            E.add_constraint(delivery)
            
    '''the current time and weather are not particularly negotiable,
        so they're not constrained here as if they're adjustable'''

    

    # constraint.add_exactly_one(E, Rating)  # a rating must exist
    # constraint.add_exactly_one(E, Price)  # a price must exist
    # constraint.add_exactly_one(E, Weather)  # weather must exist
    # constraint.add_at_least_one(E, Service)  # service must exist

    E.add_constraint(ff >> takeout)  # 'fast food' restaurants have take-out
    # E.add_constraint(eatin >> (indoor | outdoor))
    E.add_constraint((indoor | outdoor) >> eatin)
    E.add_constraint(((rain | snow) & eatin) >> indoor)

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
    props = [0, 0, [], False, [], [], [], time]  # rating, price, dietary, fastFood, seating, parking,
    # service, day, hours
    if not T.satisfiable():
        return props
##    print(props)
    dietary = ["Vegetarian", "Dairy-free", "Halal", "Gluten-free"]
    seating = ["Indoor", "Outdoor"]
    parking = ["Vehicle", "Bike"]
    service = ["Eat-in", "Take-out", "Delivery"]
    # day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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
        elif type(element) is dict:
            props[7] = element

    restaurants = set()

    for item in converted[0]:
        if props[0] <= item:
            restaurants.update(set(converted[0][item]))

    temp = set()

    for item in converted[1]:
        if props[1] >= item:
            temp.update(set(converted[1][item]))
    restaurants.intersection_update(temp)

    for i in range(2, len(props) - 1):  # -1 for time
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

    temp = set()
    time_dict = eval(props[-1].__repr__())
    for i in time_dict:
        open_h = properties.fill_in_hours(time_dict[i])
        for j in range(48):
            if open_h[j]:
                temp.update(set(converted[-1][i][j / 2]))
    # if temp is empty here, nothing in restaurants is kept, which isn't ideal
    open_r = restaurants.intersection(temp)
    if not restaurants:
        return restaurants
    elif not open_r:
        print("The following restaurants, which fulfill the prior constraints,"
              + " are all currently closed.\n"
              + "    Perhaps try a different Time, or maybe using other restrictions.\n")
    else:
        restaurants = open_r # so only restrict if options remaining exist

    return restaurants


if __name__ == "__main__":
    T = solution()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
##    print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))
    sol = T.solve()
    '''
    print("   Solution: %s" % sol)
    '''
##    print(time.__repr__())
    '''
    print(displaySolution())
    '''
    print('\n' + '-'*100)
    options_list = getRestaurants()
    print(options_list if options_list else
          "Maybe try adjusting some requirements, or adding new restaurants!")
    # print("\nVariable likelihoods:")
    #   for v, vn in zip([a, b, c, x, y, z], 'abcxyz'):
    # Ensure that you only send these functions NNF formulas
    # Literals are compiled to NNF here
    #        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
