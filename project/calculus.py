import re
from assignation import is_numeric, database, fct_name
from CPV1 import compute_poly

def simple_matrix_multiplication(one, two, n_matrix):
    if n_matrix == 2:
        if len(one) != len(two) or len(one[0]) != len(two[0]):
            return "Error: bad matrix shape Matrix-1 : {}, Matrix-2 : {}".format((len(one), len(one[0])), (len(two), len(two[0])))
        else:
            res = []
            for i in range(len(one)):
                line = []
                for j in range(len(one[0])):
                    line.append(one[i][j] * two[i][j])
                res.append(line)
            return res
    else:
        if is_numeric(two):
            one, two = two, one
        for i in range(len(two)):
            for j in range(len(two[0])):
                two[i][j] = float(one) * two[i][j]
        return two
    
def multiple_matrix_multiplication(M1, M2):
    result = [[0 for col in range(len(M1))] for row in range(len(M2[0]))]
    if len(M1[0]) == len(M2):
        for i in range(len(M1)):
            for j in range(len(M2[0])):
                for k in range(len(M2)):
                    result[i][j] += M1[i][k] * M2[k][j]
        return result
    else:
        return "Error: bad matrix shape Matrix-1 : {} Matrix-2 : {}".format((len(M1), len(M1[0])), (len(M2), len(M2[0])))
 

def matrix_calculus(equation):
    e = []
    n_matrix = 0
    thermes = re.split(r'(\*{1,2})', equation)
    for therm in thermes:
        if therm.isupper():
            n_matrix = n_matrix + 1
            e.append(database[therm.lower()][0])
        else:
            e.append(therm)
    if len(e) != 3:
        return 'Error'
    if e[1] == '*':
        return simple_matrix_multiplication(e[0], e[2], n_matrix)
    elif e[1] == '**':
        return multiple_matrix_multiplication(e[0], e[2])
    else:
        return 'Error: wrong operateur : {}'.format(e[1])

op = ['+', '-', '*', '**', '/', '%', '(', ')', '^']

def solve(equation, y):
    l = 0
    var = None
    for i in range(len(fct_name)):
        if re.match(r'[a-z]+', fct_name[i])[0] in equation:
            fct = re.search(r'[a-z]+\([a-z0-9]+\)', equation)[0]
            var = re.search(r'\([a-z0-9]+\)', fct)[0][1:-1]
            x = re.search(r'\([a-z0-9]+\)', fct_name[i])[0][1:-1]
            equation = equation.replace(fct, str(database[fct_name[i]][0]).replace(x, var))
            equation = equation.replace(" ", "")
    therms = re.split(r'(\+|-|\*{1,2}|/|%|\^|\(|\))', equation)
    for therm in therms:
        if therm == "":
            continue
        elif therm in op or therm == var:
            l = l + len(therm)
        elif is_numeric(therm):
            l = l + len(therm)
        elif therm in database:
            if database[therm][1] == 'M':
                equation = equation[:l] + therm.upper() + equation[l + len(therm):]
                l = l + len(therm)
            elif database[therm][1] == 'F':
                l = l + len(therm)
                continue
            else:
                equation = equation[:l] + str(database[therm][0]) + equation[l + len(therm):]
                l = l + len(str(database[therm][0]))
        else:
            return "Error: Can'y find {} in Database".format(therm)
    equation = equation.replace(' ', '')
    if re.findall(r'[a-zA-Z]', equation) == []:
        print('eval')
        return eval(equation)
    else:
        if equation.islower():
            print('function')
            if not is_numeric(y) and y in database:
                y = database[y][0]
            else:
                return ("Error y = {}".format(y))
            equation = equation + '=' + str(y)
            compute_poly(equation.replace("**", "^"))
        else:
            print('matrix')
            #sympy.symplify ?
            return matrix_calculus(equation)
    
            
