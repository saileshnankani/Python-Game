# Filename: saileshNankani_JoeLinGame.py
# Author: Sailesh Nankani and Joe Lin
# Date: January 20th, 2015
# Description: This program runs a game called Dash Square where the user controls the square. The objective of the game is to dodge as many as
# triangles as possible. The user gets a score for dodging each triangle. The user only has one life at a time.  

# --------1) Import & start pygame -----------------------------------------
import pygame, sys   
from pygame.locals import * 
from random import randint
import random

pygame.init()

pygame.mixer.init()


# --------2) Definitions: Classes, Constants and Variables --------------------------
# Class(es): MyTriangleClass, PlayerClass and Player

class MyTriangleClass(pygame.sprite.Sprite):                                  
    def __init__(self, image_file, speed, location):              
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer     
        self.image = pygame.image.load("image/triangle.png")                        
        self.rect = self.image.get_rect()                                 
        self.rect.left, self.rect.top = location                          
        self.speed = speed                                               

    def move(self):                                                       
        global points, score_text                                         
        self.rect = self.rect.move(self.speed)                            

        if self.rect.left <= -57:   
            if self.speed[0] == -26:    # restricts the speed to maximum of -26
                self.speed[0] = random.randrange(-24, -7) # randomly chooses the speed of the triangle once it reaches maximum speed

            elif self.speed[0] != -27:
                self.speed[0] = self.speed[0]-1  # increases the speed of the triangle after each miss
            points = points + 1   # increases the score


class PlayerClass(pygame.sprite.Sprite):

    allsprites = pygame.sprite.Group() #to store all the sprites
    def __init__(self, x, y, width, height, img_string):

        pygame.sprite.Sprite.__init__(self)
        PlayerClass.allsprites.add(self)

        self.image = pygame.image.load("image/main1.png")

        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y

        self.width = width
        self.height = height

#creating a class called Player which contians the variables for player
class Player(PlayerClass): 

    List = pygame.sprite.Group() #stroe all sprites in a list
    def __init__(self, x, y, width, height, img_string):

        PlayerClass.__init__(self, x, y, width, height, img_string)
        Player.List.add(self)
        self.velx = 0
        self.vely = 10
        self.jump = False
        self.fall = False


    #creating a function which stops the player from going outsie of the screen
    def motion(self, width, height):

        predicted_location = self.rect.x + self.velx

        if predicted_location < 0:
            self.velx = 0
        elif predicted_location + self.width > width:
            self.velx = 0

        self.rect.x += self.velx

        self.__jump(height)

    #creating a function which specify the jump
    def __jump(self, height):

        max_jump = 210

        if self.jump:

            if self.rect.y < max_jump:
                self.fall = True

            if self.fall:
                self.rect.y += self.vely

                predicted_location = self.rect.y + self.vely

                if predicted_location + self.height > height - 120:
                    self.jump = False
                    self.fall = False

            else:
                self.rect.y -= self.vely

# Constants:BLACK, WHITE
BLACK = (0,0,0)
WHITE = (255,255,255)


# Variables: clock, FPS, delay, interval, keepGoing, pygame GUI components (screenWidth, screenHeight, screen, background, my_font, arrowKeys, 
# title, ruleDisplay1, ruleDisplay2, ruleDisplay3, gameControl1, gameControl2, bg_image)


clock = pygame.time.Clock()
FPS = 40                    
delay = 100
interval = 50
scoreList=[0]
keepGoing = True

# pygame GUI & sound components
screenWidth = 700
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))
background = pygame.Surface((screenWidth, screenHeight))

my_font = pygame.font.SysFont("arial", 20)

arrowKeys = pygame.image.load("image/ArrowKeys.jpg")
title = my_font.render("WELCOME TO THE SQUARE DASH!", True, BLACK)
ruleDisplay1 = my_font.render("Rules:", True, BLACK)
ruleDisplay2 = my_font.render("1) You are the square. Dodge the triangles to score using the controls specified below.", True, BLACK)
ruleDisplay3 = my_font.render("2) You have only 1 life to play this game.", True, BLACK)
gameControl1 = my_font.render("Game controls:", True, BLACK)
gameControl2 = my_font.render("Use the arrow keys to move around and dodge.", True, BLACK)
start = my_font.render("Press (SPACE) to start.", True, WHITE)
bg_image = pygame.image.load("image/bg_image.jpg")

pygame.key.set_repeat(delay, interval)



# ------------3) Sounds set-up ------------------------------------------------

r = randint(0, 2) #pick random number from 0 to 1
#This is a list that stores different background musics (0 = welcome1, 1 = welcome2) the number 
#it selects is random which is to be determined by the upper code.
sounds = [pygame.mixer.Sound("sound/welcome1.wav"), #play if random picked 0
          pygame.mixer.Sound("sound/welcome2.wav"), #play if random picked 1
          pygame.mixer.Sound("sound/welcome3.wav")] #play if random picked 2
backgroundMusic = sounds[r] #play the song
backgroundMusic.play(-1) #loop that song 
d = randint(0, 2)
sounds_inGame = [pygame.mixer.Sound("sound/bgm1.wav"), #play if random picked 0
                 pygame.mixer.Sound("sound/bgm2.wav"), #play if random picked 1
                 pygame.mixer.Sound("sound/bgm3.wav")] #play if random picked 2
backgroundMusic_inGame = sounds_inGame[d] #play the song
sound_eff = pygame.mixer.Sound("sound/jump_eff.wav")

