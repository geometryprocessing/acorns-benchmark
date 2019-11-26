import random, string


def function_generator(degree, variables, terms, input_string):
    def gen_polynomial(select_deg, append_term, select_var):
        for deg in range(0, select_deg-1):
            append_term += select_var + ' * '
        append_term += select_var
        return append_term


    op = [' + ', ' - ', ' * ', ' / ']
#     paranthesis = ['']
    blocks = random.randint(1,1)
    

    append_term = ''
    for b in range(blocks):

        select_deg = random.randint(1,degree)
        select_var = random.choice(variables)
        # fix this
#         select_paranthesis = random.choice(paranthesis)

        
        if b==0:
            append_term += gen_polynomial(select_deg, append_term, select_var)
        else:
            append_term = append_term + ' * '+gen_polynomial(select_deg, '', select_var)

    select_op = random.choice(op)
    
    if len(input_string)==0:
        input_string.append('('+append_term+')')
    else:
        input_string.append(select_op + '('+ append_term+')')

    if len(input_string) == terms:
        final_string = ''.join(input_string)  
        return final_string
    else:          
        return function_generator(degree, variables, terms, input_string)

from itertools import combinations

def gen_vars(k):
    alphabets = list(string.ascii_lowercase)
    alphabets.remove('i')


    if k<=23:
        return alphabets[0:k]
    
    outputs = alphabets

    for num_maxdigits in range(2,100):
        combinations_ = list(combinations(alphabets,num_maxdigits))
        outputs +=   [''.join(item) for item in combinations_]
        if len(outputs)>k:
            return outputs[0:k]





import argparse
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('num_variables', type = int, help='file name')
    parser.add_argument('num_terms', type = int, help='file name')

    parser = parser.parse_args()



    functions = []
    alphabets = list(string.ascii_lowercase)
    alphabets.remove('i')
    f = open("generated_function.txt","w")

    variables = gen_vars(parser.num_variables)
    print(variables)
    temp = [function_generator(parser.num_variables,variables,parser.num_terms,[]), variables]
    functions.append(temp)
    f.write(str(temp))
    print(str(temp))
    f.close()


