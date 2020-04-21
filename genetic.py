import puzzle as p
import constants as c
import random
import torch
import torch.nn as nn

'''
#fake neural network used for testing
def fakenn(mat):
    if (random.random()  > 0.75):
        return 'a'
    elif (random.random()  < 0.25):
        return 's'
    elif (random.random()  > 0.50):
        return 'd'
    else:
        return 'w'
'''
'''
    def forward(self, x, net):
        #preprocessing
        y = []
        for i in x:
            for e in i:
                y.append(float(e))
        x = y
        x = torch.tensor(x)
        #pass tensor through each layer
        net.
        x = x.tolist().index(max(x.tolist())) #returns the index which has max probability

        #transforms index into char
        valid_chars = [c.KEY_LEFT, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_UP]

        return valid_chars[x]
'''

chromosome1 = torch.randn(2*c.GRID_LEN * c.GRID_LEN, c.GRID_LEN * c.GRID_LEN, dtype=torch.float)
chromosome2 = torch.randn(c.GRID_LEN * c.GRID_LEN, 2*c.GRID_LEN * c.GRID_LEN, dtype=torch.float)


while(str(p.EXITCODE) != str(c.END_SCORE)):
    layers = []
    layers.append(nn.Linear(c.GRID_LEN * c.GRID_LEN, 2*c.GRID_LEN * c.GRID_LEN))
    layers.append(nn.Sigmoid())
    layers.append(nn.Linear(2*c.GRID_LEN * c.GRID_LEN, 4))
    layers.append(nn.Sigmoid())

    net = nn.Sequential(*layers)

    with torch.no_grad():
        print(net[0])
        print(net[0].weight)
        print(net[2].weight)
        net[0].weight = nn.Parameter(chromosome1)
        net[2].weight = nn.Parameter(chromosome2)

    OBJ = p.GameGrid(net)
    print(p.EXITCODE)

    print(net)