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
'''
while(str(p.EXITCODE) != str(22)):
    nn = Network()
    #nn.setWeights()
    OBJ = p.GameGrid(nn.forward)
    print(p.EXITCODE)
'''
layers = []
layers.append(nn.Linear(c.GRID_LEN*c.GRID_LEN, 4*c.GRID_LEN*c.GRID_LEN))
layers.append(nn.Sigmoid())
layers.append(nn.Linear(4*c.GRID_LEN*c.GRID_LEN, 4))
layers.append(nn.Sigmoid())

net = nn.Sequential(*layers)

with torch.no_grad():
    net[0].weight = nn.Parameter(torch.ones_like(net[0].weight))
    net[0].weight[0, 0] = 2.
    net[0].weight.fill_(3.)

print(net)