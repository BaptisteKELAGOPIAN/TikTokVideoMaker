def my_print(string, color):
    if(color == 'red'):
        print('\x1b[1;31;41m' + string + '\x1b[0m')
    elif(color == 'green'):
        print('\x1b[1;32;42m' + string + '\x1b[0m')
    else :
        print(string)