import pygame
from pygame.locals import *
import time
import random


SIZE = 35
length = 32

class Apple:
    def __init__ (self,parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.png")
        self.x = SIZE*3
        self.y = SIZE*3
    def draw_apple(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        max_x = (500 // SIZE - 1) * SIZE
        max_y = (500 // SIZE - 1) * SIZE
        self.x = random.randint(0, max_x // SIZE) * SIZE
        self.y = random.randint(0, max_y // SIZE) * SIZE

class Snake:
    def __init__(self,parent_screen,length):
        self.length = length
        self.parent_screen=parent_screen
        self.block = pygame.image.load("resources/box.png")
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='down'
        
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw_snake(self):
        self.parent_screen.fill((50,168,72))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
        
    
    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'    
    
    def move_right(self):
        self.direction = 'right'
    
    def move_left(self):
        self.direction = 'left'
        
    def walk(self):
        
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        self.draw_snake()
        
        
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background()
        self.screen = pygame.display.set_mode((500,500))
        self.screen.fill((50, 168, 72))
        self.snake=Snake(self.screen,1)
        self.snake.draw_snake()
        self.apple=Apple(self.screen)
        self.apple.draw_apple()
        
        pygame.display.flip()
        
    def play_background(self):
        pygame.mixer.music.load("resources/background-game-melody-loop.mp3")
        pygame.mixer.music.play(loops=-1)
        
    def play_sound(self,sound):
        track = pygame.mixer.Sound(sound)
        pygame.mixer.Sound.play(track)
        
    def collision(self,x1,y1,x2,y2):
        if(y1 < y2 + SIZE and y1 >= y2):
            if(x1 < x2 + SIZE and x1 >= x2):
                return True
        return False
            
            
    def play(self):
        self.snake.walk()
        self.apple.draw_apple()
        self.display_score()
        pygame.display.flip()
        
        if self.collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            
            self.play_sound("resources/Ding-sound-effect.mp3")
            self.snake.increase_length()
            self.apple.move()
            
        for i in range(3,self.snake.length):
            if self.collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("resources/cymbal-crash-sound-effect.mp3")
                raise "Game Over"
        if self.snake.x[0] < 0 or self.snake.x[0] >= 500 or self.snake.y[0] < 0 or self.snake.y[0] >= 500:
            self.play_sound("resources/cymbal-crash-sound-effect.mp3")
            raise "Game Over"
            
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score : {self.snake.length}",True,(0,0,0))
        self.screen.blit(score,(400,20))
        
    def reset(self):
        self.snake=Snake(self.screen,1)
        self.apple=Apple(self.screen)
        
    def show_game_over(self):
        self.screen.fill((255,255,255))
        font = pygame.font.SysFont('arial',30)
        game_over = font.render(f"Game Over! Your Score :{self.snake.length}",True,(0,0,0))
        self.screen.blit(game_over,(100,200))
        font = pygame.font.SysFont('arial',30)
        line2 = font.render(f"To retry press Enter.To exit press Escape!!",True,(0,0,0))
        self.screen.blit(line2,(20,250))
        pygame.display.flip()
        pygame.mixer.music.pause()
    
    def run(self):
        running = True
        pause = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                        
                    if not pause:
                        if event.key == K_ESCAPE:
                            running = False
                        if event.key==K_UP:
                            self.snake.move_up()
                        if event.key==K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type==QUIT:
                    running = False   
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.2) 

if __name__ == "__main__":
    game = Game()
    game.run()
    
    #pygame.display.flip()
   # block = pygame.transform.scale(block,(500,500))
    
  
    