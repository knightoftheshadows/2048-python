import puzzle as p
import constants as c
import random

def nn1(mat):
    if (random.random()  > 0.75):
        return 'a'
    elif (random.random()  < 0.25):
        return 's'
    elif (random.random()  > 0.50):
        return 'd'
    else:
        return 'w'

while(str(p.EXITCODE) != str(22)):
    
    OBJ = p.GameGrid(nn)
    print(p.EXITCODE)

