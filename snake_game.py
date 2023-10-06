import pygame
import random
from gym import Env
from gym.spaces import Discrete, Box 

window_width = 400
window_height = 300
game_over=False
snake_block = 10
snake_speed = 30
pygame.init()
dis=pygame.display.set_mode((window_width,window_height))
clock = pygame.time.Clock()
pygame.display.update()
pygame.display.set_caption('Snake game by Edureka')

class SnakeGame:
    def __init__(self,dis) -> None:
        self.dis = dis
        self.one_head = {
            "x" : 200,
            "y" : 150,
            "width" : snake_block,
            "length" : snake_block
        }
        self.snake_heads = [self.one_head]
        self.food = {
            "x" : round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0,
            "y" : round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0,
            "width" : snake_block,
            "length" : snake_block
        }
        self.event = None 
        self.game_over = False
        
    def snake_move(self,x,y):
        self.snake_heads.insert(0,{
            "x": self.snake_heads[0]["x"] + x,
            "y" : self.snake_heads[0]["y"] + y,
            "width" : snake_block,
            "length" : snake_block
        })
        del self.snake_heads[-1]
        print("MOVE", self.snake_heads)
    
    def snake_eat(self,x,y):
        #Create new food
        self.food["x"] = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
        self.food["y"] = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
        
        #Increase snake head
        new_head = {
            "x" : self.snake_heads[-1]["x"] - x,
            "y" : self.snake_heads[-1]["y"] - y,
            "width" : snake_block,
            "length" : snake_block
        }
        self.snake_heads.append(new_head)
        print("EAT", self.snake_heads)
        
    def event_handle(self,event):
        if event.type == pygame.QUIT:
            self.game_over = True
            return self.game_over
        elif event.type == pygame.KEYDOWN:
            x_change = 0
            y_change = 0
            if event.key == pygame.K_LEFT:
                x_change = -snake_block
            elif event.key == pygame.K_RIGHT:
                x_change = snake_block
            elif event.key == pygame.K_UP:
                y_change = -snake_block
            elif event.key == pygame.K_DOWN:
                y_change = snake_block
            self.snake_move(x_change,y_change)
            if self.snake_heads[0]["x"] == self.food["x"] and self.snake_heads[0]["y"] == self.food["y"]:
                self.snake_eat(x_change, y_change)
            if self.snake_heads[0]["x"] >= window_width or self.snake_heads[0]["y"] >= window_height or (self.snake_heads[0] in self.snake_heads[1:]):
                #Hit boundary or eat itself
                self.game_over = True
    
    def start(self):
        while not self.game_over:
            for event in pygame.event.get():
                self.event_handle(event)
            dis.fill((255,255,255))
            for head in self.snake_heads:
                pygame.draw.rect(dis,(0,0,255),[head["x"],head["y"],head["width"],head["length"]])
            pygame.draw.rect(dis,(255,0,0),[self.food["x"],self.food["y"],self.food["width"],self.food["length"]])
            pygame.display.update()
            clock.tick(snake_speed)
        pygame.quit()
        quit()
          
game = SnakeGame(dis)
game.start()