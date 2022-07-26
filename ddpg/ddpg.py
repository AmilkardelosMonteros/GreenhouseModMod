import pathlib
import os
import pickle
import pickle5 as p
import glob
import torch
import copy
import pandas as pd
import numpy as np
import json
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
        self.hidden_sizes     = parameters['hidden_sizes']
        actor_learning_rate   = parameters['actor_learning_rate']
        self.actor_learning_rate = actor_learning_rate
        critic_learning_rate  = parameters['critic_learning_rate']
        self.critic_learning_rate = critic_learning_rate
        self.gamma            = parameters['gamma']
        self.tau              = parameters['tau']
        max_memory_size       = parameters['max_memory_size']
        vars                  = parameters['vars']
        self.controls         = parameters['controls']
        self.batch_size       = parameters['batch_size']
        self.vars             = vars
        self.num_states       = len(vars)
        self.num_actions      = self.num_actions_()
        sizes_actor           = self.hidden_sizes.copy()
        sizes_actor.insert(0, self.num_states)
        sizes_critic          = self.hidden_sizes.copy()
        sizes_critic.insert(0, self.num_states + self.num_actions)
        self.limit            = 3000
        self.critic_loss_     = np.zeros(self.limit)
        self.policy_loss_     = np.zeros(self.limit)
        self.i                = 0 
        self.real_changes     = 0
        self.real_changes_eps = list()
        #seed = 45
        # Networks
        #torch.manual_seed(seed)
        self.actor = Actor(sizes_actor, self.num_actions)
        #torch.manual_seed(seed)
        self.actor_target = Actor(sizes_actor, self.num_actions)
        #torch.manual_seed(seed)
        self.critic = Critic(sizes_critic)
        #torch.manual_seed(seed)
        self.critic_target = Critic(sizes_critic)
        #breakpoint()
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
    
    def num_actions_(self):
        s = 0
        for _,v in self.controls.items():
            if v == True:
                s+=1
        return s

    def get_action(self, state):
        state = Variable(torch.from_numpy(state).float().unsqueeze(0))
        action = self.actor.forward(state.to(device))
        action = action.detach().cpu().numpy()[0,:]
        #action = action.detach().numpy()[0,:]
        return action

    def update(self, batch_size):
        states, actions, rewards, next_states, _ = self.memory.sample(batch_size)
        states, actions, rewards, next_states = np.array(states), np.array(actions), np.array(rewards), np.array(next_states)
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
        #Actor 
        x = torch.ones(1,9)
        y = self.actor.forward(x)
        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()
        y1 = self.actor.forward(x)
        if torch.norm(y-y1) > 0:
            self.real_changes+= 1
        #Critic 
        self.critic_optimizer.zero_grad()
        critic_loss.backward() 
        self.critic_optimizer.step()

        # update target networks 
        #Actor
        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(self.tau * param.data + (1.0 - self.tau)*target_param.data)
        
        #Critic

        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(self.tau *param.data + (1.0 - self.tau)*target_param.data)

        self.critic_loss_[self.i%self.limit] = critic_loss
        self.policy_loss_[self.i%self.limit] = policy_loss
        self.i += 1

    def save_losses(self,path):
        critic_loss_ = {}
        policy_loss_ = {}
        i = 0
        for x,y in zip(self.critic_loss_,self.policy_loss_): 
            critic_loss_[str(i)] = float(x)
            policy_loss_[str(i)] = float(y)
            i+=1
        with open(path + '/output/critic_loss.json', 'w') as outfile:
            json.dump(critic_loss_, outfile,indent = 4)
        with open(path + '/output/policy_loss.json', 'w') as outfile:
            json.dump(policy_loss_, outfile,indent = 4)
    
    def save_real_changes(self,path):
        self.real_changes_eps.append(self.real_changes)
        self.real_changes = 0
        data = pd.DataFrame(self.real_changes_eps)
        data.to_csv(path + '/reports/changes.csv')



    def save(self, path, name=""): 
        pathlib.Path(path+'/nets/'+name).mkdir(parents=True, exist_ok=True)
        
        #Critic 
        torch.save(self.critic.state_dict(), path + "/nets/"+ name +"/critic")
        torch.save(self.critic_optimizer.state_dict(), path + "/nets/"+ name +"/critic_optimizer")
        
        #Critic target 
        torch.save(self.critic_target.state_dict(), path + "/nets/"+ name +"/critic_target")

        #Actor
        torch.save(self.actor.state_dict(), path + "/nets/"+ name +"/actor")
        torch.save(self.actor_optimizer.state_dict(), path + "/nets/"+ name +"/actor_optimizer")

        #Actor target
        torch.save(self.actor_target.state_dict(), path + "/nets/"+ name +"/actor_target")

        #Memory
        with open(path +'/output/memory.pickle', 'wb') as handle:
            pickle.dump(self.memory, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self, path, name=""):
        #Critic
        self.critic.load_state_dict(torch.load(path + "/nets/"+ name +"/critic", map_location=device))
        #self.critic_optimizer.load_state_dict(torch.load(path + "/nets/"+ name +"/critic_optimizer",  map_location=device))
        self.critic_optimizer  = optim.Adam(self.critic.parameters(), lr=self.critic_learning_rate)

        #Critic target
        self.critic_target.load_state_dict(torch.load(path + "/nets/"+ name +"/critic_target", map_location=device))

        #Actor
        self.actor.load_state_dict(torch.load(path + "/nets/"+ name +"/actor",  map_location=device))
        #self.actor_optimizer.load_state_dict(torch.load(path + "/nets/"+ name +"/actor_optimizer",  map_location=device))
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=self.actor_learning_rate)
        
        #Actor target 
        self.actor_target.load_state_dict(torch.load(path + "/nets/"+ name +"/actor_target",  map_location=device))

        #Critic
        self.critic.train()
        self.critic_target.train()

        #Actor
        self.actor.train()
        self.actor_target.train()

        #Memory
        file = open(path + '/output/memory.pickle', 'rb')
        self.memory = p.load(file)
        file.close()



