import pathlib
import os
import pickle
import glob
import torch
import copy
import numpy as np
import torch.autograd
import torch.optim as optim
import torch.nn as nn
from torch.autograd import Variable
from .models import Actor, Critic
from .utils import Memory

device = 'cpu'

if torch.cuda.is_available():
    device = 'cuda'


class DDPGagent:
    def __init__(self, parameters):
        # Params
        hidden_sizes          = parameters['hidden_sizes']
        actor_learning_rate   = parameters['actor_learning_rate']
        critic_learning_rate  = parameters['critic_learning_rate']
        gamma                 = parameters['gamma']
        tau                   = parameters['tau']
        max_memory_size       = parameters['max_memory_size']
        vars                  = parameters['vars']
        controls              = parameters['controls']
        self.batch_size       = parameters['batch_size']
        self.controls         = controls 
        self.vars             = vars
        self.num_states       = len(vars)
        self.num_actions      = sum(controls.values())
        self.gamma = gamma
        self.tau = tau

        self.hidden_sizes = hidden_sizes
        sizes_actor = hidden_sizes.copy()
        sizes_actor.insert(0, self.num_states)
        sizes_critic = hidden_sizes.copy()
        sizes_critic.insert(0, self.num_states + self.num_actions)

        # Networks
        self.actor = Actor(sizes_actor, self.num_actions)
        self.actor_target = Actor(sizes_actor, self.num_actions)
        self.critic = Critic(sizes_critic)
        self.critic_target = Critic(sizes_critic)
        if torch.cuda.is_available():
            self.actor.cuda()
            self.actor_target.cuda()
            self.critic.cuda()
            self.critic_target.cuda()

        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data)

        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data)
        
        # Training
        self.memory = Memory(max_memory_size)        
        self.critic_criterion  = nn.MSELoss()
        #self.actor_optimizer = optim.Adadelta(self.actor.parameters)
        #self.critic_optimizer = optim.Adadelta(self.critic.parameters)
        self.actor_optimizer  = optim.Adam(self.actor.parameters(), lr=actor_learning_rate)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=critic_learning_rate)
    
    def get_action(self, state):
        state = Variable(torch.from_numpy(state).float().unsqueeze(0))
        action = self.actor.forward(state.to(device))
        action = action.detach().cpu().numpy()[0,:]
        #action = action.detach().numpy()[0,:]
        return action

    def update(self, batch_size):
        states, actions, rewards, next_states, _ = self.memory.sample(batch_size)
        states = torch.FloatTensor(states).to(device)
        actions = torch.FloatTensor(actions).to(device)
        rewards = torch.FloatTensor(rewards).to(device)
        next_states = torch.FloatTensor(next_states).to(device)
    
        # Critic loss        
        Qvals = self.critic.forward(states, actions)
        next_actions = self.actor_target.forward(next_states)
        next_Q = self.critic_target.forward(next_states, next_actions).detach()
        Qprime = rewards + self.gamma * next_Q
        critic_loss = self.critic_criterion(Qvals, Qprime)

        # Actor loss
        policy_loss = -self.critic.forward(states, self.actor.forward(states)).mean()
        
        # update networks
        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward() 
        self.critic_optimizer.step()

        # update target networks 
        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))
       
        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))

    def save(self, path, name=""):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True) 
        torch.save(self.critic.state_dict(), path + "/critic"+name)
        torch.save(self.critic_optimizer.state_dict(), path + "/critic_optimizer"+name)
        torch.save(self.actor.state_dict(), path + "/actor"+name)
        torch.save(self.actor_optimizer.state_dict(), path + "/actor_optimizer"+name)
        with open(path +'/memory.pickle', 'wb') as handle:
            pickle.dump(self.memory, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self, path, name=""):
        self.critic.load_state_dict(torch.load(path + "/critic"+name, map_location=device))
        self.critic_optimizer.load_state_dict(torch.load(path + "/critic_optimizer"+name,  map_location=device))
        self.critic_target = copy.deepcopy(self.critic)
        self.actor.load_state_dict(torch.load(path + "/actor"+name,  map_location=device))
        self.actor_optimizer.load_state_dict(torch.load(path + "/actor_optimizer"+name,  map_location=device))
        self.actor_target = copy.deepcopy(self.actor)

