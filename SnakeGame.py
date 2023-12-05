import pygame
import random
import os

pygame.mixer.init()     #for add music 

pygame.init()

#colors
white =(255,255,255)
red = (255,0,0)
black = (0,0,0)

#creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#background images
#playing game
bgimg = pygame.image.load('bg.jpg')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
#starting
bgimg2 = pygame.image.load("Snake_Game_starting.jpg")
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()
#game over
bgimg3 = pygame.image.load("gameo.jpg")
bgimg3 = pygame.transform.scale(bgimg3, (screen_width, screen_height)).convert_alpha()

#game title 
pygame.display.set_caption("SnakeGameWithTithi")
pygame.display.update()
clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 55)

custom_font = pygame.font.Font('gomarice_no_continue.ttf', 55)
custom_font2 = pygame.font.Font('gomarice_no_continue.ttf', 30)

def text_screen(text,color,x,y):
    screen_text = custom_font.render(text, True, color)
    gameWindow.blit(screen_text, (x,y))

def text_screen2(text,color,x,y):
    screen_text2 = custom_font2.render(text, True, color)
    gameWindow.blit(screen_text2, (x,y))

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():              #Welcome screen
    exit_game = False
    while not exit_game :
        pygame.mixer.music.load('nagin.mp3')
        pygame.mixer.music.play()

        gameWindow.fill((130,99,150))#purple color
        gameWindow.blit(bgimg2,(0,0))
        text_screen2("Snakes Game by Tithi" ,black,5,5)
        text_screen("Welcome to Snakes Game..." ,black,20,420)
        text_screen("Press Space Bar to Play" ,black,270,470)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

#game loop
def gameloop() : 
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 25
    fps = 60
    velocity_x = 0
    velocity_y = 0 
    init_velocity = 5
    snk_list = []
    snk_length = 1
    score = 0

    food_x = random.randint(20,screen_width/2)
    food_y = random.randint(20,screen_height/2)

    pygame.mixer.music.load('nagin.mp3')
    pygame.mixer.music.play(-1)

    if (not os.path.exists ("highscore.txt")):
        with open("highscore.txt",'w') as f:
            f.write("0")

    with open("highscore.txt",'r') as f:
        highscore = f.read()

    while not exit_game:

        if game_over :
            with open("highscore.txt",'w') as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(bgimg3,(0,0))
            text_screen("Game Over !!!",black,300,150)
            text_screen("Press Enter to Continue...",black,150,450)
            text_screen("Score : "+ str(score),black,550,280)
            text_screen("Highscore : "+ str(highscore),black,20,280)

            for event in pygame.event.get() :
                
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RETURN :
                        welcome()

        else :

            for event in pygame.event.get() :
                
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT :
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT :
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP :
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN :
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q :    #cheatcode to score high
                        score+=10

            snake_x = snake_x + velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<9 and abs(snake_y-food_y)<9:
                score+=10
                print("Score : ",score)
                food_x = random.randint(20,screen_width/2)
                food_y = random.randint(20,screen_height/2)
                snk_length += 5

                if score>int(highscore) :
                        highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen2("Score : " + str(score) ,(255,255,0),5,5)
            text_screen2("Highscore : " + str(highscore) ,(255,255,0),690,5)
    
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:       #game over if snake touch at the wall
                pygame.mixer.music.stop()
                pygame.mixer.music.load('ohnoc.mp3')
                pygame.mixer.music.play()
                game_over = True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height: #game over if snake touch it self
                pygame.mixer.music.stop()
                pygame.mixer.music.load('ohnoc.mp3')
                pygame.mixer.music.play()
                game_over=True

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()