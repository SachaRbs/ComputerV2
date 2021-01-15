import re
from assignation import save_complex, save_matrix, save_function, save_reel, database
from calculus import solve

def assigation(inpt):
    ass = inpt.replace(' ', '').split('=')
    if len(ass) != 2:
        return('Error: expression is not valid')
    name, value = ass
    if 'i' in value:
        return save_complex(name, value)
    elif '[' in value:
        return save_matrix(name, value)
    elif re.match(r'[a-z]*\([a-z]*\)', name):
        return save_function(name, value)
    else:
        return save_reel(name, value)

def calculus(inpt):
    ass = inpt.replace(' ', '').split('=')
    if len(ass) != 2 or ass[1][-1] != "?":
        return('Error: expression is not valid')
    y = ass[1].replace('?', '')
    equation = ass[0]
    return(solve(equation, y))
    
def main():
    print("----------------------")
    print("Welcome to Computer V2")
    print("----------------------")

    while(1):
        inpt = input('> ')
        if inpt == 'DB':
            print(database)
        elif inpt == 'exit':
            exit()
        elif "?" in inpt:
            print(calculus(inpt.lower()))
        else:
            print(assigation(inpt.lower()))

if __name__ == "__main__":
    main()