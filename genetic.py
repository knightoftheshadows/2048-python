import puzzle as p
import constants as c
from logic import MATRIX
import random

def nn1():
    if (random.random()  > 0.75):
        return 'a'
    elif (random.random()  < 0.25):
        return 's'
    elif (random.random()  > 0.50):
        return 'd'
    else:
        return 'w'



while(str(p.EXITCODE) != str(c.WINAT)):
    OBJ = p.GameGrid(nn1)
    print(p.EXITCODE)

