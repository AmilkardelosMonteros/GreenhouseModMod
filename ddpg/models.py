import torch
import torch.nn as nn
import torch.nn.functional as F 
import torch.autograd
from torch.autograd import Variable


class Critic(nn.Module):
    def __init__(self, h_sizes):
        super(Critic, self).__init__()
        self.hidden = nn.ModuleList()
        for k in range(len(h_sizes) - 1):
            self.hidden.append(nn.Linear(h_sizes[k], h_sizes[k+1]))
        
        # Aplicaremos batch norm en la salida de la primera capa
        #self.bn = nn.BatchNorm1d(num_features=h_sizes[1]) 
        self.out = nn.Linear(h_sizes[-1], 1)

    def forward(self, state, action):
        """
        Params state and actions are torch tensors
        """
        x = torch.cat([state, action], 1)
        for i, layer in enumerate(self.hidden):
            x = layer(x)
            x = F.relu(x)
        x = self.out(x)
        return x


class Actor(nn.Module):
    def __init__(self, h_sizes, output_size, learning_rate=3e-4):
        super(Actor, self).__init__()
        self.hidden = nn.ModuleList()
        for k in range(len(h_sizes) - 1):
            self.hidden.append(nn.Linear(h_sizes[k], h_sizes[k+1]))

        # Aplicaremos batch norm en la salida de la primera capa
        #self.bn = nn.BatchNorm1d(num_features=h_sizes[1]) 
        self.out = nn.Linear(h_sizes[-1], output_size)
        
    def forward(self, state):
        """
        Param state is a torch tensor
        """

        x = state
        # import pdb; pdb.set_trace()
        for i, layer in enumerate(self.hidden):
            x = layer(x)
            x = F.relu(x)
        x = torch.sigmoid(self.out(x))
        return x