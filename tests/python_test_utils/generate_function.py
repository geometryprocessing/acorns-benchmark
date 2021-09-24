import string
import random

character_selection = 'abcdefghjklmnopqrstuvwxzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def gen_other(s):
    if s > len(character_selection):
        raise Exception("s must be less than {}".format(len(character_selection))) 
    vars = create_vars(s)

    function_string = ""
    adept_function_string = ""

    # print('----')

    prefix_string = ""
    for i in range(s):
        prefix_string += "4*"

    product_string = ""
    adept_product_string = ""
    for i, var in enumerate(vars):
        product_string += "({} * (1 - {}))".format(var, var)
        adept_product_string += "(sum({} * (1 - {})))".format(var, var)

        if (i != len(vars) - 1):
            product_string += "*"
            adept_product_string += "*"
    
    function_string = prefix_string + "(" + product_string + ")"
    adept_function_string = prefix_string + "(" + adept_product_string + ")"

    function = [function_string, vars]
    adept_function = [adept_function_string, vars]
    print (adept_function)
    print(vars)
    return function, adept_function

def create_vars(s):
    vars = []
    i = 0
    while i < s:
        letter = random.choice(character_selection)
        if letter not in vars:
            vars.append(letter)
            i += 1
    return vars

def generate_simple(s):
    if s > len(character_selection):
        raise Exception("s must be less than {}".format(len(character_selection))) 
    vars = create_vars(s)

    ders_string = ""

    for i, var in enumerate(vars):
        ders_string += var 

        if (i != len(vars) - 1):
            ders_string += "*2*"

    function = [ders_string, vars]
    return function

func = gen_other(7)
# print(func)