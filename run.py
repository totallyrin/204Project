from pprint import pprint
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

from properties import *

# Encoding that will store all of your constraints
E = Encoding()


# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicProposition:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


# Basic Propositions
f = BasicProposition("Fast-food")

# Dietary restrictions
v = BasicProposition("Vegetarian")
d = BasicProposition("Dairy-free")
h = BasicProposition("Halal")

# Seating location
i = BasicProposition("Indoor")
o = BasicProposition("Outdoor")

# Parking
c = BasicProposition("Vehicle")
b = BasicProposition("Bike")


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html


@constraint.exactly_one(E)
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


@constraint.exactly_one(E)
@proposition(E)
class Price:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


# Price ($ or $$ or $$$)
p1 = Price("$")
p2 = Price("$$")
p3 = Price("$$$")


@constraint.at_least_one(E)
@proposition(E)
class Service:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"


# dine-in, take-out, delivery
di = Service("Eat-in")
t = Service("Take-out")
u = Service("Delivery")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def solution():
    E.add_constraint(di & (i | o))  # dine-in means there must be either indoor or outdoor seating
    E.add_constraint(f >> t)  # fast-food restaurants have take-out

    # E.add_constraint(r3 >> (r3 | r4 | r5))
    # E.add_constraint(r3 & p2)

    return E


def displaySolution():
    if not T.satisfiable():
        return
    result = []
    lis = T.solve()
    for key in lis.keys():
        if lis.get(key):
            result.append(key.__repr__())
    result.sort()
    return result


# trying to write a function to return corresponding restaurant
# def getRestaurants():
#     props = [0, 0, [], False, [], [], [], []]  # rating, price, dietary, fastFood, seating, parking, service, hours
#     if not T.satisfiable():
#         return props
#     dietary = ["Vegetarian", "Dairy-Free", "Halal"]
#     seating = ["Indoor", "Outdoor"]
#     parking = ["Vehicle", "Bike"]
#     service = ["Eat-in", "Take-out", "Delivery"]
#     converted = properties.convert_properties()
#     lis = displaySolution()
#     for element in lis:
#         if '*' in element:
#             props[0] = (int(element[0]))
#         elif '$' in element:
#             props[1] = (len(element))
#         elif element in dietary:
#             props[2].append(element.lower())
#         elif element == "Fast-food" and props[3] is False:
#             props[3] = True
#         elif element in seating:
#             props[4].append(element.lower())
#         elif element in parking:
#             props[5].append(element.lower())
#         elif element in service:
#             props[6].append(element.lower())
#     pprint(props)
#     for j in range(len(props)):
#         for key in converted[j]:


if __name__ == "__main__":
    T = solution()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())
    print()
    pprint(displaySolution())
    print()
    # print("\nVariable likelihoods:")
    #   for v, vn in zip([a, b, c, x, y, z], 'abcxyz'):
    # Ensure that you only send these functions NNF formulas
    # Literals are compiled to NNF here
    #        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
