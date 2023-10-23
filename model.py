import torch 
from torch.nn import *

class Q_model(Module):
    def __init__(self,actions,init_state):
        super(Q_model,self).__init__()
        self.flat = Flatten()
        self.relu = ReLU()
        self.nn1 = Conv1d(init_state, 24, 1)
        self.nn2 = Linear(48,75)
        self.nn3 = Linear(75,24)
        self.nn4 = Linear(24,actions)
        self.softmax = Softmax(dim=1)
        
    def forward(self,x):
        # print("INPUT SHAPE: ",x.shape)
        x = self.nn1(x)
        # print(x.shape)
        x = self.relu(x)
        x = self.flat(x)
        # print(x.shape)
        x = self.nn2(x)
        x = self.relu(x)
        x = self.nn3(x)
        x = self.relu(x)
        x = self.nn4(x)
        # print(x.max(0)[0])
        return x 