# -------------4) Pygame commands ------------------------------------------
# 4a) Set up pygame GUI components (caption, background)

screen = pygame.display.set_mode((700,480))
pygame.display.set_caption("Rules")
background = pygame.Surface(screen.get_size()).convert()
screen.fill(WHITE)
background.fill(WHITE)

# 4b) display the rules screen until user closes it 

keepGoingRules = True

while keepGoingRules:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoingRules = False
            sys.exit()  

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:    # exits the while loop and displays the main game screen 

                backgroundMusic_inGame.play(-1)
                backgroundMusic.fadeout(500)
                pygame.time.delay(1000)

                background.fill(WHITE)
                pygame.display.set_caption("Rules")
                keepGoingRules = False

            #end of if event.key 
        #end of if event
    #end for event

    #display the rules to the screen   
    screen.blit(background, (0, 0))
    screen.blit(ruleDisplay1, (20, 50))
    screen.blit(title, (190, 10))
    screen.blit(ruleDisplay2, (20, 90))
    screen.blit(ruleDisplay3, (20, 120))
    screen.blit(gameControl1, (20, 160))
    screen.blit(gameControl2, (150, 322))
    screen.blit(start, (250, 388))
    arrowKeys = arrowKeys.convert() #need to convert it after we have set-up the screen
    screen.blit(arrowKeys, (270,200)) #draw img onto temporary buffer that is not displayed  
    background.blit(bg_image, (0, 0))

    pygame.display.flip()
    # end of rule screen

# 4c) Set up pygame GUI components (speedTriangle, clock, points, score, width, height, screen, caption, font, score_text, textpos, gameOver) for
# the main game screen 

speedTriangle = 7 # initial speed of the triangle
clock = pygame.time.Clock()                                                               
points = 0    # for final screen
score = 0     # for main screen
width = 700   
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Square Dash - The Game")
font = pygame.font.Font(None, 50)                                         
score_text = font.render(str(points), 1, (0, 0, 0))                       
textpos = [10, 10]                                                          
gameOver = False

# ememyGroup components
myTriangle = MyTriangleClass('image/triangle.png', [(-1*speedTriangle),0], [50, 50]) # defines myTriangle
enemy = pygame.sprite.Group(myTriangle)  # groups triangles as enemy
myTriangle.rect.topleft = (700, 310)
# Player 
player = Player(20, 310, 50, 50, "image/main1.png")

#4d) displays the game until the user closes it or until the square collides with the triangle

while not gameOver: 

    screen.fill([255, 255, 255])                                       
    for event in pygame.event.get():                                   
        if event.type == pygame.QUIT:                                  
            sys.exit()    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.velx = 5 #move the square right

    elif keys[pygame.K_LEFT]:
        player.velx = -5 #move the square left


    else:
        player.velx = 0 #if nothings pressed the player will not move

    #if the up arrow is pressed the jump function is activated
    if keys[pygame.K_UP]:
        sound_eff.play()              # plays the jump sound everytime the square jumps
        sound_eff.set_volume(0.05)
        player.jump = True


    player.motion(width, height) #set-up the border
    screen.fill(WHITE) #fill screen white
    pygame.draw.rect(screen, BLACK, (0, 360, 700, 120)) #draws the ground 
    PlayerClass.allsprites.draw(screen) #draws all the sprites on the screen
    highestScore = str(len(scoreList)-1) # gets the last score
    highScore = my_font.render(highestScore, True, BLACK)    
    screen.blit(myTriangle.image, myTriangle.rect.topleft)                             
    screen.blit(highScore, [10, 10])  # blits the score on the top left of the main screen      
    screen.blit(myTriangle.image, myTriangle.rect.topleft)  
    pygame.display.flip()

    if pygame.sprite.spritecollide(player, enemy, False): # if the square collides with the triangle

        gg_image = pygame.image.load("image/gg_image.jpg")
        pygame.display.set_caption("Game Over")  # sets the caption for final screen
        screen.blit(gg_image, (0, 0))   # displays the background for final screen
        backgroundMusic_inGame.stop()   # stops the background music

        final_text1 = "Game Over"
        final_text2 = "Your final score is:  " + str(points)
        final_text3 = "The game will close in 5 seconds."

        ft1_font = pygame.font.Font(None, 70)
        ft1_surf = font.render(final_text1, 1, (0, 0, 0))  

        ft2_font = pygame.font.Font(None, 50)
        ft2_surf = font.render(final_text2, 1, (0, 0, 0))  

        ft3_font = pygame.font.Font(None, 50)
        ft3_surf = font.render(final_text3, 1, (0, 0, 0)) 

        screen.blit(ft1_surf, [screen.get_width()/2 - \
                               ft1_surf.get_width()/2, 100])            # displays "Game Over"

        screen.blit(ft2_surf, [screen.get_width()/2 - \
                               ft2_surf.get_width()/2, 200])            # displays the final score

        screen.blit(ft3_surf, [screen.get_width()/2 - \
                               ft3_surf.get_width()/2, 300])            # displays the time it will take to close the game

        pygame.display.flip()

        gameOver = True                # exits the while loop                                           
        pygame.time.delay(5000)        # waits for 5 seconds 
        sys.exit()                     # closes the game

    if not gameOver: 
        pygame.display.flip()                                             
        myTriangle.move()             # moves the Triangle

    if myTriangle.rect.left <= -57:
        scoreList.append(score)      
        myTriangle.rect.topleft = [800, 310]    # blits the triangle back to its original position  

    clock.tick(FPS)



