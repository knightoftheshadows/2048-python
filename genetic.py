import puzzle as p
import constants as c
import random
import torch
import torch.nn as nn



class Network(nn.Module):
    def __init__(self):
        super().__init__()

        # Inputs to hidden layer linear transformation
        self.hidden = nn.Linear(c.GRID_LEN*c.GRID_LEN, 4*c.GRID_LEN*c.GRID_LEN)
        #another hidden layer
        self.hidden2 = nn.Linear(4*c.GRID_LEN*c.GRID_LEN, 256)
        # Output layer, 4 units = one for each direction
        self.output = nn.Linear(256, 4)

        # Define sigmoid activation and softmax output
        self.sigmoid = nn.Sigmoid()
        self.sigmoid2 = nn.Sigmoid()
        self.sigmoid3 = nn.Sigmoid()

    def forward(self, x):
        #preprocessing
        y = []
        for i in x:
            for e in i:
                y.append(float(e))
        x = y
        x = torch.tensor(x)
        #pass tensor through each layer
        x = self.hidden(x)
        x = self.sigmoid(x)
        x = self.hidden2(x)
        x = self.sigmoid2(x)
        x = self.output(x)
        x = self.sigmoid3(x)
        x = x.tolist().index(max(x.tolist())) #returns the index which has max probability

        #transforms index into char
        valid_chars = [c.KEY_LEFT, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_UP]

        return valid_chars[x]

def fakenn(mat):
    if (random.random()  > 0.75):
        return 'a'
    elif (random.random()  < 0.25):
        return 's'
    elif (random.random()  > 0.50):
        return 'd'
    else:
        return 'w'

while(str(p.EXITCODE) != str(22)):
    nn = Network()
    OBJ = p.GameGrid(nn.forward)
    print(p.EXITCODE)

