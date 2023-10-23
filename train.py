from env import Enviroment
from model import Q_model
from torch import optim
from memory import ReplayMemory, Transition
import torch
import random
import math
from torch.nn import *
from itertools import count
from matplotlib import pyplot as plt

BATCH_SIZE = 10
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4

env = Enviroment()
n_actions = env.action_space.n 
state = env.reset()
# state_shape = int(env.observation_space.high[0] * env.observation_space.high[1])

policy_net = Q_model(n_actions,len(state)) #Compute point for current state
target_net = Q_model(n_actions,len(state)) #Compute point for next state
policy_net.load_state_dict(policy_net.state_dict()) #Create init value of model

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)

steps_done = 0

points = []


def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(points, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Point')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated

def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        return policy_net(state).max(1)[1].view(1,1).type(torch.long)
    else:
        return torch.tensor([[env.action_space.sample()]],dtype=torch.long)
    
def optimize_model():
    if len(memory) < BATCH_SIZE:
        return 
    transitions = memory.shuffle(BATCH_SIZE)
    batch = Transition(*zip(*transitions))
    # print(batch.state)
    
    state_batch = torch.cat(batch.state,dim=0)
    # print(state_batch)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    next_state_batch = torch.cat(batch.next_state)
    
    # q of state
    state_action_values = policy_net(state_batch).gather(1,action_batch)
    print("STATE ACTION VALUE : ", state_action_values)
    
    #q of next state
    with torch.no_grad():
        next_state_values = target_net(next_state_batch).max(1)[0]
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    
    #Compute Huber loss
    criterion = SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))
    
    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

def train():
    for e in range(10000):
        state = env.reset().unsqueeze(0)
        score = 0
        for t in count():
            action = select_action(state)
            # print(action)
            new_state, point, done = env.step(action[0][0])
            new_state = new_state.unsqueeze(0)
            score += point
            score_tensor = torch.tensor([score])
            memory.push(state,action,new_state,score_tensor)
            state = new_state
            optimize_model()
            
            #Update parameter of target net (target = policy * t + target * (1-t))
            target_net_state_dict = target_net.state_dict()
            policy_net_state_dict = policy_net.state_dict()
            for key in policy_net_state_dict:
                target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
            target_net.load_state_dict(target_net_state_dict)
            
            
            if done:
                points.append(score)
                plot_durations()
                break
    torch.save(target_net.state_dict(),"./target.pt")
    # torch.save(policy_net.state_dict(),"./policy.pt")
    print('Complete')
    plot_durations(show_result=True)
    plt.ioff()
    plt.show()

train()