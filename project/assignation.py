import re
import sympy

op = ['-', '+', '*', '/', '%']
fct_name = []
database = {}

def is_numeric(s):
    try:
        float(s)
        return True
        int(s)
        return(True)
    except:
        return False

def save_reel(name, value):
    try:
        l = 0
        for fct_n in fct_name:
            if re.match(r'[a-z]+', fct_n)[0] in value:
                fct = re.search(r'[a-z]+\([a-z0-9]+\)', value)[0]
                var = re.search(r'\([a-z0-9]+\)', fct)[0][1:-1]
                x = re.search(r'\([a-z0-9]+\)', fct_n)[0][1:-1]
                value = value.replace(fct, str(database[fct_n][0]).replace(x, var))
                value = value.replace(" ", "")
        therms = re.split(r'\+|-|\*|/|%|\(|\)', value)
        for therm in therms:
            if therm not in op and not is_numeric(therm) and therm != "":
                if therm in database:
                    value = value[:l] + str(database[therm][0]) + value[l + len(therm):]
                    l = l + len(str(database[therm][0])) + 1
                else:
                    print("ERROR can't find {} in DB".format(therm))
            else:
                l = l + len(therm) + 1
        database[name] = [eval(value), 'R']
        return database[name][0]
    except:
        return "Error: can't assign {} to {} - Real Error".format(name, value)

def save_complex(name, value):
    try:
        value = value.replace('*', '')
        value = value.replace('i', 'j')
        imag = re.search(r'[+|\-]?[0-9]+j', value)[0]
        reel = value.replace(imag, '')
        get = ""
        if imag[0] != '-' and imag[0] != '+':
            get = '+'
        value = reel + get + imag
        c = complex(value)
        sign = '-' if c.imag < 0 else '+'
        database[name] = ['{} {} {}i'.format(c.real, sign, abs(c.imag)), 'C']
        return database[name][0]
    except:
        return "Error: can't assign {} to {} - Complex Error".format(name, value)

def save_matrix(name, value):
    try:
        matrix = []
        thermes = re.findall(r'\[[-?\d+.?\d+,]+\]', value)
        for therm in thermes:
            number = re.findall(r'[-?\d+.?\d+]+', therm)
            l = []
            for n in number:
                l.append(float(n))
            matrix.append(l)
        database[name] = [matrix, 'M']
        return database[name][0]
    except:
        return "Error: can't assign {} to {} - Matrix Error".format(name, value)

def save_function(name, value):
    try:
        var = re.search(r'\([a-z]+\)', name)[0][1:-1]
        therms = re.split(r'\+|-|\*|/|%|\^|\(|\)', value)
        l = 0
        for therm in therms:
            if therm not in op and not is_numeric(therm.replace('x', '')) and therm != var and therm != "":
                if therm in database:
                    value = value[:l] + str(database[therm][0]) + value[l + len(therm):]
                    l = l + len(str(database[therm][0])) + 1
                elif therm != var:
                    print("ERROR can't find {} in DB".format(therm))
            elif var in therm and len(therm) > 1:
                value = value[:l + len(therm) - 1] + '*' + value[l + len(therm) - 1:]
                l = l + len(therm) + 1
            else:
                l = l + len(therm) + 1
        res = sympy.simplify(value)
        if 'zoo' in str(res):
            return('Division by 0 is Forbidden')
        database[name] = [res, 'F']
        fct_name.append(name)
        return str(database[name][0]).replace('**', '^')
    except:
        return "Error: can't assign {} to {} - Function Error".format(name, value)