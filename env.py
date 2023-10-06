from gym import Env
from gym.spaces import Discrete, Box 
import numpy as np
from pynput.keyboard import Key, Controller
import random 
import pygame
from snake_game import SnakeGame, window_width, window_height, dis, snake_speed, snake_block, clock

class Enviroment:
    def __init__(self) -> None:
        self.action_space = Discrete(4) #0 : Up, 1 : Down, 2: Left, 3:Right
        self.observation_space = Box(low=np.array([0,0],dtype=np.float32), high=np.array([window_width,window_height],dtype=np.float32))
        #First State 
        self.keyboard = Controller()
        self.snake = SnakeGame(dis)
        
    def render(self,state):
        dis.fill((255,255,255))
        for head in state:
            pygame.draw.rect(dis,(0,0,255),[head["x"],head["y"],head["width"],head["length"]])
        pygame.draw.rect(dis,(255,0,0),[self.snake.food["x"],self.snake.food["y"],self.snake.food["width"],self.snake.food["length"]])
        pygame.display.update()
        clock.tick(snake_speed)
        
    def step(self,action):
        state, point, done = self.snake.event_handle(action) 
        self.render(state)
        return state, point, done 

    def reset(self):
        self.snake.restart()
      
print("HERE")  
env = Enviroment()
env.step(2)
env.step(1)
env.step(3)