# Snake Game
import pygame
import time
import random
pygame.init()
# Setting the Game Window
length = 500
width = 300
bg1=pygame.image.load("colorsky.jpeg")  #For loading the image from the source with relative path.
s=pygame.display.set_mode((length,width))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()  #used to define fps
exit_game = False
# Passing Initial Position
pos_x=30
pos_y=50
x,y=5,0
score=0
food_x=random.randint(50,length-50)
food_y=random.randint(50,width-50)
fps=60
font = pygame.font.SysFont(None,45)

def plot_snake(gamewindow,color,snk_list,snake_size):
    size=0
    for x,y in snk_list[::-1][1:]:       # -2 is taken due to excluding the head arguments and taking only body args
        rect=pygame.draw.circle(gamewindow,color,[x,y],snake_size+size)
        rect.center=(x,y)
        size-=0.02

def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    s.blit(screen_text,[x,y])

snk_list=[]         # To store snake body coordinates
snk_length=2        # To speify the snake length
y_move_lock=True    #locking the movements
x_move_lock=True
start_command=True  
while not exit_game:
    time.sleep(0.025)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit_game=True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                exit_game=True
                break
            if event.key==pygame.K_RIGHT and y_move_lock:
                x=5
                y=0
                y_move_lock=False
                x_move_lock=True
                start_command=True
            if event.key==pygame.K_LEFT and y_move_lock and start_command:
                x=-5
                y=0
                y_move_lock=False
                x_move_lock=True
            if event.key==pygame.K_UP and x_move_lock:
                y=-5
                x=0
                x_move_lock=False
                y_move_lock=True
            if event.key==pygame.K_DOWN and x_move_lock:
                y=5
                x=0
                x_move_lock=False
                y_move_lock=True
    pos_x+=x
    pos_y+=y
    if abs(pos_x-food_x)<10 and abs(pos_y-food_y)<10:
        snk_length+=5
        score+=5
        food_x=random.randint(50,length-50)
        food_y=random.randint(50,width-50)
    s.fill((0,0,0))
    # s.blit(bg1,(0,0))   #for adding the background to the game window
    text_screen("Score: "+str(score),(255,0,0),5,5)
    pygame.draw.circle(s, (0,255,255), (food_x,food_y),10)
    head = []    
    head.append(pos_x)
    head.append(pos_y)
    if (pos_x>=length or pos_x<=0 or pos_y<=0 or pos_y>=width or (len(snk_list)>1 and head in snk_list[::-1])):
        y_move_lock=True
        x_move_lock=False
        start_command=False
        pos_x=30
        pos_y=50
        x,y=0,0
        snk_list=[]
        snk_length=1
        q=font.render("Game Over",True,(255,255,255))
        s.blit(q,[length//3,width//3])
        q=font.render("Final Score is: "+str(score),True,(255,255,255))
        s.blit(q,[length//3,width//2])
        pygame.display.update()
        time.sleep(1)
        s.fill((0,0,0))
        s.blit(s,(0,0))
        fo = pygame.font.SysFont(None,40)
        q=fo.render("Enter (-->)continue (Esc) to exit..",True,(255,255,255))
        s.blit(q,[length//10,width//1.5])
        pygame.display.update()
        time.sleep(1)
        score=0
    snk_list.append(head)

    if len(snk_list)>snk_length:  #this condition is used to break the body arguments if not eaten food.
        del snk_list[0]

    plot_snake(s, (0,255,0), snk_list,10)
    r1=pygame.draw.circle(s, (255,255,255),[pos_x,pos_y],10)     #used to specify the head of the snake

    pygame.display.update()
pygame.quit()
quit()