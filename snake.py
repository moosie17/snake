import pygame
import sys
from pygame.math import Vector2
import random

# How to make a rect and display on the screen --
# - create a surface object :: test_surface = pygame.Surface((dimenstions for the size of surface))
# - test_rect = test_surface.get_rect(center = (coordinates for where you want the center of the rect to be)) 
# - in the game loop :: screen.blit(test_surface, test_rect)
# - rect gives more control to move objects because you can access multiple positions on it such as --
# - center, topright, topleft, right, left, midtop, midbottom, bottomright, bottomleft

# What do we need for this game --
# - A Fruit and a Snake

class Fruit():
    # Class to create a fruit in the game which the snake will chase
    def __init__(self):
        # Defining x and y coordinates of the fruit and assigning it to a vector
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126,166,144), fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Snake():
    def __init__(self):
        # Define body of the snake as a list of three adjacent vectors on the screen --
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        # Curved body parts --
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sounds/crunch.wav')
    
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # Position the snake on the display screen --
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            # Check which direction is the Head of the snake facing --
            if index == 0:
                screen.blit(self.head, block_rect)
            
            # Check which direction is the Tail of the snake facing --
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            
            # Check if the middle blocks are horizontal or vertical or a corner in orientation --
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                        
    
    def update_head_graphics(self):

        # Function to compare two blocks and see what the Head orientation needs to be
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down


    def update_tail_graphics(self):
        # Function to compare two blocks and see what the Tail orientation needs to be
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down


    
    def move_snake(self):
        if self.new_block == True:
            # Extending the length of the snake -- 
            body_copy = self.body[:]
            # Insert snake head at the beginning of the list 
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        
        else:
            # The head of the snake moves first, and then the remaninig blocks take the position
            # of their predecessing blocks...and the final block (snake's tail) gets deleted
            # Create a copy of the snake position and drop the last block (tail) in that vector list --
            body_copy = self.body[:-1]
            # Insert snake head at the beginning of the list 
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def play_crunch_sound(self):
        self.crunch_sound.play()

    def game_reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        print("Game restarted")

class Main():
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()
    
    def check_collision(self):
        # check if the head of the snake is on the fruit --
        if(self.fruit.pos == self.snake.body[0]):
            # reposition the fruit --
            self.fruit.randomize()
            # extend the length of the snake by adding a new block at it's tail --
            self.snake.add_block()
            # Play the crunch sound --
            self.snake.play_crunch_sound()
        
        # To make sure the newly created fruit doesn't land anywhere on the snake body --
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def check_fail(self):
        # check if snake is outside the screen window --
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            print("Game over - snake crashed into the game window")
            self.game_over()
    
        # check if snake head hits itself on any block --
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                print("Game over - snake collided with itself")
                self.game_over()
    
    def game_over(self):
        # pygame.quit()
        # sys.exit()
        self.snake.game_reset()
    
    def draw_grass(self):
        grass_color = (167,209,61)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        # Length of the snake at any given time --
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
# Dimensions to create the grid on the screen
cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

clock = pygame.time.Clock()
fps = 30

# Adding image for the fruit surface --
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('PoetsenOne-Regular.ttf', 25)

main_game = Main()

# Create a custom USEREVENT to make the snake move every 150 ms --
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
# Note -- invoke this custom USEREVENT in the event loop below

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)

            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)


    screen.fill((175,215,70))
    # screen.fill((255,255,255))

    # Drawing fruit and snake on the display screen --
    main_game.draw_elements()

    # screen.blit(test_surface, test_rect)
    pygame.display.update()
    clock.tick(fps)
